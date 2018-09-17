from scgraphics import GraphicsWindow
import sys
import random

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
'''

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
HEADER_HEIGHT = 80
GAME_WND_HEIGHT = CANVAS_HEIGHT - HEADER_HEIGHT
GAME_WND_WIDTH = CANVAS_WIDTH
CENTERX = GAME_WND_WIDTH//2
CENTERY = GAME_WND_HEIGHT//2
WALL_WIDTH = 20

# Create the window and access the canvas. 
win = GraphicsWindow(CANVAS_WIDTH, CANVAS_HEIGHT)
canvas = win.canvas()

def printInstructions():
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
def drawShip(x, y):
    canvas.setFill('dark gray')
    canvas.setOutline('darkgray')
    canvas.drawRect(x, y, 35, 10)
    canvas.drawOval(x+30, y, 10, 10)
    canvas.drawRect(x-2, y-8, 5, 16)
    canvas.drawRect(x, y-5, 5, 10)

#draw the wall
def drawWall(x, y, width, height, openingY, openingHeight):
    canvas.setFill('brown')
    canvas.setOutline('black')
    canvas.drawRect(x-width//2, y, width, height)
    canvas.setFill('white')
    canvas.setOutline('white')
    canvas.drawRect(x-width//2, openingY-openingHeight//2, width, openingHeight)

#draw the header
def drawHeader(name, score, level, speed, fuel, lives):
    #draw the blue header
    canvas.setFill(40, 60, 200)
    canvas.setOutline('black')    
    canvas.drawRect(0, 0, GAME_WND_WIDTH, HEADER_HEIGHT)
    
    #draw the labels in white
    canvas.setTextFont(family='arial', size=18, style='normal')
    canvas.setOutline('white')
    canvas.drawText(20, 10, 'Name')
    canvas.drawText(20, 40, 'Level:')
    canvas.drawText(260, 10, 'Score:')
    canvas.drawText(260, 40, 'Speed:')
    canvas.drawText(500, 10, 'Fuel:')
    canvas.drawText(500, 40, 'Lives:')

    #draw the name entry in blue
    canvas.setOutline('light blue')
    canvas.drawText(120, 10, name)
    
    #draw all other entries in yellow
    canvas.setOutline('yellow')
    canvas.drawText(120, 40, '%02d'%(level))
    canvas.drawText(360, 10, '%05d'%(score))
    canvas.drawText(360, 40, '%0.1f MPH'%(175 + speed*100.0))
    canvas.drawText(600, 10, '%0.1f%%'%(fuel))
    canvas.drawText(600, 40, '%d'%(lives))
    
#draw the predictor
def drawPredictor(openingY, openingHeight):
    scale = HEADER_HEIGHT/CANVAS_HEIGHT
    openingY = int(openingY * scale)
    openingHeight = int(openingHeight * scale)
    drawWall(x=CANVAS_WIDTH - 50, y=0, width=5, height=HEADER_HEIGHT, openingY=openingY, openingHeight=openingHeight)

#main game loop
def main():
    shipX = GAME_WND_WIDTH//4
    shipY = CENTERY
    wallX = 0.0 #float(GAME_WND_WIDTH)
    openingY = CENTERY
    nextOpeningY = CENTERY
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
    printInstructions()
    
    #get the user's name
    #name = input('Please enter your name: ')
    name = 'None'
    win.pause(1000)
    
    #enter the game loop
    while not gameOver:
        canvas.clear()
        drawHeader(name=name, score=score, level=1, speed=wallSpeed, fuel=fuel, lives=lives)
        drawPredictor(nextOpeningY, openingHeight)
        drawWall(x=int(wallX), y=HEADER_HEIGHT, width=WALL_WIDTH, height=GAME_WND_HEIGHT, openingY=openingY, openingHeight=openingHeight)
        drawShip(shipX, shipY)
        wallX -= wallSpeed
        fuel -= fuelDecrement
        if fuel < 0:
            gameOver = True
        
        if wallX <= 0:
            wallX = GAME_WND_WIDTH
            openingY = nextOpeningY
            nextOpeningY = random.randint(10+HEADER_HEIGHT+openingHeight//2, CANVAS_HEIGHT-openingHeight//2-10)
            newGate = True
        
        if wallX < shipX and newGate == True:
            newGate = False
            #check if we have a collision
            if shipY < openingY-openingHeight//2 or shipY > openingY+openingHeight//2:
                lives -= 1
                if lives == 0:
                    gameOver = True
                    
                canvas.setFill('red')
                canvas.drawOval(shipX-50, shipY-50, 100, 100)
                win.pause(1000)
            else:
                score += wallSpeed * 1000
                
        #process user key inputs
        key = win.scanKey()
        if key == 'q' or key == 'Q':
            win.quit()
            sys.exit()
        elif key == 'Up':
            shipY -= shipYspeed
            if shipY < HEADER_HEIGHT:
                shipY = HEADER_HEIGHT
        elif key == 'Down':
            shipY += shipYspeed
            if shipY > CANVAS_HEIGHT:
                shipY = CANVAS_HEIGHT
        elif key == 'Right':
            wallSpeed  += wallSpeedIncrement
        elif key == 'Left':
            wallSpeed -= wallSpeedIncrement
            if wallSpeed < wallSpeedIncrement:
                wallSpeed = wallSpeedIncrement
        elif key == 'space':     #warp
            shipY = openingY
            fuel -= 10.0
            
        win.update()
    
    #print a 'Game Over' message and quit
    canvas.setOutline('black')
    canvas.setTextFont(family='arial', size=48, style='bold')
    canvas.drawText(CENTERX - 120, CENTERY, 'GAME OVER')
    win.wait()


#call main()
main()
