# TODO Fidger Spinner
# TODO Find another worksheet – Box + Lid?
# TODO 3.4, 3.0, 2.6 (>, =, <)
# TODO maybe box sizes
# TODO seperate pane for buttons, forbidden zone (mouse press events don't actually get processed by us if y > ??)

import pygame
import sys
import os
import math
import ezdxf
import time
from ezdxf import recover, units
from ezdxf.addons import r12writer
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.dropdown import Dropdown



pygame.init()
os.system('clear')

SCREEN_WIDTH = 1039
SCREEN_HEIGHT = 803
(centerScreenX, centerScreenY) = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 47)
boxWidth = 200
wallWidth = 40
blockSize = 38


########################################

snaps = []
forbidden_regions = []
lines = []
linesDict = {}
circles = []

connected_constraint = False

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
# file_name = "b.dxf"
# file_name = "fidgetWorksheet.dxf"
# file_name = "snapWorksheet.dxf"
# file_name = "presentation.dxf"
# file_name = "snapTest.dxf"
# file_name = "fidgetTest2.dxf"
# file_name = "finalFidget.dxf"
file_name = "snowFidget.dxf"
# file_name = "blank.dxf"

########################################

PPM = 8.0

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
                
    
    with r12writer("creation.dxf") as dxf:
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
            if color == 4:
                pass
            else:
                start_x, start_y = e.dxf.start[0], e.dxf.start[1]
                end_x, end_y = e.dxf.end[0], e.dxf.end[1]
                lines.append(Line((centerScreenX + PPM * start_x , centerScreenY - PPM * start_y), (centerScreenX + PPM * end_x, centerScreenY - PPM * end_y), frozen))

        elif e.dxftype() == "CIRCLE":
            center_x, center_y = e.dxf.center[0], e.dxf.center[1]
            radius = e.dxf.radius
            if color == 7: 
                snaps.append(Snap((centerScreenX + PPM * center_x, centerScreenY - PPM * center_y), True))
            elif color == 2:
                forbidden_regions.append(Forbidden((centerScreenX + PPM * center_x, centerScreenY - PPM * center_y), radius * PPM, True))
            elif color == 4:
                connected_constraint = True
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
    # draw grid
    for x in range(0, SCREEN_WIDTH, int(blockSize)):
        for y in range(0, SCREEN_HEIGHT, int(blockSize)):
            rectGrid = pygame.Rect(x, y, blockSize, blockSize)
            pygame.draw.rect(canvas, color = (240,240,240), rect = rectGrid, width = 1)

    event_queue = []

    events = pygame.event.get()

    pygame_widgets.update(events)

    for event in events: 
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

class Forbidden:
    def __init__(self, p1, r, frozen):
        self.p1 = p1
        self.r = r
        self.frozen = frozen

    def draw(self):
        pygame.draw.circle(canvas, (255, 213, 128), self.p1, self.r)

    
########################################

def is_point_forbidden(point):
    (p1, p2) = point
    for zone in forbidden_regions:
        (c1, c2) = zone.p1
        radius = zone.r
        d = math.sqrt((((c1 - p1)**2) + ((c2 - p2)**2)))
        if d < radius: 
            return True
    
    return False

########################################

def snapTo(point, shape):
    (p1, p2) = point

    blockSnap = round(blockSize)

    if shape == "Line":
        for line in lines:
            if abs(p1 - line.p1[0]) <= 10 and abs(p2 - line.p1[1]) <= 10:   
                return (line.p1[0], line.p1[1])
            elif abs(p1 - line.p2[0]) <= 10 and abs(p2 - line.p2[1]) <= 10:   
                return (line.p2[0], line.p2[1])
    
        if (p1 % blockSnap < 5 or p1 % blockSnap > blockSnap - 5) and (p2 % blockSnap < 5 or p2 % blockSnap > blockSnap - 5):
            closeX = round(p1/blockSnap)
            closeY = round(p2/blockSnap)
            newX = closeX * blockSnap
            newY = closeY * blockSnap
            return (newX, newY)

    for snap in snaps:
        if abs(p1 - snap.p1[0]) <= 10 and abs(p2 - snap.p1[1]) <= 10:
            return (snap.p1[0], snap.p1[1])
    return point


########################################

def eraseCircle(circle, point):
    c_x, c_y = circle.p1
    p_x, p_y = point

    d = abs(math.sqrt((p_x - c_x)**2 + (p_y - c_y)**2) - circle.r)

    if d < 20 :
        return True
    
    return False

def eraseLine(lineA, lineB, point):
    x_a, y_a = lineA
    x_b, y_b = lineB
    p_1, p_2 = point

    top = abs(((x_b - x_a) * (p_2 - y_a)) - ((y_b - y_a) * (p_1 - x_a)))
    bottom = math.sqrt((x_b - x_a)**2 + (y_b -y_a)**2)

    if bottom == 0:
        return True

    d = top / bottom

    if d < 20:
        return True
    
    return False

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

lengthNeeded = False
waiting_for_second_click_length = False
length = None

squareLengthNeeded = False
waiting_for_second_click_square_length = False
squareLength = None

angleNeeded = False
angleOnOff = False

########################################

########################################

def isConnected():
    endpointDict = {}

    for line in lines:
        if line.p1 not in endpointDict.keys():
            endpointDict[line.p1] = 1
        else:
            endpointDict[line.p1] += 1
        
        if line.p2 not in endpointDict.keys():
            endpointDict[line.p2] = 1
        else:
            endpointDict[line.p2] += 1

    for value in endpointDict.values():
        if value != 2:
            return False
            
    return True


########################################
    

def helperDesignatedRadius(click, size):
    global waiting_for_second_click_circle
    global first_click
    global mode
    circles.append(Circle(click, size, False))
    waiting_for_second_click_circle = False
    first_click = None
    mode = MODE_NONE

    pressFit.hide()
    slipButton.hide()
    
def helperDesignateSquareSize(click, length):
    global waiting_for_second_box_click
    global first_click
    global mode

    if mode == MODE_BOX:
    #lines
        l1 = Line(click, (click[0], click[1] + length), False)
        l2 = Line(click, (click[0] + length, click[1]), False)
        l3 = Line((click[0] + length, click[1]), (click[0] + length, click[1] + length), False)
        l4 = Line((click[0], click[1] + length), (click[0] + length, click[1] + length), False)
        lines.append(l1)
        lines.append(l2)
        lines.append(l3)
        lines.append(l4)

        #squareSizeDropdown.hide()
        # squareRelease.hide()

        waiting_for_second_box_click = False

    if mode == MODE_LINE:
        l1 = Line(click, (click[0]+length, click[1]+ length), False)

        lines.append(l1)
    
    first_click = None
    mode = MODE_NONE
    
def lineAngle(first, second):
    
    x1, y1 = first
    x2, y2 = second

    mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

    x = x2 - x1
    y = y2 - y1

    theta = math.atan2(y, x)

    newTheta = round(theta / (math.pi / 4)) * (math.pi / 4)

    firstNew = mag * math.cos(newTheta)
    secondNew = mag * math.sin(newTheta)

    return Line(first, (x1 + firstNew, y1 + secondNew), False)

# slip fit
slipButton = Button(
    canvas,  # Surface to place button on
    10,  # X-coordinate of top left corner
    80,  # Y-coordinate of top left corner
    40,  # Width
    40,  # Height

# Optional Parameters
text = 'Slip',  # Text to display
fontSize = 15,  # Size of font
margin = 20,  # Minimum distance between text/image and edge of button
inactiveColour = (200, 50, 0),  # Colour of button when not being interacted with
hoverColour = (150, 0, 0),  # Colour of button when being hovered over
pressedColour = (0, 200, 20),  # Colour of button when being clicked
onClick = lambda: helperDesignatedRadius(first_click, 10.0)  # Function to call when clicked on
)

# press fit

pressFit = Button(
    canvas,  # Surface to place button on
    80,  # X-coordinate of top left corner
    80,  # Y-coordinate of top left corner
    40,  # Width
    40,  # Height

# Optional Parameters
text = 'Press',  # Text to display
fontSize = 13,  # Size of font
margin = 20,  # Minimum distance between text/image and edge of button
inactiveColour=(200, 50, 0),  # Colour of button when not being interacted with
hoverColour=(150, 0, 0),  # Colour of button when being hovered over
pressedColour=(0, 200, 20),  # Colour of button when being clicked
onClick = lambda: helperDesignatedRadius(first_click, 8.0)  # Function to call when clicked on
)

def angleToggleFun():
    global angleNeeded
    global angleOnOff
    if angleOnOff == False:
        angleOnOff = True
        angleNeeded = True
        angleToggle.inactiveColour = "GREEN"
        print("ON")
    
    else:
        angleOnOff = False
        angleNeeded = False
        angleToggle.inactiveColour = "RED"
        print("OFF")

    

angleToggle = Button(
    canvas,  # Surface to place button on
    10,  # X-coordinate of top left corner
    80,  # Y-coordinate of top left corner
    60,  # Width
    60,  # Height

# Optional Parameters
text = 'Toggle 45˚',  # Text to display
fontSize = 11,  # Size of font
margin = 10,  # Minimum distance between text/image and edge of button
inactiveColour = "RED",  # Colour of button when not being interacted with
onClick = lambda: angleToggleFun()  # Function to call when clicked on
)

def helperSquareSize():
    global squareLengthNeeded
    if not waiting_for_second_click:
        squareLengthNeeded = True
 
squareSize = Dropdown (
    canvas, 80, 80, 60, 60, name = 'Length',
    choices=[
        '5.0',
        '10.0',
        '15.0',
        '20.0',
        '25.0',
        '30.0',
        '35.0',
        '40.0'
    ],
    borderRadius = 3, 
    inactiveColour = pygame.Color('Light Blue'),
    pressedColour = pygame.Color('Green'), 
    values = [5.0 * 5, 10.0 * 5, 15.0 * 5,
            20.0 * 5, 25.0 * 5, 30.0 * 5,
            35.0 * 5, 40.0 * 5], 
    direction = 'right', 
    textHAlign = 'left',
    onClick = lambda: helperSquareSize()
) 


def helperLineSize():
    global lengthNeeded 
    lengthNeeded = True

lineSize = Dropdown (
    canvas, 80, 80, 60, 60, name = 'Length',
    choices=[
        '5.0',
        '10.0',
        '15.0',
        '20.0',
        '25.0',
        '30.0',
        '35.0',
        '40.0'
    ],
    borderRadius = 3, 
    inactiveColour = pygame.Color('Light Blue'),
    pressedColour = pygame.Color('Green'), 
    values = [5.0 * 5, 10.0 * 5, 15.0 * 5,
            20.0 * 5, 25.0 * 5, 30.0 * 5,
            35.0 * 5, 40.0 * 5], 
    direction = 'right', 
    textHAlign = 'left',
    onClick = lambda: helperLineSize()
)


# NOTE (Jim): this is how to hide/show widgets
# pressFit.hide()
# pressFit.show()

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

pressFit.hide()
slipButton.hide()
#squareSizeDropdown.hide()
#squareRelease.hide()
squareSize.hide()
lineSize.hide()

while beginFrame():
    current_mouse_pos = pygame.mouse.get_pos()

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

        #pygame_widgets.update(event)
        
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


        pygame.draw.line(canvas, "black", (0, 160), (SCREEN_WIDTH, 160), width = 3)
        already_drew_gui_this_frame = True

        if mode == MODE_LINE:
            lineSize.show()
        if mode == MODE_BOX:
            squareSize.show()
        if event == None:
            pass
        elif event.type == pygame.KEYDOWN:
            pass
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_eaten_by_button:
                pass
            elif event.pos[1] < 160:
                pass
            elif mode == MODE_LINE:
                if not waiting_for_second_click:
                    waiting_for_second_click = True
                    first_click = event.pos
                    
                    if is_point_forbidden(first_click):
                        waiting_for_second_click = False
                        print('Cannot draw in forbidden zone')
                    else:
                        first_click = snapTo(first_click, "Line")
            
                else: 
                    second_click = event.pos
                    waiting_for_second_click = False
                    if is_point_forbidden(second_click):
                        waiting_for_second_click = True
                        print('Cannot draw in forbidden zone')

                    elif lengthNeeded:

                        length = lineSize.getSelected()

                        x1, y1 = first_click
                        x2, y2 = second_click

                        mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

                        if mag < length:
                            if angleNeeded:
                                line = lineAngle(first_click, second_click)

                            else:
                                line = Line(first_click, second_click, False)
                            lines.append(line)
                    
                        else:   
                            dx = ((x2 - x1) / mag) * length
                            dy = ((y2 - y1) / mag) * length

                            newX2 = x1  + dx
                            newY2 = y1 + dy
                            

                            if angleNeeded:
                                line = lineAngle(first_click, (newX2, newY2))

                            else:
                                line = Line(first_click, (x1 + dx, y1 + dy), False)

                            lines.append(line)
                        
                        lengthNeeded = False
                        mode = MODE_NONE

                    else:
                        second_click = snapTo(second_click, "Line")
                        line = Line(first_click, second_click, False)

                        if angleNeeded:
                            line = lineAngle(first_click, second_click)

                        lines.append(line)
                        mode = MODE_NONE

                    lineSize.hide()
                    lineSize.reset()

            elif mode == MODE_CIRCLE:
                
                slipButton.show()
                pressFit.show()

                if not waiting_for_second_click_circle:
                    waiting_for_second_click_circle = True
                    first_click = event.pos

                    if is_point_forbidden(first_click):
                        waiting_for_second_click_circle = False
                        print('Cannot draw in forbidden zone')
                    else:
                        first_click = snapTo(first_click, "Circle")  

                    slipButton.setX(first_click[0] + 20)
                    slipButton.setY(first_click[1] - 50)

                    pressFit.setX(first_click[0] + 20)
                    pressFit.setY(first_click[1])

                else:
                    second_click = event.pos
                   
                    waiting_for_second_click_circle = False
                    
                    if is_point_forbidden(second_click):
                        waiting_for_second_click_circle = True
                        print('Cannot draw in forbidden zone')          

                    else:  
                        rad = math.sqrt(math.pow(second_click[0] - first_click[0], 2) + math.pow(second_click[1] - first_click[1], 2))
                        circles.append(Circle(first_click, rad, False))
                        mode = MODE_NONE 

                    pressFit.hide()
                    slipButton.hide()

            elif mode == MODE_ERASER:
                click = event.pos

                for line in lines:
                    if line.frozen:
                        continue

                    toErase = eraseLine(line.p1, line.p2, click)

                    if toErase:
                        lines.remove(line)

                
                for circle in circles:

                    if circle.frozen:
                        continue

                    toErase = eraseCircle(circle, click)

                    if toErase:
                        circles.remove(circle)


                mode = MODE_NONE

            elif mode == MODE_BOX:

                #squareSizeDropdown.show()
                #squareRelease.show()

                if not waiting_for_second_box_click:
                    waiting_for_second_box_click = True
                    first_click = event.pos
                    if is_point_forbidden(first_click):
                        waiting_for_second_box_click = False
                        print('Cannot draw in forbidden zone')
                    
                    else:
                        first_click = snapTo(first_click, "Line")  

                    #squareSizeDropdown.setX(first_click[0] + 20)
                    #squareSizeDropdown.setY(first_click[1] - 50)

                    #squareRelease.setX(first_click[0] + 20)
                    #squareRelease.setY(first_click[1] - 50)

                else:
                    second_click = event.pos
                    waiting_for_second_box_click = False
                    if is_point_forbidden(second_click):
                        waiting_for_second_box_click = True
                        print('Cannot draw in forbidden zone')

                    elif squareLengthNeeded:
                        squareLength = squareSize.getSelected()

                        x1, y1 = first_click
                        x2, y2 = second_click

                        mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

                        sideLen = mag / (math.sqrt(2))

                        xmult = (x2 - x1) / abs((x2 - x1))
                        ymult = (y2 - y1) / abs((y2 - y1))

                        if sideLen < squareLength:
                            l1 = Line(first_click, (first_click[0], first_click[1] + ymult * sideLen), False)
                            l2 = Line(first_click, (first_click[0] + xmult * sideLen, first_click[1]), False)
                            l3 = Line((first_click[0] + xmult * sideLen,  first_click[1]), (first_click[0] + xmult * sideLen, first_click[1] + ymult* sideLen), False)
                            l4 = Line((first_click[0], first_click[1] + ymult * sideLen), (first_click[0] + xmult * sideLen, first_click[1] + ymult * sideLen), False)
                            lines.append(l1)
                            lines.append(l2)
                            lines.append(l3)
                            lines.append(l4)
                    
                        else:   
                            #dx = ((x2 - x1) / mag) * squareLength
                            #dy = ((y2 - y1) / mag) * squareLength

                            l1 = Line(first_click, (first_click[0], first_click[1] + ymult * squareLength), False)
                            l2 = Line(first_click, (first_click[0] + xmult * squareLength, first_click[1]), False)
                            l3 = Line((first_click[0] + xmult * squareLength,  first_click[1]), (first_click[0] + xmult * squareLength, first_click[1] + ymult * squareLength), False)
                            l4 = Line((first_click[0], first_click[1] + ymult * squareLength), (first_click[0] + xmult * squareLength, first_click[1] + ymult * squareLength), False)
                            lines.append(l1)
                            lines.append(l2)
                            lines.append(l3)
                            lines.append(l4)
                        
                        lengthNeeded = False
                        mode = MODE_NONE

                    else:
                        second_click = snapTo(second_click, "Line")  
                        l1 = Line(first_click, (first_click[0], second_click[1]), False)
                        l2 = Line(first_click, (second_click[0], first_click[1]), False)
                        l3 = Line((first_click[0], second_click[1]), second_click, False)
                        l4 = Line((second_click[0], first_click[1]), second_click, False)
                        lines.append(l1)
                        lines.append(l2)
                        lines.append(l3)
                        lines.append(l4)

                        mode = MODE_NONE    

                    #squareSizeDropdown.hide()
                    #squareRelease.hide()
                    squareSize.hide()
                    squareSize.reset()
        
    # DRAW #################################
    
    if not isConnected():
        drawC = pygame.draw.circle(canvas, color = "red", center = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), radius = 10)
    elif isConnected():
        drawC = pygame.draw.circle(canvas, color = "green", center = (SCREEN_WIDTH - 20, SCREEN_HEIGHT - 20), radius = 10)

    if waiting_for_second_click:
        if angleNeeded and lengthNeeded: 
            length = lineSize.getSelected()
            x1, y1 = first_click
            x2, y2 = current_mouse_pos
        
            mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            if length == None:
                pass
            
            elif mag < length:
                pygame.draw.line(canvas, "GREEN", first_click, current_mouse_pos, 2)
                
            else:   
                dx = ((x2 - x1) / mag) * length
                dy = ((y2 - y1) / mag) * length

                newX = first_click[0] + dx
                newY = first_click[1] + dy

                mag = math.sqrt((newX - x1)**2 + (newY - y1)**2)

                
                shortX = newX - x1
                shortY = newY - y1

                shortTheta = math.atan2(shortY, shortX)

                newTheta2 = round(shortTheta / (math.pi / 4)) * (math.pi / 4)

                firstNew = mag * math.cos(newTheta2)
                secondNew = mag * math.sin(newTheta2)

                pygame.draw.line(canvas, "GREEN", first_click, (first_click[0] + firstNew, first_click[1]+ secondNew), 2)

        elif lengthNeeded and not angleNeeded:
            length = lineSize.getSelected()
            x1, y1 = first_click
            x2, y2 = current_mouse_pos
        
            mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            if length == None:
                pass
            elif mag < length:
                pygame.draw.line(canvas, "GREEN", first_click, current_mouse_pos, 2)
                
            else:   
                dx = ((x2 - x1) / mag) * length
                dy = ((y2 - y1) / mag) * length

                pygame.draw.line(canvas, "GREEN", first_click, (first_click[0] + dx, first_click[1]+ dy), 2)
        
        elif angleNeeded and not lengthNeeded:
            x1, y1 = first_click
            x2, y2 = current_mouse_pos

            mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            x = x2 - x1
            y = y2 - y1

            theta = math.atan2(y, x)

            newTheta = round(theta / (math.pi / 4)) * (math.pi / 4)

            firstNew = mag * math.cos(newTheta)
            secondNew = mag * math.sin(newTheta)

            pygame.draw.line(canvas, "GREEN", first_click, (first_click[0] + firstNew, first_click[1] + secondNew), 2)
        

        else:        
            pygame.draw.line(canvas, "GREEN", first_click, current_mouse_pos, 2)
        

    if waiting_for_second_box_click:
        if squareLengthNeeded:
            squareLength = squareSize.getSelected()

            x1, y1 = first_click
            x2, y2 = current_mouse_pos

            mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

            sideLen = mag / (math.sqrt(2))

            if squareLength == 0 or x2-x1 == 0 or y2-y1 == 0:
                pass

            if sideLen < squareLength:
                pygame.draw.line(canvas, "GREEN", first_click, (first_click[0], current_mouse_pos[1]), 2)
                pygame.draw.line(canvas, "GREEN", first_click, (current_mouse_pos[0], first_click[1]), 2)
                pygame.draw.line(canvas, "GREEN", (first_click[0], current_mouse_pos[1]), current_mouse_pos, 2)
                pygame.draw.line(canvas, "GREEN", (current_mouse_pos[0], first_click[1]), current_mouse_pos, 2)
            
            else:
                xmult = (x2 - x1) / abs((x2 - x1))
                ymult = (y2 - y1) / abs((y2 - y1))
                
                pygame.draw.line(canvas, "GREEN", first_click, (first_click[0], first_click[1] + ymult * squareLength), 2)
                pygame.draw.line(canvas, "GREEN", first_click, (first_click[0] + xmult * squareLength, first_click[1]), 2)
                pygame.draw.line(canvas, "GREEN", (first_click[0] + xmult * squareLength,  first_click[1]), (first_click[0] + xmult * squareLength, first_click[1] + ymult * squareLength), 2)
                pygame.draw.line(canvas, "GREEN", (first_click[0], first_click[1] + ymult * squareLength), (first_click[0] + xmult * squareLength, first_click[1] + ymult * squareLength), 2)


        else:
            pygame.draw.line(canvas, "GREEN", first_click, (first_click[0], current_mouse_pos[1]), 2)
            pygame.draw.line(canvas, "GREEN", first_click, (current_mouse_pos[0], first_click[1]), 2)
            pygame.draw.line(canvas, "GREEN", (first_click[0], current_mouse_pos[1]), current_mouse_pos, 2)
            pygame.draw.line(canvas, "GREEN", (current_mouse_pos[0], first_click[1]), current_mouse_pos, 2)
        
    if waiting_for_second_click_circle:
        current_rad = math.sqrt(math.pow(current_mouse_pos[0] - first_click[0], 2) + math.pow(current_mouse_pos[1] - first_click[1], 2))
        pygame.draw.circle(canvas, "ORANGE", first_click, current_rad, width=2)

    for zone in forbidden_regions:
        zone.draw()
        
    for line in lines:
        line.draw()

    for circle in circles:
        circle.draw()

    for snap in snaps:
        snap.draw()

    





                
