from scgraphics import GraphicsWindow
import sys
import random

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
HEADER_HEIGHT = 80
GAME_WND_HEIGHT = CANVAS_HEIGHT - HEADER_HEIGHT
GAME_WND_WIDTH = CANVAS_WIDTH
CENTERX = GAME_WND_WIDTH//2
CENTERY = GAME_WND_HEIGHT//2

# Create the window and access the canvas. 
win = GraphicsWindow(CANVAS_WIDTH, CANVAS_HEIGHT)
canvas = win.canvas()

# draw the spaceship
def drawShip(x, y):
    canvas.setFill('dark gray')
    canvas.setOutline('dark gray')
    canvas.drawRect(x, y, 35, 10)
    canvas.drawOval(x+30, y, 10, 10)
    canvas.drawRect(x-2, y-8, 5, 16)
    canvas.drawRect(x, y-5, 5, 10)

#draw the wall
def drawWall(x, openingY, openingHeight):
    canvas.setFill('brown')
    canvas.setOutline('black')
    canvas.drawRect(x-10, HEADER_HEIGHT, 20, GAME_WND_HEIGHT)
    canvas.setFill('white')
    canvas.setOutline('white')
    canvas.drawRect(x-10, openingY-openingHeight//2, 20, openingHeight)

#draw the header
def drawHeader(name, score, level, speed, fuel):
    canvas.setFill(40, 60, 200)
    canvas.setOutline('black')    
    canvas.drawRect(0, 0, GAME_WND_WIDTH, HEADER_HEIGHT)
    canvas.setOutline('white')
    canvas.setTextFont(family='arial', size=18, style='normal')
    canvas.drawText(20, 10, 'Name')
    canvas.drawText(20, 40, 'Level:')
    canvas.drawText(260, 10, 'Score:')
    canvas.drawText(260, 40, 'Speed:')
    canvas.drawText(500, 10, 'Fuel:')
    canvas.drawText(500, 40, 'Ship:')

    canvas.setOutline('light blue')
    canvas.drawText(120, 10, name)
    canvas.setOutline('yellow')
    canvas.drawText(120, 40, '%02d'%(level))
    canvas.drawText(360, 10, '%05d'%(score))
    canvas.drawText(360, 40, '%0.1f MPH'%(175 + speed*100.0))
    canvas.drawText(600, 10, '%0.1f%%'%(fuel))
    canvas.drawText(600, 40, '4')


def main():
    shipX = GAME_WND_WIDTH//4
    shipY = CENTERY
    wallX = float(GAME_WND_WIDTH)
    openingY = CENTERY
    nextOpeningY = CENTERY
    openingHeight = 80
    wallSpeedIncrement = 0.25
    wallSpeed = wallSpeedIncrement
    shipYspeed = 15
    fuel = 100
    fuelDecrement = 0.01
    gameOver = False
    
    while not gameOver:
        canvas.clear()
        drawHeader('Sam, I Am', 00, 1, wallSpeed, fuel)
        drawWall(int(wallX), openingY, openingHeight)
        drawShip(shipX, shipY)
        wallX -= wallSpeed
        fuel -= fuelDecrement
        if fuel < 0:
            gameOver = True
        
        if wallX <= 0:
            wallX = GAME_WND_WIDTH
            openingY = nextOpeningY
            nextOpeningY = random.randint(10+HEADER_HEIGHT+openingHeight//2, CANVAS_HEIGHT-openingHeight//2-10)
            
        key = win.GetKey()
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
            
        win.update()
    
    canvas.setOutline('black')
    canvas.setTextFont(family='arial', size=48, style='bold')
    canvas.drawText(CENTERX - 120, CENTERY, 'GAME OVER')
    win.wait()
'''
add fuel that starts at 100% and goes to 0%...game over when we reach 0.
add "warp"ing using the space bar.  This will cost 10% of the fuel.
add "lives" which will start at 5 and drop to 0 with each strike of the wall.
'''

main()