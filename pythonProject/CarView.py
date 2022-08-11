import pyautogui
from PIL import ImageGrab
import cv2
import Utility
import numpy as np

class CarView():

    #Initialisation done to keep track of relivant Coords
    def __init__(self):
        self.resetPos()

    #sets all of the coords to their relivant position
    def resetPos(self):
        self.xCoord = 0
        self.yCoord = 0
        # most recent xCoords
        self.lastSeenX = 0
        self.lastSeenY = 0

    def updateCoOrds(self):
        # last seen pos of the text on the screen
        self.lastSeenX = self.location[0] + self.minXSearch
        self.lastSeenY = self.location[1] + self.minYSearch
        # Move X and Y to correct pos relitive to car title
        self.xCoord = int(self.lastSeenX - 130)
        self.yCoord = int(self.lastSeenY - 70)
        # makes sure the bounds aren't irrational
        if (self.xCoord < 0):
            self.xCoord = 0
        if (self.yCoord < 0):
            self.yCoord = 0

    def getView(self):
        # Tries the first search with restricted parameters
        # Finds the restricted boundary co-ords
        self.minXSearch, self.minYSearch, self.maxXSearch, self.maxYSearch = Utility.screenshotBoundary(self.lastSeenX, self.lastSeenY, 90, [25,7])
        # takes a simplified screenshot where the car likely will be
        self.captureSimplified = ImageGrab.grab(bbox=(self.minXSearch, self.minYSearch, self.maxXSearch, self.maxYSearch))
        # an overall capture of the image
        self.captureOverall = ImageGrab.grab(bbox=(0, 0, 960, 1080))
        # tries to find the car on the simplified screenshot
        self.location = pyautogui.locate(r"F:\3rd Year Project\Important Screenshots\identifier.png", self.captureSimplified,  confidence=0.7)
        # If it finds a capture
        if(self.location!=None):
            # Adds to statistics
            Utility.storeCaptureAccuracy(1, "carView")
            # Updates co-ords (finds actual car pos)
            self.updateCoOrds()
        # if it can't find it on the restricted version, try the derestricted version
        else:
            # changes the co-ords to the default search that will cover everything
            self.minXSearch, self.minYSearch, self.maxXSearch, self.maxYSearch = 0, 0, 1080, 960
            self.location = pyautogui.locate(r"F:\3rd Year Project\Important Screenshots\identifier.png", self.captureOverall, confidence=0.7)
            # If it finds a capture
            if (self.location != None):
                # Adds to statistics
                Utility.storeCaptureAccuracy(2, "carView")
                # Updates co-ords (finds actual car pos)
                self.updateCoOrds()
            # if it fails to find the image
            else:
                # Adds to statistics
                Utility.storeCaptureAccuracy(3, "carView")

        #This line screenshots the car area, then performs edge detection on it
        self.carViewForWalls = np.array(cv2.Canny(np.array(ImageGrab.grab(bbox=(self.xCoord + 3, self.yCoord - 22, self.xCoord + 283, self.yCoord + 258))), 40, 255)).astype('float32')
        self.carViewEdge = np.array(ImageGrab.grab(bbox=(self.xCoord + 118, self.yCoord + 93, self.xCoord + 168, self.yCoord + 143)))
        #Covert car location and have rays comming out of it
        return self.carViewEdge

    #Calculates the distance between the car and the walls
    def getDistanceFromWalls(self):
        #rules for wall definition:
        #goes y by x
        #values are 280 x 280 with a 25x25 chunk that needs to be taken out

        #Casting
        self.found = [False, False, False, False]
        self.distances = [115, 115, 115, 115]

        self.width = 3
        self.additional = 2
        self.cutOff = 70

        #cast 1 and 2
        for z in range(114, self.additional + 1, -1):
            self.ray1Array = []
            self.ray2Array = []
            for additionalZ in range(0, self.additional + 1):
                for widthAdditional in range(-1, self.width):
                    self.ray1Array.append(self.carViewForWalls[138+widthAdditional][z+additionalZ])
                    self.ray2Array.append(self.carViewForWalls[z+additionalZ][138+widthAdditional])

            if(np.mean(self.ray1Array) > self.cutOff and self.found[0] is False):
                self.found[0] = True
                self.distances[0] = 114 - z

            if (np.mean(self.ray2Array) > self.cutOff and self.found[1] is False):
                self.found[1] = True
                self.distances[1] = 114 - z

        # casting 3 and 4
        for z in range(165, 277, 1):
            self.ray3Array = []
            self.ray4Array = []
            for additionalZ in range(0, self.additional + 1):
                for widthAdditional in range(-1, self.width):
                    self.ray3Array.append(self.carViewForWalls[138 + widthAdditional][z + additionalZ])
                    self.ray4Array.append(self.carViewForWalls[z + additionalZ][138 + widthAdditional])

            if (np.mean(self.ray3Array) > self.cutOff and self.found[2] is False):
                self.found[2] = True
                self.distances[2] = z - 165

            if (np.mean(self.ray4Array) > self.cutOff and self.found[3] is False):
                self.found[3] = True
                self.distances[3] = z - 165

        self.distanceReward = sum(self.distances)

        return self.distances, self.distanceReward



