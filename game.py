import os, time, random, keyboard

def play(username, highscore):
    gameHandler = GameHandler(username, highscore)
    gameHandler.play()

class GameHandler():
    def __init__(self, username, highscore):
        self.username = username
        self.highscore = highscore
        self.score = 0
        self.lives = 3
        self.aliensKilled = 0
        self.shotsFired = 0
        self.alienDirection = "Left"
        self.rowToMove = 0
        self.alienMovementBuffer = 0
        self.alienFireBuffer = 0
        self.lastAlienFired = None
        self.mysteryShipSpawnBuffer = 0
        self.mysteryShipMovementBuffer = 0

    #PLAY THE GAME, Play The Game, play the game.....
    def play(self):
        self.initGame()
        self.game()

    #INITIALISE THE GAME VARIABLES/OBJECTS
    def initGame(self):
        #SCREEN INITIALISATION
        self.screen = Screen()
        self.screen.initScreen()
        
        #PLAYER, ALIENS, BASES AND BULLETS
        self.player = Player(self.screen)
        self.genAliens()
        self.genBases()
        self.playerBullet = Bullet(0,0,"player")
        self.alienBullets = [Bullet(0,0,"alien"), Bullet(0,0,"alien"), Bullet(0,0,"alien")]


    ########THE GAME########
    def game(self):
        while True:
            if self.player.status == "Alive":
                    
                #GENERATE MYSTERY SHIP
                self.genMysteryShip()

                #MOVE BULLETS
                #PLAYER
                if self.playerBullet.status == "Alive":
                    self.playerBullet.move(self.screen)
                #ALIEN
                for i in self.alienBullets:
                    if i.status == "Alive":
                        i.move(self.screen)

                #MOVE ALIENS
                self.moveAliens()

                #MOVE MYSTERY SHIP
                self.moveMysteryShip()

                #FIRE ALIEN BULLETS
                self.genAlienBullets()
                
                #CHECK FOR KEYBOARD INPUTS
                self.getInput()

                #CHECK FOR COLLISIONS
                self.getCollisions()

                self.endGameCheck()

            #CHECK IF IS TIME FOR PLAYER TO BE REVIVED
            else:
                self.player.reviveCheck(self.screen)

            #PRINT ONTO SCREEN
            self.printScreen()


    #GENERATE THE ALIENS
    def genAliens(self):
        self.aliens = []
        columnGap = (self.screen.width - 30) / 12 
        rowGap = 4       #2D array, columns then rows   0  1  2  3  4  5  6  7  8  9  10
        for i in range(11):#                            11 12 13 14 15 16 17 18 19 20 21    etc.
            self.aliens.append([])
            for j in range(5):
                if j == 0:
                    self.aliens[i].append(Alien(((i + 1) * int(columnGap)) + (i * 3), (j + 1) * rowGap + 5, "al1"))
                elif j == 1 or j == 2:
                    self.aliens[i].append(Alien(((i + 1) * int(columnGap)) + (i * 3), (j + 1) * rowGap + 5, "al2"))
                else:
                    self.aliens[i].append(Alien(((i + 1) * int(columnGap)) + (i * 3), (j + 1) * rowGap + 5, "al3"))
        
        self.mysteryShip = Alien(self.screen.width, 5, "mys")
    
    #GENERATE ALIEN BULLETS
    def genAlienBullets(self):
        if time.time() > self.alienFireBuffer:
            #CHECK IF THERE IS AN AVAILABLE ALIEN BULLET
            bulletAvailable = False
            bulletFiring = None
            for i in self.alienBullets:
                if i.status == "Dead" and not bulletAvailable:
                    bulletAvailable = True
                    bulletFiring = i
            #FIRE A BULLET
            if bulletAvailable:
                #PICK RANDOM column
                valid = False
                while not valid:
                    column = random.randint(0,10)
                    #VERIFY THERE IS AN ALIVE ALIEN IN THAT COLUMN
                    if self.lastAlienFired != column:
                        for i in self.aliens[column]:
                            if i.status == "Alive":
                                valid = True
                #FIND FRONTMOST ALIEN
                alienShooting = None
                columnFound = False
                for i in range(4,-1,-1):
                    if columnFound == False and self.aliens[column][i].status == "Alive":
                        columnFound = True
                        alienShooting = self.aliens[column][i]
                        self.lastAlienFired = i
                #FIRE BULLET
                bulletFiring.fire(alienShooting)
                self.alienFireBuffer = time.time() + 0.7

    #MYSTERY SHIP GENERATION
    def genMysteryShip(self):
        if self.mysteryShipSpawnBuffer < time.time():
            ranNum = random.randint(1,450)
            if ranNum == 8 and self.mysteryShip.status == "Dead":
                self.mysteryShip.spawnMysShip(self.screen)
            self.mysteryShipSpawnBuffer = time.time() + 0.02

    #GENERATE THE BASES
    def genBases(self):
        self.bases = [Base(0), Base(1), Base(2), Base(3)]
        for i in self.bases:
            i.populate(self.screen)

    #GET KEYBOARD INPUTS
    def getInput(self):
        if keyboard.is_pressed("a"):
            self.player.move("Left")
        elif keyboard.is_pressed("d"):
            self.player.move("Right")
        elif keyboard.is_pressed(" "):
            if self.playerBullet.status == "Dead":
                self.playerBullet.fire(self.player)

    #GET COLLISIONS
    def getCollisions(self):
        ##PLAYER BULLET##
        #WITH BASES
        if self.playerBullet.status == "Alive":
            for base in self.bases:
                for componant in base.componants:
                    if self.playerBullet.status == "Alive":
                        if(int(self.playerBullet.y) == int(componant.y)) and (int(self.playerBullet.x) == int(componant.x) or int(self.playerBullet.x) == int(componant.x + 1)) and componant.status == "Alive":
                            self.playerBullet.status = "Dead"
                            componant.shot()

        #WITH ALIENS
        if self.playerBullet.status == "Alive":
            for columnIndx in range(len(self.aliens)):
                for alienIndx in range(len(self.aliens[columnIndx])):
                    if (self.playerBullet.x >= self.aliens[columnIndx][alienIndx].x and self.playerBullet.x <= self.aliens[columnIndx][alienIndx].x + 2) and (self.playerBullet.y <= self.aliens[columnIndx][alienIndx].y and self.playerBullet.y >=  self.aliens[columnIndx][alienIndx].y - 3) and self.aliens[columnIndx][alienIndx].status == "Alive":
                        self.playerBullet.status = "Dead"
                        self.aliens[columnIndx][alienIndx].status = "Dead"
                        if alienIndx == 0:
                            self.score += 30
                        elif alienIndx == 1 or alienIndx == 2:
                            self.score += 20
                        elif alienIndx == 3 or alienIndx == 4:
                            self.score += 10
        
        ##ALIEN BULLETS##
        #WITH BASES
        for bullet in self.alienBullets:
            if bullet.status == "Alive":
                for base in self.bases:
                    for componant in base.componants:
                        if(int(bullet.y) == int(componant.y)) and (int(bullet.x) == int(componant.x) or int(bullet.x) == int(componant.x + 1)) and componant.status == "Alive":
                               bullet.status = "Dead"
                               componant.shot()

        #WITH PLAYER
        for bullet in self.alienBullets:
            if bullet.status == "Alive":
                if (int(bullet.x) == int(self.player.x) or int(bullet.x) == int(self.player.x + 1) or int(bullet.x) == int(self.player.x + 2)) and (int(bullet.y) == int(self.player.y) or int(bullet.y) == int(self.player.y - 1)):
                    self.player.kill(self)
                    bullet.status = "Dead"
        
        #WITH PLAYERBULLET
        if self.playerBullet.status == "Alive":
            for bullet in self.alienBullets:
                if bullet.status == "Alive":
                    if int(bullet.x) == int(self.playerBullet.x) and int(bullet.y) == int(self.playerBullet.y):
                        bullet.status = "Dead"
                        self.playerBullet.status = "Dead"

    #MOVE ALIENS
    def moveAliens(self):
        if self.alienMovementBuffer < time.time():

            if self.rowToMove == 0:
                moveDown = False
                for column in self.aliens:
                    for alien in column:
                        if alien.status == "Alive" and alien.x == 1 and self.alienDirection == "Left":
                            moveDown = True
                            self.alienDirection = "Right"
                        elif alien.status == "Alive" and alien.x == self.screen.width - 4 and self.alienDirection == "Right":
                            moveDown = True
                            self.alienDirection = "Left"
                if moveDown:
                    for i in self.aliens:
                        for j in i:
                            j.y += 1
           
            #HORISONTAL
            for i in self.aliens:
                i[self.rowToMove].move(self.alienDirection)
            #INCREMENT ROWTOMOVE
            self.rowToMove += 1
            if self.rowToMove == 5:
                self.rowToMove = 0    

            self.alienMovementBuffer = time.time() + 0.25              

    #MOVE MYSTERY SHIP
    def moveMysteryShip(self):
        if self.mysteryShip.x < 0:
            self.mysteryShip.status = "Dead"
            
        if self.mysteryShip.status == "Alive":
            if self.mysteryShipMovementBuffer < time.time():
                self.mysteryShip.x -= 1
                self.mysteryShipMovementBuffer = time.time() + 0.04
        
    #CHECK ENG GAME CONDITIONS
    def endGameCheck(self):
        ending = True
        reason = ""
        for i in self.aliens:
            for j in i:
                if j.status == "Alive":
                    ending = False
                    reason = "win"
                    if j.y == self.screen.height - 1:
                        ending = True
                        reason = "reachBottom"
        if self.lives == 0:
            ending = True
            reason = "shot"

        if ending:
            self.endGame(reason)

    #DISPLAY THE SCREEN
    def printScreen(self):

        if self.screen.displayBuffer < time.time():
            #WIPE
            self.screen.wipe()
            #PLAYER
            self.screen = self.player.plot(self.screen)
            #ALIENS
            for i in self.aliens:
                for j in i:
                    if j.status == "Alive":
                        self.screen = j.plot(self.screen)
            #MYSTERY SHIP
            if self.mysteryShip.status == "Alive":
                self.mysteryShip.plot(self.screen)
            #BULLETS
            if self.playerBullet.status == "Alive":
                self.screen = self.playerBullet.plot(self.screen)
            for i in self.alienBullets:
                if i.status == "Alive":
                    self.screen = i.plot(self.screen)
            #BASES
            for i in self.bases:
                for j in i.componants:
                    self.screen = j.plot(self.screen)
            #DISPLAY
            self.screen.display(self)
            #FRAMERATE BUFFER
            self.screen.displayBuffer = time.time() + 0.03

    #END THE GAME
    def endGame(self, reason):
        time.sleep(1)
        os.system("cls")
        #GAME OVER MESSAGES
        if reason == "shot" or reason == "reachBottom":
            print("YOU LOSE")
        else:
            print("YOU WIN")

        #LOAD LOGINS DATA
        import json
        with open("Logins.json", "r") as file:
            data = json.load(file)
        
        #LOCATE INDEX OF USER IN LOGINS FILE
        userIndx = -1
        found = False
        for user in data["logins"]:
            if not found:
                userIndx += 1
                if user["Username"] == self.username:
                    found = True
        
        #CHECK FOR NEW HIGHSCORE
        if data["logins"][userIndx]["Highscore"] < self.score:
            print("NEW HIGHSCORE")
            data["logins"][userIndx]["Highscore"] = self.score
            with open("Logins.json", "w") as file:
                json.dump(data, file, indent = 4)
                        
        else:
            print("NO NEW HIGHSCORE, BETTER LUCK NEXT TIME")
            print("YOUR HIGHSCORE IS ", data["logins"][userIndx]["Highscore"])

        print(f"YOUR SCORE WAS {self.score}")

        time.sleep(2)
        
        quit()




class Screen():
    def __init__(self):
        self.width, self.height = os.get_terminal_size()
        self.height = 36
        self.displayBuffer = 0
        self.screenArray = []

    def initScreen(self):
        for i in range(self.height):
            self.screenArray.append([])
            for j in range(self.width):
                self.screenArray[i].append(" ")

    def wipe(self):
        for i in range(len(self.screenArray)):
            for j in range(len(self.screenArray[i])):
                self.screenArray[i][j] = " "
    
    def display(self, gameHandler):
        os.system("cls")
        print("SPACE INVADERS")
        print(f"YOU ARE LOGGED IN AS {gameHandler.username}")
        print(f"YOUR HIGHSCORE IS: {gameHandler.highscore}          YOUR SCORE IS: {gameHandler.score}")
        if gameHandler.lives == 1:
            print(f"YOU HAVE 1 LIFE REAMINING")
        else:
            print(f"YOU HAVE {gameHandler.lives} LIVES REAMINING")
        for i in self.screenArray:
            line = ""
            for j in i:
                line += j
            print(line)


class Player():
    def __init__(self, screen):
        self.x = (screen.width/2) - 1
        self.y = screen.height
        self.movementBuffer = 0
        self.status = "Alive"
        self.deadBuffer = 0

        #    _
        #   |_|

    def spawn(self, screen):
        self.x = (screen.width/2) - 1
        self.y = screen.height
        self.movementBuffer = 0
        self.status = "Alive"

    def move(self, direction):
        if time.time() >= self.movementBuffer:
            if direction == "Left": 
                self.x -= 1
            else:
                self.x += 1
            self.movementBuffer = time.time() + 0.04

    def kill(self, gameHandler):
        self.status = "Dead"
        self.deadBuffer = time.time() + 2
        gameHandler.lives -= 1

    def reviveCheck(self, screen):
        if time.time() > self.deadBuffer:
            self.spawn(screen)

    def plot(self, screen):
        self.x = int(self.x)
        self.y = int(self.y)
        if self.status == "Alive":
            screen.screenArray[int(self.y - 2)][int(self.x)] = "_"
            screen.screenArray[self.y - 1][self.x - 1] = "|"
            screen.screenArray[self.y - 1][self.x] = "_"
            screen.screenArray[self.y - 1][self.x + 1] = "|"
        else:
            screen.screenArray[self.y - 1][self.x - 1] = "\\"
            screen.screenArray[self.y - 1][self.x] = "_"
            screen.screenArray[self.y - 1][self.x + 1] = "/"
        return screen
        

class Alien():
    def __init__(self, x, y, alType):
        self.x = x
        self.y = y
        self.type = alType #types are al1 al2 al3 and mys
        if alType == "mys":
            self.status = "Dead"
        else:
            self.status = "Alive"
        
    #           /^\           /^\           \^/                 /--\
    #   type 1  {%}   type 2  \|/   type 3  (%)   mystery ship  \--/
    #           \_/           <|>           /|\

    def move(self, direction):
        if direction == "Left":
            self.x -= 1
        else:
            self.x += 1

        if self.type == "mys" and self.x < 0:
            self.status = "Dead"

    def plot(self, screen):
        self.x = int(self.x)
        self.y = int(self.y)
        if self.type == "al1":
            screen.screenArray[self.y - 3][self.x - 1], screen.screenArray[self.y - 3][self.x], screen.screenArray[self.y - 3][self.x + 1] =  "/", "^", "\\"
            screen.screenArray[self.y - 2][self.x - 1], screen.screenArray[self.y - 2][self.x], screen.screenArray[self.y - 2][self.x + 1] =  "{", "%", "}"
            screen.screenArray[self.y - 1][self.x - 1], screen.screenArray[self.y - 1][self.x], screen.screenArray[self.y - 1][self.x + 1] = "\\", "_", "/"
        elif self.type == "al2":
            screen.screenArray[self.y - 3][self.x - 1], screen.screenArray[self.y - 3][self.x], screen.screenArray[self.y - 3][self.x + 1] =  "/", "^", "\\"
            screen.screenArray[self.y - 2][self.x - 1], screen.screenArray[self.y - 2][self.x], screen.screenArray[self.y - 2][self.x + 1] = "\\", "|", "/"
            screen.screenArray[self.y - 1][self.x - 1], screen.screenArray[self.y - 1][self.x], screen.screenArray[self.y - 1][self.x + 1] = "<", "|", ">"
        elif self.type == "al3":
            screen.screenArray[self.y - 3][self.x - 1], screen.screenArray[self.y - 3][self.x], screen.screenArray[self.y - 3][self.x + 1] = "\\", "^", "/"
            screen.screenArray[self.y - 2][self.x - 1], screen.screenArray[self.y - 2][self.x], screen.screenArray[self.y - 2][self.x + 1] =  "(", "%", ")"
            screen.screenArray[self.y - 1][self.x - 1], screen.screenArray[self.y - 1][self.x], screen.screenArray[self.y - 1][self.x + 1] =  "/", "|", "\\"
        else:
            screen.screenArray[self.y - 2][self.x - 1], screen.screenArray[self.y - 2][self.x], screen.screenArray[self.y - 2][self.x + 1], screen.screenArray[self.y - 2][self.x + 2] =  "/", "-", "-", "\\"
            screen.screenArray[self.y - 1][self.x - 1], screen.screenArray[self.y - 1][self.x], screen.screenArray[self.y - 1][self.x + 1], screen.screenArray[self.y - 1][self.x + 2] = "\\", "-", "-","/"
        
        return screen
    
    def spawnMysShip(self, screen):
        self.x = screen.width - 4
        self.status = "Alive"


class Bullet():
    def __init__(self, x, y, bulType):
        self.x = x
        self.y = y
        self.type = bulType
        self.status = "Dead"
        self.fireBuffer = 0
        self.movementBuffer = 0
    
    def fire(self, firer):
        if self.fireBuffer < time.time():
            self.status = "Alive"
            self.x = firer.x + 1
            self.y = firer.y

    def move(self, screen):
        if self.movementBuffer < time.time():
            if self.type == "player":
                self.y -= 1
            else:
                self.y += 1
        
        if self.y < 1 or self.y > screen.height:
            self.status = "Dead"

        self.movementBuffer = time.time() + 0.005
    
    def plot(self, screen):
        self.x = int(self.x)
        self.y = int(self.y)
        screen.screenArray[self.y - 1][self.x - 1] = "|"
        return screen


class Base():
    def __init__(self, baseNo):
        self.baseNo = baseNo
        self.componants = []

    #           ########       XXXXXXXX       /\///\\/
    #           ########       XXXXXXXX       \\\\/\/\
    #           ##    ##       XX    XX       /\    //

    def populate(self, screen):
        offset = ((self.baseNo + 1) * ((screen.width - 32) / 5)) + (self.baseNo * 8)#baseGap + basesBefore

        self.componants.append(BaseComp(offset, 33))
        self.componants.append(BaseComp(offset + 6, 33))
        self.componants.append(BaseComp(offset, 32))
        self.componants.append(BaseComp(offset + 2, 32))
        self.componants.append(BaseComp(offset + 4, 32))
        self.componants.append(BaseComp(offset + 6, 32))
        self.componants.append(BaseComp(offset, 31))
        self.componants.append(BaseComp(offset + 2, 31))
        self.componants.append(BaseComp(offset + 4, 31))
        self.componants.append(BaseComp(offset + 6, 31))


class BaseComp():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.timesShot = 0
        self.appearance = "#"
        self.status = "Alive"
    
    def shot(self):
        if self.status == "Alive":
            self.timesShot += 1
            if self.timesShot == 1:
                self.appearance = "x"
            if self.timesShot == 2:
                rN = random.randint(1,2)
                if rN == 1:
                    self.appearance = "\\"
                else:
                    self.appearance = "/"
            if self.timesShot == 3:
                self.status = "Dead"
    
    def plot(self, screen):
        if self.status == "Alive":
            self.x = int(self.x)
            self.y = int(self.y)
            screen.screenArray[self.y - 1][self.x - 1], screen.screenArray[self.y - 1][self.x] = self.appearance, self.appearance

        return screen
