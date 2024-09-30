
import pygame
import sys
import math
from Line import *
from Circle import *

SCREEN_WIDTH = 750
SCREEN_HEIGHT = 750

pygame.init()
canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), depth = 1) 

pygame.display.set_caption("My Board") 
exit = False

clock = pygame.time.Clock()

# save any previous lines created
lines = []

# save any previous arcs created
arcs = []

# save circles
circles = []

def drawStart(end):
    pygame.draw.line(canvas, color = "red", start_pos = end, end_pos = pygame.mouse.get_pos(), width = 2)


def squareProgram():
    running = True

    canvas.fill("white")

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # line
            pygame.draw.rect(canvas, color = (162, 189, 235), rect = (10,10,60,60))
            lineFont = pygame.font.Font(None, 32)
            lineObj = lineFont.render('line', True, (30, 30, 30), None)
            canvas.blit(lineObj, (20,30))

            # circle
            pygame.draw.rect(canvas, color = (129, 235, 125), rect = (80,10,60,60))
            arcFont = pygame.font.Font(None, 25)
            arcObj = arcFont.render('circle', True, (30, 30, 30), None)
            canvas.blit(arcObj, (86,30))

            # adding X's
            pygame.draw.circle(canvas, color = "green", center = (375, 375), radius = 2)

# make circles with clicks
# Add Snaps
# Add non-editable geometry – worksheets. Look for other CAD simplifications
    # boxes and pyramids
    # other real world objects
# concrete educational objectives – measurements and designs


# Think about good first task – what are we hoping they can do
# WHAT IS GOAL?



def grid():
    blockSize = 25
    for x in range(0, SCREEN_WIDTH, blockSize):
        for y in range(0, SCREEN_HEIGHT, blockSize):
            rectGrid = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(canvas, color = "light grey", rect = rectGrid, width = 1)



canvas.fill("white")

grid()

while not exit: 
    # squareProgram()

    pygame.draw.rect(canvas, color = (162, 189, 235), rect = (10,10,60,60))
    lineFont = pygame.font.Font(None, 32)
    lineObj = lineFont.render('line', True, (30, 30, 30), None)
    canvas.blit(lineObj, (20,30))

    # arc square
    pygame.draw.rect(canvas, color = (129, 235, 125), rect = (80,10,60,60))
    arcFont = pygame.font.Font(None, 25)
    arcObj = arcFont.render('circle', True, (30, 30, 30), None)
    canvas.blit(arcObj, (86,30))
    
    for line in lines:
        pygame.draw.line(canvas, color="red", start_pos=line[0], end_pos=line[1], width=2)

    for circle in circles:
        pygame.draw.circle(canvas, color = "blue", center = circle[0], radius = circle[1], width = 2)

    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            exit = True 

        (x,y) = pygame.mouse.get_pos()
        if x >= 10 and y <= 70 and x <= 70 and y >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
            #drawLine()
            l = Line(canvas)
            l.drawLine(1)


        if x >= 80 and y <= 70 and x <= 140 and y >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
            c = Circle(canvas)
            c.drawCircle(1)
        

    pygame.display.update()  
    clock.tick(60)   

