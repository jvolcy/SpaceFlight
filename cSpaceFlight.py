from scgraphics import GraphicsWindow
import sys
import random

#scGraphics demo SlaceFlight program class
class SpaceFlight():
    '''Simple game to demonstrate use of scGraphics library.
This game is intended to be a proof of concept for an
first semester programming class.  The game makes no 
use of classes or any coding concepts that may not be
covered in a CS0 course.
scGraphics is a modification of the ezGraphics library by
Rance Necaise (http://ezgraphics.org).  Every attempt is
made to keep szGraphics backward compatible with
ezGraphics 2.1, from which it is derived.  The main
differences between sc and ez are
1)  addition of a canvas update function, update().  
update() can be used instead of wait() so that
the graphics on the canvas can be animated.  Use 
update() inside of a loop that repeatedly clears() and
redraws the canvas.
2) addition of a non-blocking key reading function,
scanKey().  Unlike getKey(), scanKey() returns the keysym
for the last key pressed.  Instead of blocking and waiting
for user input, scanKey() returns an empty string if no
key has been pressed.
3) by default, 'keypress' events are enabled

Execute the demo with the command
SpaceFlight().run()
'''    
    def __init__(self):
        # Constants
        self.CANVAS_WIDTH = 800
        self.CANVAS_HEIGHT = 600
        self.HEADER_HEIGHT = 80
        self.GAME_WND_HEIGHT = self.CANVAS_HEIGHT - self.HEADER_HEIGHT
        self.GAME_WND_WIDTH = self.CANVAS_WIDTH
        self.CENTERX = self.GAME_WND_WIDTH//2
        self.CENTERY = self.GAME_WND_HEIGHT//2
        self.WALL_WIDTH = 20
        
        # Create the window and access the canvas. 
        self.win = GraphicsWindow(self.CANVAS_WIDTH, self.CANVAS_HEIGHT)
        self.canvas = self.win.canvas()
    
    def printInstructions(self):
        instructions = '''Use the up and down arrows to move the spacecraft up and down.
    The object of the game is to navigate through each gate until your
    fuel runs out or until you have no crafts left.  On startup, your fuel
    is at 100% and you have 4 reserved crafts.  You can control the
    speed of your craft using the left and right arrows.  Your score
    increments with each gate you successfully cross.  The points 
    you accumulate is dependent on the speed at which you cross
    each gate.  Use the predictor at the upper-right to see the location
    of the next gate ahead.  You may use the spacebar to 'warp' through
    any gate.  Doing so will cost you 10% of your fuel.
    Good luck, Space Ranger!'''
        
        print('How to Play\n-----------')
        print(instructions)
        print()
        
    # draw the spaceship
    def drawShip(self, x, y):
        self.canvas.setFill('dark gray')
        self.canvas.setOutline('darkgray')
        self.canvas.drawRect(x, y, 35, 10)
        self.canvas.drawOval(x+30, y, 10, 10)
        self.canvas.drawRect(x-2, y-8, 5, 16)
        self.canvas.drawRect(x, y-5, 5, 10)
    
    #draw the wall
    def drawWall(self, x, y, width, height, openingY, openingHeight):
        self.canvas.setFill('brown')
        self.canvas.setOutline('black')
        self.canvas.drawRect(x-width//2, y, width, height)
        self.canvas.setFill('white')
        self.canvas.setOutline('white')
        self.canvas.drawRect(x-width//2, openingY-openingHeight//2, width, openingHeight)
    
    #draw the header
    def drawHeader(self, name, score, level, speed, fuel, lives):
        #draw the blue header
        self.canvas.setFill(40, 60, 200)
        self.canvas.setOutline('black')    
        self.canvas.drawRect(0, 0, self.GAME_WND_WIDTH, self.HEADER_HEIGHT)
        
        #draw the labels in white
        self.canvas.setTextFont(family='arial', size=18, style='normal')
        self.canvas.setOutline('white')
        self.canvas.drawText(20, 10, 'Name')
        self.canvas.drawText(20, 40, 'Level:')
        self.canvas.drawText(260, 10, 'Score:')
        self.canvas.drawText(260, 40, 'Speed:')
        self.canvas.drawText(500, 10, 'Fuel:')
        self.canvas.drawText(500, 40, 'Lives:')
    
        #draw the name entry in blue
        self.canvas.setOutline('light blue')
        self.canvas.drawText(120, 10, name)
        
        #draw all other entries in yellow
        self.canvas.setOutline('yellow')
        self.canvas.drawText(120, 40, '%02d'%(level))
        self.canvas.drawText(360, 10, '%05d'%(score))
        self.canvas.drawText(360, 40, '%0.1f MPH'%(175 + speed*100.0))
        self.canvas.drawText(600, 10, '%0.1f%%'%(fuel))
        self.canvas.drawText(600, 40, '%d'%(lives))
        
    #draw the predictor
    def drawPredictor(self, openingY, openingHeight):
        scale = self.HEADER_HEIGHT/self.CANVAS_HEIGHT
        openingY = int(openingY * scale)
        openingHeight = int(openingHeight * scale)
        self.drawWall(x=self.CANVAS_WIDTH - 50, y=0, width=5, height=self.HEADER_HEIGHT, openingY=openingY, openingHeight=openingHeight)
    
    #main game loop
    def run(self):
        shipX = self.GAME_WND_WIDTH//4
        shipY = self.CENTERY
        wallX = 0.0 #float(GAME_WND_WIDTH)
        openingY = self.CENTERY
        nextOpeningY = self.CENTERY
        openingHeight = 80
        wallSpeedIncrement = 0.25
        wallSpeed = wallSpeedIncrement
        shipYspeed = 15
        fuel = 100
        score = 0
        lives = 4
        fuelDecrement = 0.01
        gameOver = False
        newGate = True;
        
        #print the instructions for play
        self.printInstructions()
        
        #get the user's name
        name = input('Please enter your name: ')
        self.win.pause(1000)
        
        #enter the game loop
        while not gameOver:
            self.canvas.clear()
            self.drawHeader(name=name, score=score, level=1, speed=wallSpeed, fuel=fuel, lives=lives)
            self.drawPredictor(nextOpeningY, openingHeight)
            self.drawWall(x=int(wallX), y=self.HEADER_HEIGHT, width=self.WALL_WIDTH, height=self.GAME_WND_HEIGHT, openingY=openingY, openingHeight=openingHeight)
            self.drawShip(shipX, shipY)
            wallX -= wallSpeed
            fuel -= fuelDecrement
            if fuel < 0:
                gameOver = True
            
            if wallX <= 0:
                wallX = self.GAME_WND_WIDTH
                openingY = nextOpeningY
                nextOpeningY = random.randint(10+self.HEADER_HEIGHT+openingHeight//2, self.CANVAS_HEIGHT-openingHeight//2-10)
                newGate = True
            
            if wallX < shipX and newGate == True:
                newGate = False
                #check if we have a collision
                if shipY < openingY-openingHeight//2 or shipY > openingY+openingHeight//2:
                    lives -= 1
                    if lives == 0:
                        gameOver = True
                        
                    self.canvas.setFill('red')
                    self.canvas.drawOval(shipX-50, shipY-50, 100, 100)
                    self.win.pause(1000)
                else:
                    score += wallSpeed * 1000
                    
            #process user key inputs
            key = self.win.scanKey()
            if key == 'q' or key == 'Q':
                self.win.quit()
                sys.exit()
            elif key == 'Up':
                shipY -= shipYspeed
                if shipY < self.HEADER_HEIGHT:
                    shipY = self.HEADER_HEIGHT
            elif key == 'Down':
                shipY += shipYspeed
                if shipY > self.CANVAS_HEIGHT:
                    shipY = self.CANVAS_HEIGHT
            elif key == 'Right':
                wallSpeed  += wallSpeedIncrement
            elif key == 'Left':
                wallSpeed -= wallSpeedIncrement
                if wallSpeed < wallSpeedIncrement:
                    wallSpeed = wallSpeedIncrement
            elif key == 'space':     #warp
                shipY = openingY
                fuel -= 10.0
                
            self.win.update()
        
        #print a 'Game Over' message and quit
        self.canvas.setOutline('black')
        self.canvas.setTextFont(family='arial', size=48, style='bold')
        self.canvas.drawText(self.CENTERX - 120, self.CENTERY, 'GAME OVER')
        self.win.wait()

#scGraphics
#function to launch scGraphics "SpaceFlight" demo program
def demo():
    SpaceFlight().run()




demo()