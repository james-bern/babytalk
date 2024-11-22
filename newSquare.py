
import pygame
import sys
import os
import math
import ezdxf
from ezdxf import recover, units
from ezdxf.addons import r12writer

pygame.init()
os.system('clear')

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 750
(centerScreenX, centerScreenY) = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
boxWidth = 200
wallWidth = 40

########################################

lines = []
linesDict = {}
circles = []
linesMM = []
circlesMM = []

########################################

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
clock = pygame.time.Clock()
event_queue = None


########################################

fidget = "fidgetBearing.dxf"
lineTest = "lineTest.dxf"
combo = "combo.dxf"

########################################

PPM = 3.7795275591

def draw_line_entity(e):
    start_x, start_y = e.dxf.start[0], e.dxf.start[1]
    end_x, end_y = e.dxf.end[0], e.dxf.end[1]
    # pygame.draw.line(canvas, "BLACK", (centerScreenX + PPM * start_x, centerScreenY - PPM * start_y), (centerScreenX + PPM * end_x, centerScreenY - PPM * end_y))
    lines.append(Line((centerScreenX + PPM * start_x , centerScreenY - PPM * start_y), (centerScreenX + PPM * end_x, centerScreenY - PPM * end_y)))
    
def draw_circle_entity(e):
    center_x, center_y = e.dxf.center[0], e.dxf.center[1]
    radius = e.dxf.radius
    # pygame.draw.circle(canvas, "BLACK", (centerScreenX + PPM * center_x, centerScreenY - PPM * center_y), PPM * radius, width = 2)
    circles.append(Circle((centerScreenX + PPM * center_x, centerScreenY - PPM * center_y), radius * PPM))
    
###DXF READER###########################

def readDXF():
    try:
        doc, auditor = recover.readfile(combo)
    except IOError:
        print(f"Not a DXF file or a generic I/O error.")
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file.")
        sys.exit(2)
    
   
    msp = doc.modelspace()

    for e in msp:
        if e.dxftype() == "LINE":
            draw_line_entity(e)
        if e.dxftype() == "ARC":
            draw_circle_entity(e)
        
    
########################################

def grid():
    blockSize = 25
    for x in range(0, SCREEN_WIDTH, blockSize):
        for y in range(0, SCREEN_HEIGHT, blockSize):
            rectGrid = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(canvas, color = "light grey", rect = rectGrid, width = 1)


########################################


def lineUnitConverter(point):
    x, y = point
    
    xZero = x - centerScreenX
    yZero = centerScreenY - y
    
    return (xZero / PPM, yZero / PPM)
    
########################################

def circleUnitConverter(coords, r):
    x, y = coords
    radius = r
    
    xNew = x - centerScreenX
    yNew = centerScreenY - y
    
    newCoords = (xNew / PPM, yNew / PPM)
    
    return newCoords, r / PPM
    

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
        # World Coordinates
        self.p1 = p1
        self.p2 = p2
        
    def draw(self):
        # Converts to Pixel Coordinates and Draws
        pygame.draw.line(canvas, "BLACK",
                        (PPM * self.p1[0], PPM * self.p1[1]),
                        (PPM * self.p2[0], PPM * self.p2[1]))

########################################

class Circle:
    def __init__(self, p1, r):
        self.p1 = p1
        self.r = r

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
        elif abs(p1 - line.p2[0]) <= 25 and abs(p2 - line.p2[1]) <= 25:   
            return (line.p2[0], line.p2[1])
    return point

########################################
    

########################################

MODE_NONE   = 0
MODE_LINE   = 1
MODE_BOX    = 2
MODE_CIRCLE = 3
MODE = 0
PROGRAM = 3

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

def checkBearingCircle(point):
    (x, y) = point
    dist = math.sqrt((centerScreenX - x) ** 2 + (centerScreenY - y) ** 2)
    if dist > 60:
        return True
    
    return False

########################################


# TODO
# Line List needs to be in MM
# 1 / PPM

readDXF()

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
        pygame.draw.circle(canvas, color = "red", center = (centerScreenX, centerScreenY), radius = 60, width = 2)
        pygame.draw.circle(canvas, color = "yellow", center = (centerScreenX, centerScreenY), radius = 40, width = 2)
        
        
    # DRAWING LEGEND #######################
    pygame.draw.rect(canvas, color = (162, 189, 235), rect = (10,10,60,60))
    lineFont = pygame.font.Font(None, 32)
    lineObj = lineFont.render('line', True, (30, 30, 30), None)
    canvas.blit(lineObj, (20,30))

    # circle square
    pygame.draw.rect(canvas, color = (129, 235, 125), rect = (80,10,60,60))
    circleFont = pygame.font.Font(None, 25)
    circleObj = circleFont.render('circle', True, (30, 30, 30), None)
    canvas.blit(circleObj, (86,30))
    
    # eraser
    pygame.draw.rect(canvas, color = (234, 224, 153), rect = (150,10,60,60))
    eraserFont = pygame.font.Font(None, 25)
    eraserObj = eraserFont.render('cancel', True, (30, 30, 30), None)
    canvas.blit(eraserObj, (154,30))
    
    # end
    pygame.draw.rect(canvas, color = "red", rect = (SCREEN_WIDTH - 70,10,60,60))
    endFont = pygame.font.Font(None, 30)
    endObj = endFont.render('END', True, (30, 30, 30), None)
    canvas.blit(endObj, (SCREEN_WIDTH - 62 ,30))
    
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
            if current_mouse_pos[0] >= 150 and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= 210 and current_mouse_pos[1] >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
                MODE = 3
            if current_mouse_pos[0] >= SCREEN_WIDTH - 70 and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= SCREEN_WIDTH - 10 and current_mouse_pos[1] >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
                MODE = 4
                
        elif event.type == pygame.MOUSEBUTTONDOWN and MODE == 1:
            if not waiting_for_second_click:
                waiting_for_second_click = True
                first_click = event.pos
                if PROGRAM == 1:
                    first_click = anchorSquare(first_click)
                if PROGRAM == 2:
                    if checkBearingCircle(first_click):
                        if lines != []:
                            first_click = snap(first_click)
                            if first_click in linesDict:
                                linesDict[first_click] += 1
                            else:
                                linesDict[first_click] = 1
                        else:
                            linesDict[first_click] = 1
                    else: 
                        waiting_for_second_click = False
                        
                if PROGRAM == 3:
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
                    if checkBearingCircle(second_click):
                        if lines != []:
                            second_click = snap(second_click)
                            if second_click in linesDict:
                                linesDict[second_click] += 1
                            else:
                                linesDict[second_click] = 1
                        else:
                            linesDict[second_click] = 1
                if PROGRAM == 3:
                    if lines != []:
                        second_click = snap(second_click)
                        if second_click in linesDict:
                            linesDict[second_click] += 1
                        else:
                            linesDict[second_click] = 1
                    else:
                        linesDict[second_click] = 1
                        
                        
                lines.append(Line(first_click, second_click))
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

        elif event.type == pygame.MOUSEBUTTONDOWN and MODE == 3:
            erase_click_x, erase_click_y = event.pos
            smallest_dist = SCREEN_WIDTH
            lineObj = None
            for line in lines:
                x_1, y_1 = line.p1
                x_2, y_2 = line.p2
                
                t = ((erase_click_x - x_1) * (x_2 - x_1)) + ((erase_click_y - y_1) * (y_2 - y_1)) / (((x_2 - x_1) ** 2) + ((y_2 - y_1)**2))
            
                if t < 0 and abs(x_1 - erase_click_x) <= 25 and abs(y_1 - erase_click_y) <= 25:
                    tempDist = math.sqrt(((erase_click_x - x_1) ** 2) + ((erase_click_y - y_1)**2))
                    if tempDist < smallest_dist:
                        lineObj = line
                        smallest_dist = tempDist
                
                elif t > 1 and abs(x_2 - erase_click_x) <= 25 and abs(y_2 - erase_click_y) <= 25:
                    tempDist = math.sqrt(((erase_click_x - x_2) ** 2) + ((erase_click_y - y_2)**2))
                    if tempDist < smallest_dist:
                        lineObj = line
                        smallest_dist = tempDist
                
                else:
                    x_close = x_1 + (t * (x_2 - x_1))
                    y_close = y_1 + (t * (y_2 - y_1))
                    
                    tempDist = math.sqrt(((erase_click_x - x_close) ** 2) + ((erase_click_y - y_close)**2))
                    if tempDist < smallest_dist:
                        lineObj = line
                        smallest_dist = tempDist
                
            MODE = 0
                   
        elif MODE == 4:
            if lines != []:
                for line in lines:
                    linesMM.append([lineUnitConverter(line.p1), lineUnitConverter(line.p2)])
                    
            if circles != []:
                for circle in circles:
                    newCoords, r = circleUnitConverter(circle.p1, circle.r)
                    toAdd = [newCoords, r]
                    if toAdd not in circlesMM: 
                        circlesMM.append(toAdd)
                    
            print(linesMM)
            print(circlesMM)
            
            with r12writer("test.dxf") as dxf:
                dxf.units = units.MM
                for line in linesMM:
                    dxf.add_line(start = line[0], end = line[1], color = 3)
        
                for circle in circlesMM:
                    dxf.add_circle(center = circle[0], radius = circle[1], color = 4)
            
            print("Your file has been exported")
            
            exit()
        
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
        pygame.draw.line(canvas, "GREEN", (line.p1[0], line.p1[1]), (line.p2[0], line.p2[1]), 2)
        
    for circle in circles:
        pygame.draw.circle(canvas, "GREEN", circle.p1, circle.r, width=2)




                
