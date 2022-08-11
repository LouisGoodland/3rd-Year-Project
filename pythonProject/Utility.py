import math
import numpy as np
import matplotlib.pyplot as plt

#A method that calculates the restricted bounds of where to take a screenshot based on its location
def screenshotBoundary(x, y, radius, imageSize):
    #Makes min values non negative
    minXSearch = x - radius
    if (minXSearch < 0):
        minXSearch = 0
    minYSearch = y - radius
    if (minYSearch < 0):
        minYSearch = 0
    #Makes max values within the left hand size of the screen
    maxXSearch = x + radius
    if (maxXSearch > 960):
        maxXSearch = 960
    maxYSearch = y + radius
    if (maxYSearch > 1080):
        maxYSearch = 1080
    #if the min value is too small, make it the minimum required size
    if (minXSearch >= maxXSearch - imageSize[0]):
        minXSearch = maxXSearch - imageSize[0]
    if (minYSearch >= maxYSearch - imageSize[1]):
        minYSearch = maxYSearch - imageSize[1]
    #if the max value is too small, make it the minimum required size
    if (maxXSearch < minXSearch + imageSize[0]):
        maxXSearch = maxXSearch + imageSize[0]
    if (maxYSearch < minYSearch + imageSize[1]):
        maxYSearch = maxYSearch + imageSize[1]
    return minXSearch, minYSearch, maxXSearch, maxYSearch

#Attributes that will be used (Need to be non class specific)
carViewAccuracy = [0, 0, 0, 0]
miniMapAccuracy = [0, 0, 0, 0]
rewards = []
averageReward = []
laptimes = []
laptimePos = []
speed = []
averageSpeed = []
firstTimeSetUp = False

#capture int codes: 1 = inSmall, 2 = inLarge, 3 = fail
#used to report the accuracy of the capturing elements
def storeCaptureAccuracy(captureInt, location):
    if(location=="carView"):
        carViewAccuracy[0] = carViewAccuracy[0] + 1
        carViewAccuracy[captureInt] = carViewAccuracy[captureInt] + 1
    elif (location=="miniMap"):
        miniMapAccuracy[0] = miniMapAccuracy[0] + 1
        miniMapAccuracy[captureInt] = miniMapAccuracy[captureInt] + 1

#adds reward to array of rewards
def addReward(reward):
    rewards.append(reward)
    averageReward.append(np.mean(rewards))

#adds the laptimes to a list, along with its position in steps
def addLapTimes(lapTime):
    laptimes.append(lapTime)
    laptimePos.append(len(rewards))

#adds the average speed
def addAverageSpeed(speedX, speedY):
    speed.append(math.sqrt((speedX * speedX) + (speedY + speedY)))
    if(len(speed)>10):
        averageSpeed.append(np.mean(speed))
        speed.pop(0)

#Creates graph figures and saves them
def save(iteratorInt):
    plt.figure(figsize=[20, 15])

    size = 8000

    #Creates and saves a graph of the average rewards
    plt.xlabel('Step')
    plt.ylabel('Average Reward')
    plt.plot(averageReward[len(averageReward)-size:len(averageReward)-1])
    plt.savefig(r'F:\3rd Year Project\MachineModelCheckpoints\averageReward' + str(iteratorInt) + '.PNG')
    plt.clf()

    #Creates and saves a graph for the average speed
    plt.xlabel('Step')
    plt.ylabel('Average Speed')
    plt.plot(averageSpeed[len(averageSpeed)-size:len(averageSpeed)-1])
    plt.savefig(r'F:\3rd Year Project\MachineModelCheckpoints\averageSpeed' + str(iteratorInt) + '.PNG')
    plt.clf()

    #Creates and saves a graph with the capture accuracies
    viewLabels = ('Total_carView', 'Cap1_carView', 'Cap2_carView', 'Missed_carView', 'Total_miniMap', 'Cap1_miniMap', 'Cap2_miniMap', 'Missed_miniMap')
    heights = carViewAccuracy + miniMapAccuracy
    plt.bar(viewLabels, heights)
    plt.xticks(rotation=45)
    plt.xlabel('accuracies')
    plt.savefig(r'F:\3rd Year Project\MachineModelCheckpoints\captureAccuracy' + str(iteratorInt) + '.PNG')
    plt.clf()

    #Creates a saves a graph of the lap times
    plt.xlabel('position of laptime')
    plt.ylabel('time')
    plt.plot(laptimePos, laptimes)
    plt.savefig(r'F:\3rd Year Project\MachineModelCheckpoints\laptimes' + str(iteratorInt) + '.PNG')



