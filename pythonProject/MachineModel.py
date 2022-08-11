#List of all the imports
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten, Reshape, Softmax
import numpy as np
from tf_agents.specs import BoundedArraySpec
import time
import threading
import pyautogui
import LapTimer, GameController, CarView, MiniMapTracker, Utility, ImageOrientationDetection, Checkpoints
from gym import Env
from gym.spaces import Discrete

class RacingEnvironment(Env):

    #Initiates the env
    def __init__(self):
        #Actions we can take (4 car actions)
        self.action_space = Discrete(16)
        #This is where we observe, i.e the whole state
        self.observation_space = BoundedArraySpec(shape=([9]), dtype='int', name='observation', maximum=1000, minimum=0)
        #Sets up the initial state of the whole system
        self.state = (0,0,0,0,0,0,0,0,0)

        #Implements a large amount of default values
        self.collectedLap = False
        self.completeReward = False
        self.stepsTaken = 0
        self.distances = [0, 0, 0, 0]
        self.failed = False

        #Loads all of the class data that the machine model will use
        self.racingTrack = CarView.CarView()
        self.miniMap = MiniMapTracker.MiniMapTracker()
        self.lapTimer = LapTimer.lapTimer()
        self.imageOrientationObject = ImageOrientationDetection.TrainImage()
        self.orientationModel = self.imageOrientationObject.loadModel()
        #tick over 180, 120, 60 range 150, 180
        self.checkPointModel = Checkpoints.CheckPointCalc([[200, 250, 210, "x-"], [150, 180, 180, "y-"],
                                                           [150, 180, 120, "y-"], [150, 180, 60, "y-"],
                                                           [10, 40, 210, "x+"], [250, 275, 120, "y+"]])



    #Reset the game (call to set up game)
    def reset(self):

        #Puts all the key presses up
        GameController.offKeys()

        #If the game has never been set up this learning cycle
        if (Utility.firstTimeSetUp==False):
            Utility.firstTimeSetUp = True
            print("doing first time set up")
            GameController.backToMenu()

        else:
            #If the system didn't fail, reset the whole system
            if(self.failed == False):
                print("Did a lap! reseting environment")
                GameController.reset()

            #If the game didn't work, restart the game
            else:
                print("restarting environment")
                GameController.restart()

        #reset the last seen position
        self.racingTrack.resetPos()
        self.checkPointModel.reset()

        #resets the state
        self.state = (0,0,0,0,0,0,0,0,0)
        self.state = np.reshape(self.state, (1, 9))

        #resets all the required attributes
        self.distances = [0,0,0,0]
        self.distanceReward = 0
        self.stepsTaken = 0

        #sets attributes to false
        self.done = False
        self.completeReward = False
        self.collectedLap = False
        return self.state

    #What happens during a step of a function
    def step(self, action):
        #gets a timer, for seeing how long
        start = time.perf_counter()
        #Performs the valid key presses for a step
        GameController.stepKeyPress(action)
        # Needed for step function
        self.info = {}

        #Implements all of the different functions of the step
        self.lapTimerThread = threading.Thread(target=self.lapTimerThreadFunction())
        self.miniMapThread = threading.Thread(target=self.miniMapThreadFunction())
        self.carViewThread = threading.Thread(target=self.carViewThreadFunction())

        #Sets: isTiming, hasFinished, lapReward
        self.lapTimerThread.start()
        #Sets: speed, position, miniMapReward
        self.miniMapThread.start()
        #Sets orientation
        self.carViewThread.start()

        #Joins all of the threads back together
        self.lapTimerThread.join()
        self.lapTimerThread.join()
        self.carViewThread.join()

        # updates the state
        self.distances, self.distanceReward = self.racingTrack.getDistanceFromWalls()
        self.state = (self.speed[0], self.speed[1], self.position[0], self.position[1], self.orientation[0], self.distances[0],
            self.distances[1], self.distances[2], self.distances[3])
        #reshapes the state for usage
        self.state = np.array(self.state)
        self.state = np.reshape(self.state, (1, 9))

        # if it has completed a lap
        self.additionalLapReward = 0
        if (self.completeReward):
            # assume 60 second time
            while (self.collectedLap == False):
                print("searching for finish info")
                # if it finds the finish screen
                if pyautogui.locateOnScreen(r"F:\3rd Year Project\Important Screenshots\gameFinish.png", confidence=0.97) != None:
                    print("found the finish screen!")
                    #assume a set time
                    self.additionalLapReward = 100000
                    self.collectedLap = True
                    Utility.addLapTimes(10000)
                #Otherwise, try find the lap time
                else:
                    lapState = self.lapTimer.findTime()
                    #if it collects a valid lap time
                    if (lapState > 0):
                        print("time collected of ", lapState)
                        self.additionalReward = int(1000000000 / lapState)
                        self.collectedLap = True
                        Utility.addLapTimes(lapState)

        #Calculate the checkpoints if passed:
        print(" ")
        print(self.position[0], " ", self.position[1])
        #Does all of the rewards
        if(self.isTiming or self.completeReward):
            count = self.checkPointModel.updateCheckPointsPassed(self.position)
            count = count * 50000
            self.reward = self.miniMapReward + self.lapReward + self.additionalLapReward + self.distanceReward + count
        else:
            #resets the collected rewards
            self.miniMapReward, self.lapReward, self.additionalLapReward, self.distanceReward = 0, 0, 0, 0
            self.reward = -10000
            self.miniMap.collectPos(correctDirection=False)

        #Counts steps and resets if it has done too many
        self.stepsTaken = self.stepsTaken + 1
        if(self.stepsTaken > 200):
            print("done enough steps!")
            self.failed = True
            self.done = True

        #calculates the total step time and then adds this to the utility for diagnostics
        stepTime = round(time.perf_counter() - start, 2)
        self.diagnosticInfo(self.reward, stepTime)

        return self.state, self.reward, self.done, self.info

    def render(self):
        pass

    #responsible for calculating if the timer is moving,
    def lapTimerThreadFunction(self):
        self.lapReward = 0
        #makes 2 threads, 1 for seeing if the timer is moving, one if the finish flag is up
        lapTimerThread1 = threading.Thread(target=self.lapTimer.timerMoving())
        lapTimerThread2 = threading.Thread(target=self.lapTimer.findFinish())
        #starts them both
        lapTimerThread1.start()
        lapTimerThread2.start()
        #joins them together
        lapTimerThread1.join()
        lapTimerThread2.join()

        #sets the attributes for the attributes calculated in the threads
        self.hasFinished = self.lapTimer.foundFinish
        self.isTiming = self.lapTimer.movingTimer

        #if it found a finish
        if (self.hasFinished):
            print("lap completed")
            #initial reward for completing a lap
            self.lapReward = 1000000
            self.completeReward = True
            self.done = True

    #Collects all of the attributes from the miniMap
    def miniMapThreadFunction(self):
        self.speed = self.miniMap.speedCalc()
        self.position = self.miniMap.returnLocation()
        self.miniMapReward = self.miniMap.returnPosDifference()

    #Collects the view of the car from the racing track and uses the orientation model to work out the orientation
    def carViewThreadFunction(self):
        viewForOrientation = np.reshape(self.racingTrack.getView(), (1, 50, 50, 3))
        self.orientation = self.orientationModel.predict_classes(viewForOrientation)

    #Prints a large amount of diagnostic information in the console
    def diagnosticInfo(self, reward, stepTime):
        # stores the reward for graph plotting
        Utility.addReward(reward=reward)
        # Printing diagnostics:
        print("")
        print("steps taken: ", self.stepsTaken, " Orientation: ", self.orientation[0] * 30)
        print("Speed X: ", self.speed[0], " Speed Y: ", self.speed[1])
        print("Position X: ", self.position[1], " position y: ", self.position[0])
        print("Step time was: ", stepTime, " seconds")
        print("Distances: <", self.distances[0], " ^", self.distances[1], " >", self.distances[2], " v", self.distances[3])
        print("MiniMap Reward: ", self.miniMapReward, " Lap Rewards: ", (self.lapReward + self.additionalLapReward), " Distance Reward: ", self.distanceReward)
        print("-----------------------------------------------------------------------------------------------------")

#The model that is used to make the game choices
def neuralModel():
    model = Sequential()
    model.add(Reshape(input_shape=(1, 1, 9), target_shape=(1,9)))
    model.add(Flatten())
    model.add(Dense(units=3840, activation='elu'))
    model.add(Dense(units=1050, activation='elu'))
    model.add(Dense(units=370, activation='elu'))
    model.add(Dense(units=120, activation='elu'))
    model.add(Dense(units=84, activation='elu'))
    model.add(Dense(units=16, activation='elu'))
    model.add(Softmax())
    return model
