import pyautogui
from PIL import ImageGrab
import numpy as np
import math
import Utility

#Class dedicated to functions via the mini map car tracker
class MiniMapTracker():

    #Initialises the mini map
    def __init__(self):
        self.resetPos()
        self.initialPosCollected = False
        self.collectPos(correctDirection=True)

    #resets the array of positions
    def resetPos(self):
        #most recent
        self.xCoord = []
        self.yCoord = []
        #list of every pair co-ordinate average
        self.fullCoordList = []
        #base of min x and y co-ords
        self.minXSearch = 0
        self.minYSearch = 0

    #collects the position of the car on the minimap and adds to the list
    def collectPos(self, correctDirection):
        #If the initial position has been collected
        if (self.initialPosCollected):
            # Tries the first search with restricted parameters
            # Finds the restricted boundary co-ords
            self.minXSearch, self.minYSearch, self.maxXSearch, self.maxYSearch = Utility.screenshotBoundary(self.xCoord[len(self.xCoord) - 1], self.yCoord[len(self.yCoord) - 1], 40, [11, 11])
            # collects the image
            self.capture = pyautogui.locate(r"F:\3rd Year Project\Important Screenshots\carLocationOrb.png", ImageGrab.grab(bbox=(self.minXSearch, self.minYSearch, self.maxXSearch, self.maxYSearch)), confidence=0.6)
            # If it finds a capture
            if (self.capture != None):
                # Adds to statistics
                Utility.storeCaptureAccuracy(1, "miniMap")
                # Updates co-ords
                self.coOrdUpdates()
            # if it can't find it on the restricted version, try the derestricted version
            else:
                # changes the co-ords to the default search that will cover everything
                self.minXSearch, self.minYSearch, self.maxXSearch, self.maxYSearch = 0, 130, 400, 400
                # collects the image
                self.capture = pyautogui.locate(r"F:\3rd Year Project\Important Screenshots\carLocationOrb.png", ImageGrab.grab(bbox=(0, 130, 400, 400)), confidence=0.6)
                # If it finds a capture
                if (self.capture != None):
                    # Adds to statistics
                    Utility.storeCaptureAccuracy(2, "miniMap")
                    # Updates co-ords
                    self.coOrdUpdates()
                #if it fails to find the image
                else:
                    # Adds to statistics
                    Utility.storeCaptureAccuracy(3, "miniMap")

        #if the initial position hasn't been collected, try the vague approach
        else:
            # changes the co-ords to the default search that will cover everything
            self.img = ImageGrab.grab(bbox=(0, 130, 400, 400))
            # collects the image
            self.capture = pyautogui.locate(r"F:\3rd Year Project\Important Screenshots\carLocationOrb.png", self.img,confidence=0.6)
            # If it finds a capture
            if (self.capture != None):
                # Adds to statistics
                Utility.storeCaptureAccuracy(2, "miniMap")
                # Say it found the initial positioning
                self.initialPosCollected = True
                # Updates co-ords
                self.coOrdUpdates()
            # if it fails to find the image
            else:
                # Adds to statistics
                Utility.storeCaptureAccuracy(3, "miniMap")

        #if the size of the recents exceeds 10, remove one
        if (len(self.xCoord) > 10):
            self.xCoord.pop(0)
            self.yCoord.pop(0)

        #if the mean array is too large
        if (len(self.fullCoordList) > 40):
            self.fullCoordList.pop(0)


    #Adds all of the coords to the list
    def coOrdUpdates(self):
        #adds the adjusted co-ord location to the list if there isn't a copy
        if(len(self.xCoord) > 0):
            if ((self.xCoord[len(self.xCoord) - 1] != self.capture[0] + self.minXSearch) or
                (self.yCoord[len(self.yCoord) - 1] != self.capture[1] + self.minYSearch)):
                self.xCoord.append(self.capture[0] + self.minXSearch)
                self.yCoord.append(self.capture[1] + self.minYSearch)
                #adds the mean
                self.fullCoordList.append([np.mean(self.xCoord), np.mean(self.yCoord)])
        else:
            self.xCoord.append(self.capture[0] + self.minXSearch)
            self.yCoord.append(self.capture[1] + self.minYSearch)
            #adds the mean
            self.fullCoordList.append([np.mean(self.xCoord), np.mean(self.yCoord)])

    def returnLocation(self):
        if(len(self.yCoord) < 1):
            return[0,0]
        return [self.yCoord[-1], self.xCoord[-1]]

    #translates the minimap position into a score
    def locationResult(self):
        #if the car position was found and something had been added to the fullCoordList
        if(self.capture!=None and len(self.fullCoordList) > 0):
            # assumes closest is most recent, if so then give a reward
            nowDifferenceX = (self.fullCoordList[len(self.fullCoordList) - 1][0] - (self.capture[0] + self.minXSearch)) * (self.fullCoordList[len(self.fullCoordList) - 1][0] - (self.capture[0] + self.minXSearch))
            nowDifferenceY = (self.fullCoordList[len(self.fullCoordList) - 1][1] - (self.capture[1] + self.minYSearch)) * (self.fullCoordList[len(self.fullCoordList) - 1][1] - (self.capture[1] + self.minYSearch))
            nowDifference = nowDifferenceX + nowDifferenceY
            self.reward = nowDifference
            #testing if it has backtracked:
            for i in self.fullCoordList:
                #difference between now point and comparison point
                nowDifferenceX = (i[0] - (self.capture[0] + self.minXSearch)) * (i[0] - (self.capture[0] + self.minXSearch))
                nowDifferenceY = (i[1] - (self.capture[1] + self.minYSearch)) * (i[1] - (self.capture[1] + self.minYSearch))
                nowDifference = nowDifferenceX + nowDifferenceY
                #difference between previous point and comparison point
                pastDifferenceX = (i[0] - (self.fullCoordList[len(self.fullCoordList) - 1][0])) * (i[0] - (self.fullCoordList[len(self.fullCoordList) - 1][0]))
                pastDifferenceY = (i[1] - (self.fullCoordList[len(self.fullCoordList) - 1][1])) * (i[1] - (self.fullCoordList[len(self.fullCoordList) - 1][1]))
                pastDifference = pastDifferenceX + pastDifferenceY
                #if it has back tracked
                if(nowDifference < pastDifference):
                    self.reward = nowDifference - pastDifference
        else:
            self.reward = 0

    #collects the cars position and works out the
    def returnPosDifference(self):
        self.collectPos(correctDirection=True)
        self.locationResult()
        return self.reward

    #This calculates the velocity of the car
    def speedCalc(self):
        #if there is an actual check
        if(len(self.xCoord)>1):
            velocityX = math.sqrt((self.xCoord[-1] - self.xCoord[len(self.xCoord) - 2]) * (self.xCoord[-1] - self.xCoord[len(self.xCoord) - 2]))
            velocityY = math.sqrt((self.yCoord[-1] - self.yCoord[len(self.xCoord) - 2]) * (self.yCoord[-1] - self.yCoord[len(self.yCoord) - 2]))
        #no comparison
        else:
            velocityX = 0
            velocityY = 0
        Utility.addAverageSpeed(velocityY, velocityY)
        return [velocityX, velocityY]



