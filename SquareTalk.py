import pygame
import sys
import math
from Line import *
from Circle import *

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750

(centerScreenX, centerScreenY) = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

pygame.init()
canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), depth = 1) 

pygame.display.set_caption("My Board") 
exit = False

clock = pygame.time.Clock()

# save any previous lines created
lines = []

# save circles
circles = []

# clear all
canvas.fill("white")

#make Grid
def grid():
    blockSize = 25
    for x in range(0, SCREEN_WIDTH, blockSize):
        for y in range(0, SCREEN_HEIGHT, blockSize):
            rectGrid = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(canvas, color = "light grey", rect = rectGrid, width = 1)

grid()


#drawing markers's

boxWidth = 200
offset = boxWidth / 2
wallWidth = 50

pygame.draw.circle(canvas, color = "black", center = (centerScreenX, centerScreenY), radius = 4)

#outside
pygame.draw.circle(canvas, color = "red", center = (centerScreenX - boxWidth, centerScreenY - boxWidth), radius = 4)
pygame.draw.circle(canvas, color = "red", center = (centerScreenX - boxWidth, centerScreenY + boxWidth), radius = 4)
pygame.draw.circle(canvas, color = "red", center = (centerScreenX + boxWidth, centerScreenY - boxWidth), radius = 4)
pygame.draw.circle(canvas, color = "red", center = (centerScreenX + boxWidth, centerScreenY + boxWidth), radius = 4)

#inside
pygame.draw.circle(canvas, color = "dark green", center = (centerScreenX - (boxWidth + wallWidth), centerScreenY - (boxWidth + wallWidth)), radius = 4)
pygame.draw.circle(canvas, color = "dark green", center = (centerScreenX - (boxWidth + wallWidth), centerScreenY + (boxWidth + wallWidth)), radius = 4)
pygame.draw.circle(canvas, color = "dark green", center = (centerScreenX + (boxWidth + wallWidth), centerScreenY - (boxWidth + wallWidth)), radius = 4)
pygame.draw.circle(canvas, color = "dark green", center = (centerScreenX + (boxWidth + wallWidth), centerScreenY + (boxWidth + wallWidth)), radius = 4)

while not exit: 
    # squareProgram()

    pygame.draw.rect(canvas, color = (162, 189, 235), rect = (10,10,60,60))
    lineFont = pygame.font.Font(None, 32)
    lineObj = lineFont.render('line', True, (30, 30, 30), None)
    canvas.blit(lineObj, (20,30))

    # arc square
    pygame.draw.rect(canvas, color = (129, 235, 125), rect = (80,10,60,60))
    arcFont = pygame.font.Font(None, 25)
    circleObj = arcFont.render('circle', True, (30, 30, 30), None)
    canvas.blit(circleObj, (86,30))

    # legend 
    pygame.draw.rect(canvas, color = (0, 0, 0), rect = (800,10,120,90), width = 2)
    legendFont = pygame.font.Font(None, 32)
    legendObj = legendFont.render('Legend:', True, (30, 30, 30), None)
    outsideFont = pygame.font.Font(None, 25)
    outsideObj = outsideFont.render('= outside', True, (30, 30, 30), None)
    insideFont = pygame.font.Font(None, 25)
    insideObj = insideFont.render('= inside', True, (30, 30, 30), None)
    canvas.blit(legendObj, (820, 20))
    canvas.blit(outsideObj, (830, 50))
    canvas.blit(insideObj, (830, 70))
    pygame.draw.circle(canvas, color = "dark green", center = (815, 55), radius = 7)
    pygame.draw.circle(canvas, color = "red", center = (815, 80), radius = 7)
    
    
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
            l = Line(canvas, boxWidth, (centerScreenX, centerScreenY), wallWidth)
            l.drawLine(2)

        if x >= 80 and y <= 70 and x <= 140 and y >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
            c = Circle(canvas)
            c.drawCircle()


    pygame.display.update()  
    clock.tick(60)  