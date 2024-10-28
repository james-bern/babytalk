# TODO: numpy 2D arrays might be useful?

import pygame
import sys
import os
import math

pygame.init()
os.system('clear')

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
(centerScreenX, centerScreenY) = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
boxWidth = 100
wallWidth = 50



########################################

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
clock = pygame.time.Clock()
event_queue = None

########################################
def grid():
    blockSize = 25
    for x in range(0, SCREEN_WIDTH, blockSize):
        for y in range(0, SCREEN_HEIGHT, blockSize):
            rectGrid = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(canvas, color = "light grey", rect = rectGrid, width = 1)



########################################

def beginFrame():
    global event_queue

    pygame.display.update()
    clock.tick(60)  
    canvas.fill("WHITE")

    event_queue = []
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            return False
        else:
            event_queue.append(event)
    return True


########################################

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

########################################

class Circle:
    def __init__(self, p1, r):
        self.p1 = p1
        self.r = r
        
########################################

lines = []
linesDict = {}
circles = []

########################################

def anchorSquare(point):
    (x,y) = point

        #inside square
    if x > (centerScreenX - (boxWidth + 25)) and x < (centerScreenX - (boxWidth - 25)) and y > (centerScreenY - (boxWidth + 25)) and y < (centerScreenY - (boxWidth - 25)):
        x = (centerScreenX - boxWidth)
        y = (centerScreenY - boxWidth)
    if x > (centerScreenX - (boxWidth + 25)) and x < (centerScreenX - (boxWidth - 25)) and y > (centerScreenY + (boxWidth - 25)) and y < (centerScreenY + (boxWidth + 25)):
        x = (centerScreenX - boxWidth)
        y = (centerScreenY + boxWidth)
    if x > (centerScreenX + (boxWidth - 25)) and x < (centerScreenX + (boxWidth + 25)) and y > (centerScreenY - (boxWidth + 25)) and y < (centerScreenY - (boxWidth - 25)):
        x = (centerScreenX + boxWidth)
        y = (centerScreenY - boxWidth)
    if x > (centerScreenX + (boxWidth - 25)) and x < (centerScreenX + (boxWidth + 25)) and y > (centerScreenY + (boxWidth - 25)) and y < (centerScreenY + (boxWidth + 25)):
        x = (centerScreenX + boxWidth)
        y = (centerScreenY + boxWidth)

    #outside square
    #left side
    if x > (centerScreenX - (boxWidth + wallWidth) - 25) and x < (centerScreenX - (boxWidth + wallWidth) + 25) and y > (centerScreenY - (boxWidth + wallWidth) - 25) and y < (centerScreenY - (boxWidth + wallWidth) + 25):
        x = (centerScreenX - boxWidth - wallWidth)
        y = (centerScreenY - boxWidth - wallWidth)
    if x > (centerScreenX - (boxWidth + wallWidth) - 25) and x < (centerScreenX - (boxWidth + wallWidth) + 25) and y > (centerScreenY + (boxWidth + wallWidth) - 25) and y < (centerScreenY + (boxWidth + wallWidth) + 25):
        x = (centerScreenX - boxWidth - wallWidth)
        y = (centerScreenY + boxWidth + wallWidth)

    #right side
    if x > (centerScreenX + (boxWidth + wallWidth) - 25) and x < (centerScreenX + (boxWidth + wallWidth) + 25) and y > (centerScreenY - (boxWidth + wallWidth) - 25) and y < (centerScreenY - (boxWidth + wallWidth) + 25):
        x = (centerScreenX + boxWidth + wallWidth)
        y = (centerScreenY - boxWidth - wallWidth)
    if x > (centerScreenX + (boxWidth + wallWidth) - 25) and x < (centerScreenX + (boxWidth + wallWidth) + 25) and y > (centerScreenY + (boxWidth + wallWidth) - 25) and y < (centerScreenY + (boxWidth + wallWidth) + 25):
        x = (centerScreenX + boxWidth + wallWidth)
        y = (centerScreenY + boxWidth + wallWidth)
        
    return (x,y)


########################################

def snap(point):
    (p1, p2) = point
    for line in lines:
        if abs(p1 - line.p1[0]) <= 25 and abs(p2 - line.p1[1]) <= 25:   
            return (line.p1[0], line.p1[1])
        elif abs(p1 - line.p2[0]) <= 25 and (p2 - line.p2[1]) <= 25:   
            return (line.p2[0], line.p2[1])
    return point

########################################
    

########################################

MODE_NONE   = 0
MODE_LINE   = 1
MODE_BOX    = 2
MODE_CIRCLE = 3
MODE = 0
PROGRAM = 2

mode = MODE_NONE
waiting_for_second_click = False
waiting_for_second_click_circle = False
first_click = None
completeCircle = False

########################################

def checkComplete():
    count = 0 
    for value in linesDict.values():
        if value <= 1:
            count += 1
            
    return count

########################################


while beginFrame():

    #######################################
    
    grid()

    ## DRAWING ANCHORS FOR SQUARE####################
    
    if PROGRAM == 1:
        pygame.draw.circle(canvas, color = "red", center = (centerScreenX - boxWidth, centerScreenY - boxWidth), radius = 4)
        pygame.draw.circle(canvas, color = "red", center = (centerScreenX - boxWidth, centerScreenY + boxWidth), radius = 4)
        pygame.draw.circle(canvas, color = "red", center = (centerScreenX + boxWidth, centerScreenY - boxWidth), radius = 4)
        pygame.draw.circle(canvas, color = "red", center = (centerScreenX + boxWidth, centerScreenY + boxWidth), radius = 4)

        #outside
        pygame.draw.circle(canvas, color = "dark green", center = (centerScreenX - (boxWidth + wallWidth), centerScreenY - (boxWidth + wallWidth)), radius = 4)
        pygame.draw.circle(canvas, color = "dark green", center = (centerScreenX - (boxWidth + wallWidth), centerScreenY + (boxWidth + wallWidth)), radius = 4)
        pygame.draw.circle(canvas, color = "dark green", center = (centerScreenX + (boxWidth + wallWidth), centerScreenY - (boxWidth + wallWidth)), radius = 4)
        pygame.draw.circle(canvas, color = "dark green", center = (centerScreenX + (boxWidth + wallWidth), centerScreenY + (boxWidth + wallWidth)), radius = 4)

    elif PROGRAM == 2:
        pygame.draw.circle(canvas, color = "black", center = (centerScreenX, centerScreenY), radius = 60, width = 2)
        
    # DRAWING LEGEND #######################
    pygame.draw.rect(canvas, color = (162, 189, 235), rect = (10,10,60,60))
    lineFont = pygame.font.Font(None, 32)
    lineObj = lineFont.render('line', True, (30, 30, 30), None)
    canvas.blit(lineObj, (20,30))

    # circle square
    pygame.draw.rect(canvas, color = (129, 235, 125), rect = (80,10,60,60))
    arcFont = pygame.font.Font(None, 25)
    circleObj = arcFont.render('circle', True, (30, 30, 30), None)
    canvas.blit(circleObj, (86,30))
    
    # USER INPUT & UPDATE ##################
            
    for event in event_queue:
        current_mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and MODE == 0:
            if current_mouse_pos[0] >= 10 and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= 70 and current_mouse_pos[1] >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
                MODE = 1
            if current_mouse_pos[0] >= 80 and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= 140 and current_mouse_pos[1] >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
                MODE = 2
                
        elif event.type == pygame.MOUSEBUTTONDOWN and MODE == 1:
            if not waiting_for_second_click:
                waiting_for_second_click = True
                first_click = event.pos
                if PROGRAM == 1:
                    first_click = anchorSquare(first_click)
                if PROGRAM == 2:
                    if lines != []:
                        first_click = snap(first_click)
                        if first_click in linesDict:
                            linesDict[first_click] += 1
                        else:
                            linesDict[first_click] = 1
                    else:
                        linesDict[first_click] = 1
            else: 
                second_click = event.pos
                waiting_for_second_click = False
                if PROGRAM == 1:
                    second_click = anchorSquare(second_click)
                if PROGRAM == 2:
                    if lines != []:
                        second_click = snap(second_click)
                        if second_click in linesDict:
                            linesDict[second_click] += 1
                        else:
                            linesDict[second_click] = 1
                    else:
                        linesDict[second_click] = 1
                        
                lines.append(Line(first_click, second_click))
                print(linesDict)
                MODE = 0
                
        elif event.type == pygame.MOUSEBUTTONDOWN and MODE == 2:
            if not waiting_for_second_click_circle:
                waiting_for_second_click_circle = True
                first_click = event.pos
            else:
                second_click = event.pos
                waiting_for_second_click_circle = False
                rad = math.sqrt(math.pow(second_click[0] - first_click[0], 2) + math.pow(second_click[1] - first_click[1], 2))
                circles.append(Circle(first_click, rad))
                MODE = 0    

                #if mode == MODE_LINE:
                #    lines.append(Line(first_click, second_click))
                #elif mode == MODE_CIRCLE:
                #    pass

        
    # DRAW #################################
    
    if checkComplete() != 0:
        drawC = pygame.draw.circle(canvas, color = "red", center = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), radius = 10)
    elif checkComplete() == 0:
        drawC = pygame.draw.circle(canvas, color = "green", center = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), radius = 10)

    if waiting_for_second_click:
        pygame.draw.line(canvas, "BLUE", first_click, current_mouse_pos, 2)
        
    if waiting_for_second_click_circle:
        current_rad = math.sqrt(math.pow(current_mouse_pos[0] - first_click[0], 2) + math.pow(current_mouse_pos[1] - first_click[1], 2))
        pygame.draw.circle(canvas, "RED", first_click, current_rad, width=2)

    for line in lines:
        pygame.draw.line(canvas, "RED", line.p1, line.p2, 2)
        
    for circle in circles:
        pygame.draw.circle(canvas, "GREEN", circle.p1, circle.r, width=2)

