# 1280x720 RESOLUTION
#REFERENCES
#BACKGROUNDS https://craftpix.net/freebies/free-cartoon-forest-game-backgrounds/
#CHARACTER SPRTIE https://craftpix.net/freebies/free-3-cyberpunk-characters-pixel-art/
from tkinter import *
import time

#Movement Controls
def keyPress(event):
    if event.char == "p":
        global paused
        if paused == False:
            pauseGame()
        else:
            unpauseGame()
    if event.char =="b":                #Bosskey
        global bossKeyBG
        if paused == False:
            pauseGame()
            bossKeyBG = game_Map.create_image( 0, 0, image = bossKeyIMG, anchor = "nw")
        elif paused == True:
            game_Map.delete(bossKeyBG)
            unpauseGame()
    if event.char == "c":
        global score
        score = score + 100
        textLabel = "Score:" + str(score)
        game_Map.itemconfigure(scoreText, text=textLabel)        
    if paused == True:
        return
    else:
        file = open("controls.txt","r")
        controlsRead = file.readlines()
        file.close()
        if controlsRead[3][0] == "/":
            moveLeftControl = controlsRead[0][0]
        else:
            moveLeftControl = controlsRead[3][0]
        if controlsRead[3][0] == "/":
            moveRightControl = controlsRead[1][0]
        else:
            moveRightControl = controlsRead[4][0]
        if controlsRead[3][0] == "/":
            shootControl = controlsRead[2][0]
        else:
            shootControl = controlsRead[5][0]
        if event.char == moveLeftControl:
            game_Map.move(mainCharacter, -15, 0) 
        if event.char == moveRightControl:    
            game_Map.move(mainCharacter, +15, 0)     
        if event.char == shootControl:
            generateShot()

def checkNameBox(event):
    global nameEntry,enterNameButton,enterNameText,score
    if entryBox.get() != "":
        name = entryBox.get()    
        file = open("scoreSave.txt","a")
        file.write(str(score) + "," + name + "\n")
        file.close()    
        startButton = game_Map.create_rectangle(550,500,730,550, fill = "#9D9896")
        startText = game_Map.create_text(640,525, text = "RETURN TO MAIN MENU")
        game_Map.delete(enterNameButton,enterNameText,nameEntry)
        game_Map.tag_bind(startButton, "<Button-1>", mainMenuLoad)
        game_Map.tag_bind(startText, "<Button-1>", mainMenuLoad)
        score = 0
    else:
        return

def startClicked(event):
    drawGame()
def scoreboardClicked(event):
    scoreboardWindow()
def loadClicked(event):
    selectLoadProfile()
def controlsClicked(event):
    controlsWindow()
def mainMenuLoad(event):
    mainWindow()

def showProfiles(event):
    selectProfile()
def chooseProfile1(event):
    saveGame("save1.txt")
def chooseProfile2(event):
    saveGame("save2.txt")
def chooseProfile3(event):
    saveGame("save3.txt") 
def chooseLoadProfile1(event):
    loadGame("save1.txt")     
def chooseLoadProfile2(event):
    loadGame("save2.txt") 
def chooseLoadProfile3(event): 
    loadGame("save3.txt")

def changeLeft(event):
    changeControl("left")
def changeRight(event):
    changeControl("right")
def changeShoot(event):
    changeControl("shoot")
def saveControlL(event):
    saveControl("left")
def saveControlR(event):
    saveControl("right")
def saveControlS(event):
    saveControl("shoot")
def resetButtons(event):
    resetControls()    

def overlapping(a,b):
    if a[0] < b[2] and a[2] > b[0] and a[1] < b[3] and a[3] > b[1]:
        return True
    return False

def generateShot():    
    playerCoords = game_Map.coords(mainCharacter)
    bullets.append(game_Map.create_rectangle(playerCoords[0] + 5, playerCoords[1] + 5,playerCoords[0] - 4,playerCoords[1] - 4, fill = "red"))

def moveShapes():
    global bullets
    global score
    global shapes
    speed = 1
    removed = False
    gameOver = False
    shapePosition = []
    while gameOver == False and paused == False:
        if shapes == []:
            addShapesToBoard()
            if speed < 7:
                speed = speed + 1        
        game_Map.after(100)
        for i in range(len(shapes)):        #moves the shapes list
            game_Map.move(shapes[i], 0, +speed)
        if bullets != []:                   #moves bullets that are in the list
            bulletCoords = game_Map.coords(bullets[0])        
            for i in range(len(bullets)):            
                game_Map.move(bullets[i], 0, -12)
                bulletCoords.clear()
                bulletCoords = game_Map.coords(bullets[i])
            for i in range(len(shapes)):
                squareCheck = game_Map.coords(shapes[i])
                for j in range(len(bullets)):
                    bulletCheck = game_Map.coords(bullets[j])
                    if overlapping(squareCheck,bulletCheck):
                        game_Map.delete(bullets[j])     #removes bullets when collision occurs
                        game_Map.delete(shapes[i])
                        shapes.remove(shapes[i])
                        bullets.remove(bullets[j])
                        removed = True
                        break
                if removed == True:
                    removed = False
                    score = score + 1               #Update score system
                    textLabel = "Score:" + str(score)
                    game_Map.itemconfigure(scoreText, text=textLabel)
                    break
        if shapes != []:
            shapePosition.append(game_Map.coords(shapes[0]))           
            if shapePosition[0][1] > 720:       #ends game if shapes reach the other side
                gameOver = True                      
        shapePosition.clear()       
        game_Map.update()
    if gameOver == True:
       gameOverWindow()

      
#Draw Shapes To Spawn
def addShapesToBoard():
    global shapes 
    shapes.append(game_Map.create_rectangle(265, 50, 315, 100, fill = "white"))
    shapes.append(game_Map.create_rectangle(365, 50, 415, 100, fill = "white"))
    shapes.append(game_Map.create_rectangle(465, 50, 515, 100, fill = "white"))
    shapes.append(game_Map.create_rectangle(565, 50, 615, 100, fill = "white"))
    shapes.append(game_Map.create_rectangle(665, 50, 715, 100, fill = "white"))
    shapes.append(game_Map.create_rectangle(765, 50, 815, 100, fill = "white"))
    shapes.append(game_Map.create_rectangle(865, 50, 915, 100, fill = "white"))
    shapes.append(game_Map.create_rectangle(965, 50, 1015, 100, fill = "white"))
       
#Draw Player + Background
def drawGame():
    global scoreText,mainCharacter,textLabel
    game_Map.delete("all")
    gameMapBackground = game_Map.create_image( 0, 0, image = backgroundIMG, anchor = "nw")
    textLabel = "Score:" + str(score)
    scoreText = game_Map.create_text( width-80 , 20 , fill="darkblue" , font="Times 20 italic bold", text=textLabel)
    mainCharX = 640    #Draw Player
    mainCharY = 682
    mainCharacter = game_Map.create_image(mainCharX, mainCharY, image = mainCharacterIMG, anchor = "nw")
    game_Window.bind("<Key>", keyPress)
    game_Window.focus_set()
    addShapesToBoard()
    moveShapes()

#Draws main window
def mainWindow():
    game_Map.delete("all")
    global paused
    paused = False
    gameMapBackground = game_Map.create_image( 0, 0, image = mainPageIMG, anchor = "nw")
    mainGameText = game_Map.create_text(640,125, text = "SQUARE GAME", font = "Oswald 100 bold", fill = "#C29D12")
    startButton = game_Map.create_rectangle(550,300,730,350, fill = "#9D9896")
    startText = game_Map.create_text(640,325, text = "NEW GAME")
    loadButton = game_Map.create_rectangle(550,400,730,450, fill = "#9D9896")
    loadText = game_Map.create_text(640,425, text = "LOAD GAME")
    scoreboardButton = game_Map.create_rectangle(550,500,730,550, fill = "#9D9896")
    scoreboardText = game_Map.create_text(640,525, text = "SCOREBOARD")
    controlsButton = game_Map.create_rectangle(550,600,730,650, fill = "#9D9896")
    controlsText = game_Map.create_text(640,625, text = "CONTROLS")
    game_Map.tag_bind(startButton, "<Button-1>", startClicked)
    game_Map.tag_bind(startText, "<Button-1>", startClicked)
    game_Map.tag_bind(loadButton, "<Button-1>", loadClicked)
    game_Map.tag_bind(loadText, "<Button-1>", loadClicked)
    game_Map.tag_bind(scoreboardButton, "<Button-1>", scoreboardClicked)
    game_Map.tag_bind(scoreboardText, "<Button-1>", scoreboardClicked)
    game_Map.tag_bind(controlsButton, "<Button-1>", controlsClicked)
    game_Map.tag_bind(controlsText, "<Button-1>", controlsClicked)   

#Generate the leaderboard
def scoreboardWindow():
    game_Map.delete("all")
    gameMapBackground = game_Map.create_image( 0, 0, image = leaderboardIMG, anchor = "nw")
    leaderboardText = game_Map.create_text(640,125, text = "SCOREBOARD", font = "Oswald 70 bold", fill = "#C29D12")
    startButton = game_Map.create_rectangle(1100,670,1280,720, fill = "#9D9896")
    startText = game_Map.create_text(1190,695, text = "MAIN MENU")
    game_Map.tag_bind(startButton, "<Button-1>", mainMenuLoad)
    game_Map.tag_bind(startText, "<Button-1>", mainMenuLoad)
    file = open("scoreSave.txt", "r")
    scoreList = []
    for line in file:
        scoreLine = line.strip()
        scoreList.append(scoreLine.split(","))
    file.close()
    orderedScores = sorted(scoreList, key = lambda x:-int(x[0]))
    score1Text = game_Map.create_text(640,225, text = "1. " + orderedScores[0][1] + "   " + orderedScores[0][0], font = "Oswald 50 bold", fill = "#0AD55F")
    score2Text = game_Map.create_text(640,325, text = "2. " + orderedScores[1][1] + "   " + orderedScores[1][0], font = "Oswald 50 bold", fill = "#0AD55F")
    score3Text = game_Map.create_text(640,425, text = "3. " + orderedScores[2][1] + "   " + orderedScores[2][0], font = "Oswald 50 bold", fill = "#0AD55F")
    score4Text = game_Map.create_text(640,525, text = "4. " + orderedScores[3][1] + "   " + orderedScores[3][0], font = "Oswald 50 bold", fill = "#0AD55F")
    score5Text = game_Map.create_text(640,625, text = "5. " + orderedScores[4][1] + "   " + orderedScores[4][0], font = "Oswald 50 bold", fill = "#0AD55F")

def controlsWindow():
    global changeLButton,changeLText,changeRButton,changeRText,changeSButton,changeSText,currentMoveLeft,currentMoveRight,currentshootText
    game_Map.delete("all")
    file = open("controls.txt","r")
    controlsRead = file.readlines()
    file.close()
    if controlsRead[3][0] == "/":
        moveLeftControl = controlsRead[0]
    else:
        moveLeftControl = controlsRead[3]
    if controlsRead[4][0] == "/":
        moveRightControl = controlsRead[1]
    else:
        moveRightControl = controlsRead[4]
    if controlsRead[5][0] == "/":
        shootControl = controlsRead[2]
    else:
        shootControl = controlsRead[5]
    gameMapBackground = game_Map.create_image( 0, 0, image = leaderboardIMG, anchor = "nw")
    leaderboardText = game_Map.create_text(640,125, text = "CONTROLS", font = "Oswald 70 bold", fill = "#C29D12")
    startButton = game_Map.create_rectangle(1100,670,1280,720, fill = "#9D9896")
    startText = game_Map.create_text(1190,695, text = "MAIN MENU")
    moveLeftText = game_Map.create_text(200,300, text = "MOVE LEFT",font = "Oswald 20 bold", fill = "White")
    moveRightText = game_Map.create_text(200,400, text = "MOVE RIGHT",font = "Oswald 20 bold", fill = "White")
    shootText = game_Map.create_text(200,500, text = "SHOOT",font = "Oswald 20 bold", fill = "White")
    currentMoveLeft = game_Map.create_text(500,320, text = moveLeftControl,font = "Oswald 20 bold", fill = "White")
    currentMoveRight = game_Map.create_text(500,420, text = moveRightControl,font = "Oswald 20 bold", fill = "White")
    currentshootText = game_Map.create_text(500,520, text = shootControl,font = "Oswald 20 bold", fill = "White")
    changeLButton = game_Map.create_rectangle(810,275,980,325, fill = "#9D9896")
    changeLText = game_Map.create_text(900,300, text = "CHANGE LEFT")
    changeRButton = game_Map.create_rectangle(810,375,980,425, fill = "#9D9896")
    changeRText = game_Map.create_text(900,400, text = "CHANGE RIGHT")
    changeSButton = game_Map.create_rectangle(810,475,980,525, fill = "#9D9896")
    changeSText = game_Map.create_text(900,500, text = "CHANGE SHOOT")
    resetButton = game_Map.create_rectangle(810,575,980,625, fill = "#9D9896")
    resetText = game_Map.create_text(900,600, text = "RESET CONTROLS")
    game_Map.tag_bind(startButton, "<Button-1>", mainMenuLoad)
    game_Map.tag_bind(startText, "<Button-1>", mainMenuLoad)
    game_Map.tag_bind(changeLText, "<Button-1>", changeLeft)
    game_Map.tag_bind(changeLButton, "<Button-1>", changeLeft)
    game_Map.tag_bind(changeRText, "<Button-1>", changeRight)
    game_Map.tag_bind(changeRButton, "<Button-1>", changeRight)
    game_Map.tag_bind(changeSText, "<Button-1>", changeShoot)
    game_Map.tag_bind(changeSButton, "<Button-1>", changeShoot)
    game_Map.tag_bind(resetButton, "<Button-1>", resetButtons)
    game_Map.tag_bind(resetText, "<Button-1>", resetButtons)

def changeControl(control):
    global changeLButton,changeLText,changeRButton,changeRText,changeSButton,changeSText,LEntry,REntry,SEntry

    if control == "left":
        game_Map.delete(changeLButton,changeLText)
        saveLeft = game_Map.create_rectangle(810,275,980,325, fill = "#9D9896")
        saveLeftText = game_Map.create_text(900,300, text = "SAVE LEFT")
        LEntry = game_Map.create_window(650, 300, window=moveLeftEntry)
        game_Map.tag_bind(saveLeft, "<Button-1>", saveControlL)
        game_Map.tag_bind(saveLeftText, "<Button-1>", saveControlL)
    elif control =="right":
        game_Map.delete(changeRButton,changeRText)
        saveRight = game_Map.create_rectangle(810,375,980,425, fill = "#9D9896")
        saveRightText = game_Map.create_text(900,400, text = "SAVE RIGHT")
        REntry = game_Map.create_window(650, 400, window=moveRightEntry)
        game_Map.tag_bind(saveRight, "<Button-1>", saveControlR)
        game_Map.tag_bind(saveRightText, "<Button-1>", saveControlR)
    else:
        game_Map.delete(changeSButton,changeSText)
        saveShoot = game_Map.create_rectangle(810,475,980,525, fill = "#9D9896")
        saveShootText = game_Map.create_text(900,500, text = "SAVE SHOOT")
        SEntry = game_Map.create_window(650, 500, window=shootEntry)
        game_Map.tag_bind(saveShoot, "<Button-1>", saveControlS)
        game_Map.tag_bind(saveShootText, "<Button-1>", saveControlS)

def saveControl(control):
    global changeLButton,changeLText,changeRButton,changeRText,changeSButton,changeSText,LEntry,REntry,SEntry,currentMoveLeft,currentMoveRight,currentshootText
    if control == "left":
        if len(moveLeftEntry.get())>1 or len(moveLeftEntry.get()) == 0 or moveLeftEntry.get() == "b" or moveLeftEntry.get() == "c":
            errorEntry = game_Map.create_text(width/2,height/2,fill="white",font="Oswald 20 bold", text="ENTER ONE CHAR")
            game_Map.update()
            game_Map.after(1000)
            game_Map.delete(errorEntry)
        else:
            file = open("controls.txt","r")
            controlsRead = file.readlines()
            file.close()
            controlsRead[3] = moveLeftEntry.get() + "\n"
            file = open("controls.txt","w")
            for i in range(len(controlsRead)):
                file.write(controlsRead[i])
            file.close()
            game_Map.delete(changeLButton,changeLText,LEntry)
            changeLButton = game_Map.create_rectangle(810,275,980,325, fill = "#9D9896")
            changeLText = game_Map.create_text(900,300, text = "CHANGE LEFT")
            game_Map.itemconfigure(currentMoveLeft, text=controlsRead[3])
            game_Map.tag_bind(changeLText, "<Button-1>", changeLeft)
            game_Map.tag_bind(changeLButton, "<Button-1>", changeLeft)

    elif control == "right":
        if len(moveRightEntry.get())>1 or len(moveRightEntry.get()) == 0 or moveRightEntry.get() == "b" or moveRightEntry.get() == "c":
            errorEntry = game_Map.create_text(width/2,height/2,fill="white",font="Oswald 20 bold", text="ENTER ONE CHAR")
            game_Map.update()
            game_Map.after(1000)
            game_Map.delete(errorEntry)
        else:
            file = open("controls.txt","r")
            controlsRead = file.readlines()
            file.close()
            controlsRead[4] = moveRightEntry.get() + "\n"
            file = open("controls.txt","w")
            for i in range(len(controlsRead)):
                file.write(controlsRead[i])
            file.close()
            game_Map.delete(changeRButton,changeRText,REntry)
            changeRButton = game_Map.create_rectangle(810,375,980,425, fill = "#9D9896")
            changeRText = game_Map.create_text(900,400, text = "CHANGE RIGHT")
            game_Map.itemconfigure(currentMoveRight, text=controlsRead[4])
            game_Map.tag_bind(changeRText, "<Button-1>", changeRight)
            game_Map.tag_bind(changeRButton, "<Button-1>", changeRight)
    else:
        if len(shootEntry.get())>1 or len(shootEntry.get()) == 0 or shootEntry.get() == "b" or shootEntry.get() == "c":
            errorEntry = game_Map.create_text(width/2,height/2,fill="white",font="Oswald 20 bold", text="ENTER ONE CHAR")
            game_Map.update()
            game_Map.after(1000)
            game_Map.delete(errorEntry)
        else:
            file = open("controls.txt","r")
            controlsRead = file.readlines()
            file.close()
            controlsRead[5] = shootEntry.get() + "\n"
            file = open("controls.txt","w")
            for i in range(len(controlsRead)):
                file.write(controlsRead[i])
            file.close()
            game_Map.delete(changeSButton,changeSText,SEntry)
            changeSButton = game_Map.create_rectangle(810,475,980,525, fill = "#9D9896")
            changeSText = game_Map.create_text(900,500, text = "CHANGE SHOOT")
            game_Map.itemconfigure(currentshootText, text=controlsRead[5])
            game_Map.tag_bind(changeSText, "<Button-1>", changeShoot)
            game_Map.tag_bind(changeSButton, "<Button-1>", changeShoot)

def resetControls():
    global currentMoveLeft,currentMoveRight,currentshootText
    file = open("controls.txt","r")
    controlsRead = file.readlines()
    file.close()
    controlsRead[3] = "/\n"    
    controlsRead[4] = "/\n"
    controlsRead[5] = "/\n"
    file = open("controls.txt","w")
    for i in range(len(controlsRead)):
        file.write(controlsRead[i])
    file.close()
    game_Map.itemconfigure(currentMoveLeft, text="a")   
    game_Map.itemconfigure(currentMoveRight, text="d")
    game_Map.itemconfigure(currentshootText, text="j") 

def selectProfile():
    game_Map.delete("all")
    gameMapBackground = game_Map.create_image( 0, 0, image = backgroundIMG, anchor = "nw")
    prof1Button = game_Map.create_rectangle(550,200,730,250, fill = "#9D9896")
    prof1Text = game_Map.create_text(640,225, text = "SAVE 1")
    prof2Button = game_Map.create_rectangle(550,350,730,400, fill = "#9D9896")
    prof2Text = game_Map.create_text(640,375, text = "SAVE 2")
    prof3Button = game_Map.create_rectangle(550,500,730,550, fill = "#9D9896")
    prof3Text = game_Map.create_text(640,525, text = "SAVE 3")
    game_Map.tag_bind(prof1Button, "<Button-1>", chooseProfile1)
    game_Map.tag_bind(prof1Text, "<Button-1>", chooseProfile1)
    game_Map.tag_bind(prof2Button, "<Button-1>", chooseProfile2)
    game_Map.tag_bind(prof2Text, "<Button-1>", chooseProfile2)
    game_Map.tag_bind(prof3Button, "<Button-1>", chooseProfile3)
    game_Map.tag_bind(prof3Text, "<Button-1>", chooseProfile3)

def selectLoadProfile():
    game_Map.delete("all")
    gameMapBackground = game_Map.create_image( 0, 0, image = mainPageIMG, anchor = "nw")
    prof1Button = game_Map.create_rectangle(550,200,730,250, fill = "#9D9896")
    prof1Text = game_Map.create_text(640,225, text = "SAVE 1")
    prof2Button = game_Map.create_rectangle(550,350,730,400, fill = "#9D9896")
    prof2Text = game_Map.create_text(640,375, text = "SAVE 2")
    prof3Button = game_Map.create_rectangle(550,500,730,550, fill = "#9D9896")
    prof3Text = game_Map.create_text(640,525, text = "SAVE 3")
    game_Map.tag_bind(prof1Button, "<Button-1>", chooseLoadProfile1)
    game_Map.tag_bind(prof1Text, "<Button-1>", chooseLoadProfile1)
    game_Map.tag_bind(prof2Button, "<Button-1>", chooseLoadProfile2)
    game_Map.tag_bind(prof2Text, "<Button-1>", chooseLoadProfile2)
    game_Map.tag_bind(prof3Button, "<Button-1>", chooseLoadProfile3)
    game_Map.tag_bind(prof3Text, "<Button-1>", chooseLoadProfile3)

def saveGame(file):
    global saveShapeCoords,score,saveCharacterCoords,saveScore,bullets
    file = open(file,"w")
    file.write(str(saveCharacterCoords) + "\n")
    file.write(str(saveScore) + "\n")
    for i in saveShapeCoords:
        file.write((str(i))+"\n")
    file.close()
    bullets = []
    shapes.clear()
    mainWindow()

def loadGame(file):
    global scoreText,textLabel,mainCharacter,score,shapes
    file = open(file,"r")
    saveData = file.readlines()
    score = int(saveData[1])
    mainCharacterCoords = saveData[0]
    mainCharacterCoords.replace(" ","")
    firstDone = False
    mainCharacterX = ""
    mainCharacterY = ""
    game_Map.delete("all")    
    gameMapBackground = game_Map.create_image( 0, 0, image = backgroundIMG, anchor = "nw")
    textLabel = "Score:" + str(score)
    scoreText = game_Map.create_text( width-80 , 30 , fill="darkblue" , font="Times 20 italic bold", text=textLabel)
    for i in range(1,len(mainCharacterCoords)-2):
        if mainCharacterCoords[i] != "," and firstDone == False:
            mainCharacterX = mainCharacterX + mainCharacterCoords[i]
        elif firstDone == True and mainCharacterCoords[i] != " ":
            mainCharacterY = mainCharacterY + mainCharacterCoords[i]
        else:
            firstDone = True
    mainCharacter = game_Map.create_image(float(mainCharacterX), float(mainCharacterY), image = mainCharacterIMG, anchor = "nw")    
    for i in range(2,len(saveData)):
        coordNO = 0
        squareTLXPosition = ""
        squareBRXPosition = ""
        squareTLYPosition = ""
        squareBRYPosition = ""
        tempString = saveData[i]
        for j in range(1,len(tempString)-2):
            if tempString[j] == ",":
                coordNO = coordNO + 1
            if tempString[j] != "," and tempString[j] != " " and coordNO == 0:
                squareTLXPosition = squareTLXPosition + tempString[j]
            elif coordNO == 1 and coordNO != " " and tempString[j] != "," and tempString[j] != " ":
                squareTLYPosition = squareTLYPosition + tempString[j]
            elif coordNO == 2 and coordNO != " " and tempString[j] != "," and tempString[j] != " ":
                squareBRXPosition = squareBRXPosition + tempString[j]
            elif tempString[j] != "," and tempString[j] != " ":
                squareBRYPosition = squareBRYPosition + tempString[j]
        shapes.append(game_Map.create_rectangle(float(squareTLXPosition),float(squareTLYPosition),float(squareBRXPosition),float(squareBRYPosition), fill = "white"))        
    game_Window.bind("<Key>", keyPress)
    game_Window.focus_set()
    moveShapes()    


#Position Game Window
def setGameDimensions(Width,Height):
    window = Tk() 
    window.title("Game") 
    screenWidth = window.winfo_screenwidth() 
    screenHeight = window.winfo_screenheight()
    x = (screenWidth/2) - (Width/2) 
    y = (screenHeight/2) - (Height/2)
    window.geometry('%dx%d+%d+%d' % (Width, Height, x, y))
    return window

#Pause and Unpause game
def pauseGame():
    global paused,pauseText,saveOption,saveText,saveShapeCoords,saveCharacterCoords,saveScore,score
    paused = True
    pauseText = game_Map.create_text(width/2,height/2,fill="yellow",font="Oswald 20 bold", text="PAUSED")
    saveOption = game_Map.create_rectangle(550,450,730,500, fill = "#9D9896")
    saveText = game_Map.create_text(640,475, text = "SAVE AND RETURN \n TO MAIN MENU")
    saveShapeCoords = []
    for i in range(len(shapes)):
        saveShapeCoords.append(game_Map.coords(shapes[i]))
    saveCharacterCoords = game_Map.coords(mainCharacter)
    saveScore = score
    game_Map.tag_bind(saveOption, "<Button-1>", showProfiles)
    game_Map.tag_bind(saveText, "<Button-1>", showProfiles)

def unpauseGame():
    global paused
    game_Map.delete(pauseText,saveOption,saveText)
    paused = False
    moveShapes()

#GameOver Window
def gameOverWindow():
    global score,shapes,nameEntry,enterNameText,enterNameButton
    shapes.clear()
    bullets.clear()
    game_Map.delete("all")
    game_Map.configure(background = "black")
    game_Map.create_text(width/2,height/2,fill="white",font="Oswald 20 bold", text="Game Over!")       
    enterNameButton = game_Map.create_rectangle(450,500,630,550, fill = "#9D9896")
    enterNameText = game_Map.create_text(540,525, text = "SAVE SCORE")
    nameEntry = game_Map.create_window(750, 525, window=entryBox)
    scoreText = game_Map.create_text(640,425, text = "SCORE: " + str(score), fill = "white", font = "Oswald 15 bold")
    game_Map.tag_bind(enterNameButton, "<Button-1>", checkNameBox)
    game_Map.tag_bind(enterNameText, "<Button-1>", checkNameBox)


#Draw Window
width = 1280
height = 720
score = 0
paused = False
bullets= []
shapes = []
game_Window = setGameDimensions(width,height)
game_Map = Canvas(game_Window, width=width, height=height, bg = "white")
game_Map.pack()
mainPageIMG = PhotoImage(file = "game_Images/mainPage_BG.png")    #create all images to be used
backgroundIMG = PhotoImage(file = "game_Images/game_BG.png")    
mainCharacterIMG = PhotoImage(file = "game_Images/move_Idle.png")
leaderboardIMG = PhotoImage(file = "game_Images/leaderboard_BG.png")
bossKeyIMG = PhotoImage(file = "game_Images/bossKey.png")
entryBox = Entry(game_Window)
moveRightEntry = Entry(game_Window)
moveLeftEntry = Entry(game_Window)
shootEntry = Entry(game_Window)
#drawGame()
mainWindow()
game_Window.mainloop()
