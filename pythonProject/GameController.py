import pyautogui, time

#Reset method, takes the game from the finished screen to the main menu then calls the load game function
def reset():
    print("doing a reset")
    time.sleep(1)
    #Looks for the finish screen
    resultsLoaded = False
    while(resultsLoaded!=True):
        if pyautogui.locateOnScreen(r"F:\3rd Year Project\Important Screenshots\gameFinish.png", confidence=0.99) != None:
            resultsLoaded = True

    #Keyboard inputs to get back to the main menu
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.moveTo(400, 450)

    #Loads the game
    loadGame()

#Goes back to the main menu by clicking quit
def backToMenu():

    #Presses quit on the racing screen
    time.sleep(1)
    print("going back to the menu")
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(3)

    #Goes to the quit section of the game
    pyautogui.press('right')
    time.sleep(0.5)
    pyautogui.press('right')
    time.sleep(0.5)
    pyautogui.press('right')
    time.sleep(0.5)
    pyautogui.press('right')
    time.sleep(0.5)
    pyautogui.press('right')
    time.sleep(0.5)
    pyautogui.press('enter')
    time.sleep(1)

    #Moves the mouse (to remove interfering by hovering over)
    pyautogui.moveTo(400, 450)
    time.sleep(5)
    loadGame()

#Puts all of the keys up
def offKeys():
    pyautogui.keyUp("up")
    pyautogui.keyUp("left")
    pyautogui.keyUp("right")
    pyautogui.keyUp("down")

#Restarts the race track (race to race)
def restart():
    time.sleep(1)
    pyautogui.press('esc')
    time.sleep(1)
    pyautogui.press('down')
    time.sleep(1)
    pyautogui.press('enter')
    time.sleep(7)

#Loads the game
def loadGame():
    print("loading game")
    time.sleep(1)

    #Sets up attributes for menu navigation
    transitionInt = 1
    menuNav = True
    car1 = True
    car2 = True
    trackSelect = True
    settings1 = True
    settings2 = True

    while (menuNav):
        # Setting up
        if pyautogui.locateCenterOnScreen(
                r"F:\3rd Year Project\Important Screenshots\GameSetUp\P" + str(transitionInt) + ".jpg",
                confidence=0.9) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen(
                r"F:\3rd Year Project\Important Screenshots\GameSetUp\P" + str(transitionInt) + ".jpg", confidence=0.9))
            pyautogui.press('enter')
            transitionInt = transitionInt + 1
            time.sleep(1)
            pyautogui.moveTo(1800, 450)
        if transitionInt == 4:
            menuNav = False

    # Car1 selection
    time.sleep(2)
    pyautogui.press('up')
    while (car1):
        if pyautogui.locateCenterOnScreen(r"F:\3rd Year Project\Important Screenshots\GameSetUp\P4.jpg",
                                          confidence=0.9) != None:
            car1 = False
        else:
            pyautogui.press('left')
    time.sleep(2)
    pyautogui.press('w')

    # Car2 selection
    while (car2):
        if pyautogui.locateCenterOnScreen(r"F:\3rd Year Project\Important Screenshots\GameSetUp\P5.jpg",
                                          confidence=0.9) != None:
            pyautogui.press('enter')
            car2 = False
        else:
            pyautogui.press('d')

    transitionInt = 6
    time.sleep(1)
    # Selecting the track
    while (trackSelect):
        # Setting up
        if pyautogui.locateCenterOnScreen(
                r"F:\3rd Year Project\Important Screenshots\GameSetUp\P" + str(transitionInt) + ".jpg",
                confidence=0.9) != None:
            pyautogui.moveTo(pyautogui.locateCenterOnScreen(
                r"F:\3rd Year Project\Important Screenshots\GameSetUp\P" + str(transitionInt) + ".jpg", confidence=0.9))
            pyautogui.press('enter')
            transitionInt = transitionInt + 1
            time.sleep(1)
        if transitionInt == 9:
            trackSelect = False
            time.sleep(1)

    # Goes to the top of the settings
    time.sleep(1)
    pyautogui.press('up')
    time.sleep(1)
    pyautogui.press('up')
    time.sleep(1)
    pyautogui.press('up')
    time.sleep(1)
    pyautogui.press('up')
    time.sleep(1)
    pyautogui.press('up')

    #Makes sure of the settings on 1 page are correct
    while (settings1):
        if pyautogui.locateCenterOnScreen(
                r"F:\3rd Year Project\Important Screenshots\GameSetUp\P" + str(transitionInt) + ".jpg",
                confidence=0.95) != None:
            transitionInt = transitionInt + 1
            pyautogui.press('down')
            time.sleep(1)
        else:
            pyautogui.press('left')
            time.sleep(1)
        if transitionInt == 14:
            settings1 = False
    pyautogui.press('enter')

    #Goes to the top of settings screen 2
    time.sleep(1)
    pyautogui.press('up')
    time.sleep(1)
    pyautogui.press('up')
    time.sleep(1)
    pyautogui.press('up')
    time.sleep(1)
    pyautogui.press('up')
    time.sleep(1)
    pyautogui.press('up')
    time.sleep(1)

    # Makes sure of the settings on page 2 are correct
    while (settings2):
        if pyautogui.locateCenterOnScreen(
                r"F:\3rd Year Project\Important Screenshots\GameSetUp\P" + str(transitionInt) + ".jpg",
                confidence=0.95) != None:
            transitionInt = transitionInt + 1
            pyautogui.press('down')
            time.sleep(1)
        else:
            time.sleep(1)
            if transitionInt == 18:
                pyautogui.press('right')
            else:
                pyautogui.press('left')
        if transitionInt == 19:
            settings2 = False

    #Enters into the racing game
    pyautogui.press('enter')
    time.sleep(5)

#Presses a key based on the action given
def stepKeyPress (action):

    # Reset the key presses
    pyautogui.keyUp("up", _pause=False)
    pyautogui.keyUp("left", _pause=False)
    pyautogui.keyUp("right", _pause=False)
    pyautogui.keyUp("down", _pause=False)

    # Pressing the corresponding key to the action
    if (action - 8 > -1):
        action = action - 8
        pyautogui.keyDown("up", _pause=False)
    if (action - 4 > -1):
        action = action - 4
        pyautogui.keyDown("left", _pause=False)
    if (action - 2 > -1):
        action = action - 2
        pyautogui.keyDown("right", _pause=False)
    if (action - 1 > -1):
        pyautogui.keyDown("right", _pause=False)
