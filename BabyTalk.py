# TODO: Snaps (purple circles)


import pygame
import sys
import os
import math
import ezdxf
import time
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

snaps = []
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

# file_name = "fidgetBearing.dxf"
# file_name = "lineTest.dxf"
# file_name = "combo.dxf"
#file_name = "colortest.dxf"
file_name = "a.dxf"


########################################

PPM = 3.7795275591

###DXF READER###########################

def readDXF():
    try:
        doc, auditor = recover.readfile(file_name)
    except IOError:
        print(f"Not a DXF file or a generic I/O error.")
        sys.exit(1)
    except ezdxf.DXFStructureError:
        print(f"Invalid or corrupted DXF file.")
        sys.exit(2)
    
   
    msp = doc.modelspace()

    for e in msp:
        color = e.dxf.color
        frozen = (color == 5)
        if e.dxftype() == "LINE":
            start_x, start_y = e.dxf.start[0], e.dxf.start[1]
            end_x, end_y = e.dxf.end[0], e.dxf.end[1]
            lines.append(Line((centerScreenX + PPM * start_x , centerScreenY - PPM * start_y), (centerScreenX + PPM * end_x, centerScreenY - PPM * end_y), frozen))
        elif e.dxftype() == "CIRCLE":
            center_x, center_y = e.dxf.center[0], e.dxf.center[1]
            radius = e.dxf.radius
            circles.append(Circle((centerScreenX + PPM * center_x, centerScreenY - PPM * center_y), radius * PPM, frozen))        
        else:
            print("WARNING: UnrecognizedEntity - " + str(e))

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

# ENTITIES

# color is an int 

class Line:
    def __init__(self, p1, p2, frozen):
        # World Coordinates
        self.p1 = p1
        self.p2 = p2
        self.frozen = frozen
         
    def draw(self): # TODO
        # FORNOW
        # TODO: if frozen, draw blue, else draw red

        color = "BLUE" if self.frozen else "RED"
        pygame.draw.line(canvas, color, (self.p1[0], self.p1[1]), (self.p2[0], self.p2[1]), 2)

        # TODO: Converts to Pixel Coordinates and Draws

class Circle:
    def __init__(self, p1, r, frozen):
        self.p1 = p1
        self.r = r
        self.frozen = frozen

    def draw(self): 
        color = "BLUE" if self.frozen else "RED"
        pygame.draw.circle(canvas, color, self.p1, self.r, width=2)
    
########################################

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

def is_point_in_polygon(point, polygon_points):
    
    x, y = point
    n = len(polygon_points)
    inside = False
    
    # Get the last point
    p1x, p1y = polygon_points[0]
    
    # Loop through all edges of the polygon
    for i in range(n + 1):
        # Get next point
        p2x, p2y = polygon_points[i % n]
        
        # Check if point is within y-range of the edge
        if min(p1y, p2y) < y <= max(p1y, p2y):
            # Check if point is to the left of the edge
            if x <= max(p1x, p2x):
                # Calculate intersection of horizontal ray from point
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        
        p1x, p1y = p2x, p2y
    
    return inside
    
########################################

def get_parallel_lines(x1, y1, x2, y2, distance=25):
   
    # Calculate the direction vector of the original line
    dx = x2 - x1
    dy = y2 - y1
    
    # Calculate length of the line
    length = math.sqrt(dx*dx + dy*dy)
    
    # Normalize the direction vector
    if length != 0:
        dx = dx/length
        dy = dy/length
    
    # Calculate perpendicular vector (rotate 90 degrees)
    # For rotation: x' = -y, y' = x
    perpx = -dy
    perpy = dx
    
    #first parallel line
    line1_x1 = round(x1 + perpx * distance, 3)
    line1_y1 = round(y1 + perpy * distance, 3)
    line1_x2 = round(x2 + perpx * distance, 3)
    line1_y2 = round(y2 + perpy * distance, 3)
    
    # second parallel line
    line2_x1 = round(x1 - perpx * distance, 3)
    line2_y1 = round(y1 - perpy * distance, 3)
    line2_x2 = round(x2 - perpx * distance, 3)
    line2_y2 = round(y2 - perpy * distance, 3)
    
    
    return (line1_x1, line1_y1), (line1_x2, line1_y2), (line2_x1, line2_y1), (line2_x2, line2_y2)

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
waiting_for_second_box_click = False
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
########################################


# TODO
# Line List needs to be in MM
# 1 / PPM

# NOTE: This clears the annoying "[IMKClient subclass]: chose IMKClient_Legacy" message on Mac
if True:
    pygame.event.get()
    pygame.event.get()
    os.system('clear')

readDXF()

while beginFrame():
    #######################################
    
    grid()

    ## DRAWING ANCHORS FOR SQUARE####################
    
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
    eraserObj = eraserFont.render('eraser', True, (30, 30, 30), None)
    canvas.blit(eraserObj, (154, 30))

    # box square
    pygame.draw.rect(canvas, color = (129, 235, 125), rect = (220,10,60,60))
    boxFont = pygame.font.Font(None, 25)
    boxObj = boxFont.render('box', True, (30, 30, 30), None)
    canvas.blit(boxObj, (234,30))
    
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
            #line
            if current_mouse_pos[0] >= 10 and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= 70 and current_mouse_pos[1] >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
                MODE = 1

            #circle
            if current_mouse_pos[0] >= 80 and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= 140 and current_mouse_pos[1] >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
                MODE = 2

            #eraser
            if current_mouse_pos[0] >= 150 and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= 210 and current_mouse_pos[1] >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
                MODE = 3

            #end
            if current_mouse_pos[0] >= SCREEN_WIDTH - 70 and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= SCREEN_WIDTH - 10 and current_mouse_pos[1] >= 10 and event.type == pygame.MOUSEBUTTONDOWN:
                MODE = 4
            
            #box
            if current_mouse_pos[0] >= 220 and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= 280 and current_mouse_pos[1] >= 10 and event.type == pygame.MOUSEBUTTONDOWN: 
                MODE = 5
                
        elif event.type == pygame.MOUSEBUTTONDOWN and MODE == 1:
            if not waiting_for_second_click:
                waiting_for_second_click = True
                first_click = event.pos
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
                if lines != []:
                    second_click = snap(second_click)
                    if second_click in linesDict:
                        linesDict[second_click] += 1
                    else:
                        linesDict[second_click] = 1
                else:
                    linesDict[second_click] = 1

                lines.append(Line(first_click, second_click, False))
                MODE = 0
                
        elif event.type == pygame.MOUSEBUTTONDOWN and MODE == 2:
            if not waiting_for_second_click_circle:
                waiting_for_second_click_circle = True
                first_click = event.pos
            else:
                second_click = event.pos
                waiting_for_second_click_circle = False
                rad = math.sqrt(math.pow(second_click[0] - first_click[0], 2) + math.pow(second_click[1] - first_click[1], 2))
                circles.append(Circle(first_click, rad, False))
                MODE = 0    

                #if mode == MODE_LINE:
                #    lines.append(Line(first_click, second_click))
                #elif mode == MODE_CIRCLE:
                #    pass

        elif event.type == pygame.MOUSEBUTTONDOWN and MODE == 3:
            click = event.pos

            for line in lines:
                if line.frozen:
                    continue
                
                p1_x, p1_y = line.p1
                p2_x, p2_y = line.p2

                p1_pos, p2_pos, p1_neg, p2_neg = get_parallel_lines(p1_x, p1_y, p2_x, p2_y)
                points = [p1_pos, p2_pos, p2_neg, p1_neg]
                
                #rects.append(points)   

                if is_point_in_polygon(click, points):
                    lines.remove(line)

            MODE = 0

        elif event.type == pygame.MOUSEBUTTONDOWN and MODE == 5:
            if not waiting_for_second_box_click:
                waiting_for_second_box_click = True
                first_click = event.pos
            
            else:
                second_click = event.pos
                waiting_for_second_box_click = False
                
                lines.append(Line(first_click, (first_click[0], second_click[1]), False))
                lines.append(Line(first_click, (second_click[0], first_click[1]), False))
                lines.append(Line((first_click[0], second_click[1]), second_click, False))
                lines.append(Line((second_click[0], first_click[1]), second_click, False))
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
                        
            
            with r12writer("test.dxf") as dxf:
                dxf.units = units.MM
                for line in linesMM:
                    dxf.add_line(start = line[0], end = line[1], color = 1)
        
                for circle in circlesMM:
                    dxf.add_circle(center = circle[0], radius = circle[1], color = 3)
                    
            
            print("Your file has been exported")
            
            exit()
        
    # DRAW #################################
    
    if checkComplete() != 0:
        drawC = pygame.draw.circle(canvas, color = "red", center = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), radius = 10)
    elif checkComplete() == 0:
        drawC = pygame.draw.circle(canvas, color = "green", center = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), radius = 10)

    if waiting_for_second_click:
        pygame.draw.line(canvas, "GREEN", first_click, current_mouse_pos, 2)

    if waiting_for_second_box_click:
        pygame.draw.line(canvas, "GREEN", first_click, (first_click[0], current_mouse_pos[1]), 2)
        pygame.draw.line(canvas, "GREEN", first_click, (current_mouse_pos[0], first_click[1]), 2)
        pygame.draw.line(canvas, "GREEN", (first_click[0], current_mouse_pos[1]), current_mouse_pos, 2)
        pygame.draw.line(canvas, "GREEN", (current_mouse_pos[0], first_click[1]), current_mouse_pos, 2)
        
    if waiting_for_second_click_circle:
        current_rad = math.sqrt(math.pow(current_mouse_pos[0] - first_click[0], 2) + math.pow(current_mouse_pos[1] - first_click[1], 2))
        pygame.draw.circle(canvas, "ORANGE", first_click, current_rad, width=2)

    for line in lines:
        line.draw()

    for circle in circles:
        circle.draw()





                
