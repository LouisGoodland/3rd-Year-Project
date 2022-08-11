import pyautogui
import time
from PIL import ImageGrab

#Class dedicated to finding the lap time
class lapTimer():
    lapTimes = []
    foundFinish = False
    movingTimer = False
    #This function screenshots the area that the lap time will be in and returns laptime
    #(this will be 0 if there is no time)
    def findTime(self):
        timingState = ImageGrab.grab(bbox=(545, 90, 665, 115))
        singleLap = ""
        numberTuple = []
        #Adds an array of positions for each number to the number tuple
        #For each number
        for i in range(0,10):
            #for each number it adds a tuple containing its locations to another tuple
            numberGenerator = pyautogui.locateAll(r"F:\3rd Year Project\Important Screenshots\P" + str(i) + ".png", timingState, confidence=0.805)
            toAddTuple = []
            #add all the locations to the number specific tuple
            for i in numberGenerator:
                toAddTuple.append(i)
            numberTuple.append(toAddTuple)

        timeCalc = {}
        #for each number
        for i in range(0,10):
            #if there are positions for that number in the number tuple
            if (numberTuple[i] != []):
                #for each position of the number
                for x in numberTuple[i]:
                    #the position of that number = its number
                    timeCalc[x[0]] = i
        #creates a temporary array
        tempArr = []
        #adds everything from time calc into the temporary array
        for i in timeCalc:
            tempArr.append(i)
        #sorts the temporary array based on the values
        tempArr.sort()
        #so the temporary array will have a list of positions that corelate to numbers in the dictionary
        for i in tempArr:
            #for each item in the array, add the collected value from the dictionary (number)
            singleLap = singleLap + str(timeCalc[i])
        #if no times were added, set the time to 0
        if(singleLap==""):
            singleLap = 0
        #otherwise, convert to an int
        else:
            singleLap = int(singleLap)
        #return the time
        return singleLap

    #this method searches the screen to see if it can find the finish flag
    def findFinish(self):
        #550 x 330. 70 x 70 size
        finishCheckImage = ImageGrab.grab(bbox=(550, 330, 620, 400))
        #if it finds the finish flag, update the variable
        if pyautogui.locate(finishCheckImage, r"F:\3rd Year Project\Important Screenshots\finishFlag.png", confidence=0.98) != None:
            self.foundFinish = True
        else:
            self.foundFinish = False

    #this method takes two screenshots and compares them to tell if the lap timer is still moving
    def timerMoving(self):
        timingState = ImageGrab.grab(bbox=(545, 90, 665, 115))
        time.sleep(0.01)
        # if it finds the same lap time, update the variable
        if pyautogui.locate(timingState, ImageGrab.grab(bbox=(545, 90, 665, 115)),  confidence=0.97) != None:
            self.movingTimer = False
        else:
            self.movingTimer = True



