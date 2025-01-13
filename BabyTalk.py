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


########################################

canvas = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT)) 
clock = pygame.time.Clock()
event_queue = None

########################################

# file_name = "fidgetBearing.dxf"
# file_name = "lineTest.dxf"
# file_name = "combo.dxf"
# file_name = "colortest.dxf"
# file_name = "a.dxf"
file_name = "b.dxf"


########################################

PPM = 3.7795275591

def close_and_save():
    linesMM = []
    circlesMM = []

    for line in lines:
        linesMM.append([lineUnitConverter(line.p1), lineUnitConverter(line.p2)])
            
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
            if color == 6:  
                snaps.append(Snap((centerScreenX + PPM * center_x, centerScreenY - PPM * center_y), True))
            else:
                circles.append(Circle((centerScreenX + PPM * center_x, centerScreenY - PPM * center_y), radius * PPM, frozen))        
        else:
            print("WARNING: UnrecognizedEntity - " + str(e))




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

class Snap:
    def __init__(self, p1, frozen):
        self.p1 = p1
        self.frozen = frozen

    def draw(self):
        pygame.draw.circle(canvas, "Purple", self.p1, radius = 3)

    
########################################



########################################

def snapTo(point):
    (p1, p2) = point
    for line in lines:
        if abs(p1 - line.p1[0]) <= 25 and abs(p2 - line.p1[1]) <= 25:   
            return (line.p1[0], line.p1[1])
        elif abs(p1 - line.p2[0]) <= 25 and abs(p2 - line.p2[1]) <= 25:   
            return (line.p2[0], line.p2[1])
        
    for snap in snaps:
        if abs(p1 - snap.p1[0]) <= 25 and abs(p2 - snap.p1[1]) <= 25:
            return (snap.p1[0], snap.p1[1])
    return point

########################################

def is_point_in_polygon(point, polygon_points):
    
    x, y = point
    n = len(polygon_points)
    inside = False
    
    p1x, p1y = polygon_points[0]
    
    for i in range(n + 1):
        p2x, p2y = polygon_points[i % n]
        
        if min(p1y, p2y) < y <= max(p1y, p2y):
           
            if x <= max(p1x, p2x):
               
                if p1y != p2y:
                    xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        
        p1x, p1y = p2x, p2y
    
    return inside
    
########################################

def get_parallel_lines(x1, y1, x2, y2, distance=25):
   
    dx = x2 - x1
    dy = y2 - y1
    
    length = math.sqrt(dx*dx + dy*dy)
    
    if length != 0:
        dx = dx/length
        dy = dy/length
    
    perpx = -dy
    perpy = dx
    
    line1_x1 = round(x1 + perpx * distance, 3)
    line1_y1 = round(y1 + perpy * distance, 3)
    line1_x2 = round(x2 + perpx * distance, 3)
    line1_y2 = round(y2 + perpy * distance, 3)
    
    line2_x1 = round(x1 - perpx * distance, 3)
    line2_y1 = round(y1 - perpy * distance, 3)
    line2_x2 = round(x2 - perpx * distance, 3)
    line2_y2 = round(y2 - perpy * distance, 3)
    
    return (line1_x1, line1_y1), (line1_x2, line1_y2), (line2_x1, line2_y1), (line2_x2, line2_y2)

########################################

MODE_NONE   = 0
MODE_BOX    = 1
MODE_CIRCLE = 2
MODE_ERASER = 3
MODE_LINE   = 4

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

def addToDict(line):
    if lines != []:
        click = snapTo(line)
        if click in linesDict:
            linesDict[click] += 1
        else:
            linesDict[click] = 1
    else:
        linesDict[click] = 1

    return click 

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
    current_mouse_pos = pygame.mouse.get_pos()
    
    # draw grid
    blockSize = 25
    for x in range(0, SCREEN_WIDTH, blockSize):
        for y in range(0, SCREEN_HEIGHT, blockSize):
            rectGrid = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(canvas, color = "light grey", rect = rectGrid, width = 1)
    
    # imgui api
    already_drew_gui_this_frame = False
    mouse_eaten_by_button = False
    def BUTTON(event, name, color):
        global _button_x
        global current_mouse_pos
        global mouse_eaten_by_button

        BUTTON_WIDTH = 60

        mouse_in_button_rect = current_mouse_pos[0] >= _button_x and current_mouse_pos[1] <= 70 and current_mouse_pos[0] <= _button_x + 60 and current_mouse_pos[1] >= 10        
        
        if (mouse_in_button_rect):
            color = ((color[0] + 255) / 2, (color[1] + 255) / 2, (color[2] + 255) / 2)

        if not already_drew_gui_this_frame:
            # draw itself
            pygame.draw.rect(canvas, color = color, rect = (_button_x,10,BUTTON_WIDTH,BUTTON_WIDTH))
            font = pygame.font.Font(None, 26)
            text_width, _ = font.size(name)
            canvas.blit(\
                font.render(name, True, (30, 30, 30), None),
                (_button_x + (BUTTON_WIDTH - text_width) / 2, 30))
        # update gui state
        _button_x += 70

        result = (event != None) and (event.type == pygame.MOUSEBUTTONDOWN) and mouse_in_button_rect # FORNOW BAD VERY BAD
        if result:
            mouse_eaten_by_button = True
        return result


    if (len(event_queue) == 0):
        event_queue.append(None)
    for event in event_queue:

        mouse_eaten_by_button = False
        _button_x = 10
        if (BUTTON(event, "box", (129, 235, 125))): 
            mode = MODE_BOX 
        if (BUTTON(event, "circle", (129, 235, 125))): 
            mode = MODE_CIRCLE                                                   
        if (BUTTON(event, "eraser", (234, 224, 153))): 
            mode = MODE_ERASER
        if (BUTTON(event, "line", (162, 189, 235))): 
            mode = MODE_LINE 
        if (BUTTON(event, "end", (255, 0, 0))): 
            close_and_save()
        already_drew_gui_this_frame = True

        if event == None:
             pass
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_eaten_by_button:
                pass 
            elif mode == MODE_LINE:
                if not waiting_for_second_click:
                    waiting_for_second_click = True
                    first_click = event.pos
                    first_click = addToDict(first_click)
                else: 
                    second_click = event.pos
                    waiting_for_second_click = False
                    second_click = addToDict(second_click)
                    lines.append(Line(first_click, second_click, False))
                    mode = MODE_NONE

            elif mode == MODE_CIRCLE:
                if not waiting_for_second_click_circle:
                    waiting_for_second_click_circle = True
                    first_click = event.pos
                else:
                    second_click = event.pos
                    waiting_for_second_click_circle = False
                    rad = math.sqrt(math.pow(second_click[0] - first_click[0], 2) + math.pow(second_click[1] - first_click[1], 2))
                    circles.append(Circle(first_click, rad, False))
                    mode = MODE_NONE 

            elif mode == MODE_ERASER:
                click = event.pos

                for line in lines:
                    if line.frozen:
                        continue
                    
                    p1_x, p1_y = line.p1
                    p2_x, p2_y = line.p2

                    p1_pos, p2_pos, p1_neg, p2_neg = get_parallel_lines(p1_x, p1_y, p2_x, p2_y)
                    points = [p1_pos, p2_pos, p2_neg, p1_neg]
                    
                    if is_point_in_polygon(click, points):
                        lines.remove(line)

                mode = MODE_NONE

            elif mode == MODE_BOX:
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

                    mode = MODE_NONE    
                           
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

    for snap in snaps:
        snap.draw()





                
