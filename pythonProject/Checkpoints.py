class CheckPointCalc():

    #checkpoint consists of min and max of line as well as axis on and how you pass it
    #x or y for set axis and + or - for if it needs to decrease or increase over
    #note is + actualy means go down or right
    def __init__(self, checkpointList):
        self.checkpoints = checkpointList
        self.checkpointsPassed = 0

    def reset(self):
        self.checkpointsPassed = 0

    #coOrd should be passed in Y X
    #is current is true if it hasn't passed and  false otherwise
    #Example = [bound1, bound2, staticCoOrd, "y+"] and coOrd is [y, x]
    #x = horizontal line, y = veritcal line
    def checkPassed(self, coOrd, checkPointInt, isCurrent):

        #This is the non cross over int (y if x)
        self.inRangeInt = 0
        #must pass line (if x must be x)
        self.tickOverInt = 0

        if ((self.checkpoints[checkPointInt][3] == "x+") or (self.checkpoints[checkPointInt][3] =="x-")):
            self.tickOverInt = coOrd[0]
            self.inRangeInt = coOrd[1]
        #This is the y+ or y-
        else:
            self.tickOverInt = coOrd[1]
            self.inRangeInt = coOrd[0]
        #print("in range int:", self.inRangeInt, " tick over int:", self.tickOverInt)


        #If its in range of the 2 co-ords
        if self.checkpoints[checkPointInt][1] >= self.inRangeInt >= self.checkpoints[checkPointInt][0]:

            #if its passing over = true or checking if it back tracked a negative
            if (self.checkpoints[checkPointInt][3] == "x+") or (self.checkpoints[checkPointInt][3] == "y+"):
                if isCurrent == True:
                    # if its passed the bounds
                    if self.tickOverInt >= self.checkpoints[checkPointInt][2]:
                        return True
                else:
                    #if its going back and hasn't passed the bounds
                    if self.tickOverInt < self.checkpoints[checkPointInt][2]:
                        return True

            else:
                if isCurrent == False:
                    # if its passed the bounds
                    if self.tickOverInt >= self.checkpoints[checkPointInt][2]:
                        return True
                else:
                    #if its going back and hasn't passed the bounds
                    if self.tickOverInt < self.checkpoints[checkPointInt][2]:
                        return True

        #default return false
        return False

    #Main method to be called
    def updateCheckPointsPassed(self, coOrd):
        #count for increasing or decreasing
        count = 0
        #if its passed the next checkpoint, increase the count
        print(self.checkpointsPassed, " ", len(self.checkpoints))
        if self.checkpointsPassed < len(self.checkpoints):
            if(self.checkPassed(coOrd, self.checkpointsPassed, True)):
                count = 1
                self.checkpointsPassed = self.checkpointsPassed + 1
        #otherwise
        elif(self.checkpointsPassed > 0):
            #if it hasn't passed the old checkpoint
            if (self.checkPassed(coOrd, self.checkpointsPassed - 1, False)):
                count = -1
                self.checkpointsPassed = self.checkpointsPassed - 1
        #print("the count is ", self.checkpointsPassed)
        return count

