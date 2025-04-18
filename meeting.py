# TODO: numpy 2D arrays might be useful?

import pygame
import sys
import os
import math
import pygame_widgets
from pygame_widgets.button import Button



pygame.init()
os.system('clear')

########################################

canvas = pygame.display.set_mode((512, 512)) 
clock = pygame.time.Clock()
event_queue = None


button = Button(
    # Mandatory Parameters
    canvas,  # Surface to place button on
    100,  # X-coordinate of top left corner
    100,  # Y-coordinate of top left corner
    300,  # Width
    150,  # Height

    # Optional Parameters
    text = 'Test',  # Text to display
    fontSize = 50,  # Size of font
    margin = 20,  # Minimum distance between text/image and edge of button
    inactiveColour = (200, 50, 0),  # Colour of button when not being interacted with
    hoverColour = (150, 0, 0),  # Colour of button when being hovered over
    pressedColour=(0, 200, 20),  # Colour of button when being clicked
    radius=20,  # Radius of border corners (leave empty for not curved)
    onClick=lambda: print('Click')  # Function to call when clicked on
)


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

button.hide()

########################################

class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

########################################

lines = []
rects=[]

########################################

if (True):
    lines.append(Line((0, 0), (100, 100)))
    lines.append(Line((100, 100), (300, 200)))
    lines.append(Line((100, 100), (100, 200)))

    lines.append(Line((80,80), (80, 140)))
    lines.append(Line((80,80), (140, 80)))
    lines.append(Line((80,140), (140, 140)))
    lines.append(Line((140,80), (140, 140)))

########################################

MODE_NONE   = 0
MODE_LINE   = 1
MODE_BOX    = 2
MODE_CIRCLE = 3

MODE = 4

mode = MODE_NONE
waiting_for_second_click = False
waiting_for_second_click_length = False
first_click = None

waiting_for_second_click_box = False
waiting_for_second_click_length_box = False

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
    
    # Calculate endpoints for first parallel line (offset by +distance)
    line1_x1 = round(x1 + perpx * distance, 3)
    line1_y1 = round(y1 + perpy * distance, 3)
    line1_x2 = round(x2 + perpx * distance, 3)
    line1_y2 = round(y2 + perpy * distance, 3)
    
    # Calculate endpoints for second parallel line (offset by -distance)
    line2_x1 = round(x1 - perpx * distance, 3)
    line2_y1 = round(y1 - perpy * distance, 3)
    line2_x2 = round(x2 - perpx * distance, 3)
    line2_y2 = round(y2 - perpy * distance, 3)
    
    # return [Line((line1_x1, line1_y1), (line1_x2, line1_y2)), Line((line2_x1, line2_y1),(line2_x2, line2_y2))]
    
    return (line1_x1, line1_y1), (line1_x2, line1_y2), (line2_x1, line2_y1), (line2_x2, line2_y2)
    

########################################

while beginFrame():

    # USER INPUT & UPDATE ##################

    for event in event_queue:
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN and MODE == 1:
            if not waiting_for_second_click:
                waiting_for_second_click = True
                first_click = event.pos
            else: 
                second_click = event.pos
                waiting_for_second_click = False
                lines.append(Line(first_click, second_click))

                #if mode == MODE_LINE:
                #    lines.append(Line(first_click, second_click))
                #elif mode == MODE_CIRCLE:
                #    pass

        if event.type == pygame.MOUSEBUTTONDOWN and MODE == 2:
            
            click = event.pos

            for line in lines:
                p1_x, p1_y = line.p1
                p2_x, p2_y = line.p2

                p1_pos, p2_pos, p1_neg, p2_neg = get_parallel_lines(p1_x, p1_y, p2_x, p2_y)
                points = [p1_pos, p2_pos, p2_neg, p1_neg]
                
                #rects.append(points)   

                if is_point_in_polygon(click, points):
                    lines.remove(line)
                else:
                    print("Click is outside polygon!")

                # trueFalse = is_point_in_rectangle(click, [p1_pos, p2_pos, p1_neg, p2_neg])
                #print(trueFalse)

        if event.type == pygame.MOUSEBUTTONDOWN and MODE == 3:

            length = 40.0

            if not waiting_for_second_click_length:
                waiting_for_second_click_length = True
                first_click = event.pos

            else:
                second_click = event.pos
                waiting_for_second_click_length = False

                x1, y1 = first_click
                x2, y2 = second_click

               
                mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

                if mag < length:
                    lines.append(Line(first_click, second_click))
            
                else:   
                    dx = ((x2 - x1) / mag) * length
                    dy = ((y2 - y1) / mag) * length


                    lines.append(Line(first_click, (x1 + dx, y1 + dy)))


               #lines.append(Line(first_click, second_click))
            
        if event.type == pygame.MOUSEBUTTONDOWN and MODE == 4:
            length = 100.0

            if not waiting_for_second_click_length_box:
                waiting_for_second_click_length_box = True
                first_click = event.pos

            else:
                second_click = event.pos
                waiting_for_second_click_length_box = False

                x1, y1 = first_click
                x2, y2 = second_click

               
                mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

                sideLen = (mag * (math.sqrt(2))) / 2

                xmult = (x2 - x1) / abs((x2 - x1))
                ymult = (y2 - y1) / abs((y2 - y1))

                if sideLen < length:
                    l1 = Line(first_click, (first_click[0], first_click[1] + ymult * sideLen))
                    l2 = Line(first_click, (first_click[0] + xmult* sideLen, first_click[1]))
                    l3 = Line((first_click[0] + xmult* sideLen,  first_click[1]), (first_click[0] + xmult * sideLen, first_click[1] + ymult* sideLen))
                    l4 = Line((first_click[0], first_click[1] + ymult * sideLen), (first_click[0] + xmult * sideLen, first_click[1] + ymult * sideLen))
                    lines.append(l1)
                    lines.append(l2)
                    lines.append(l3)
                    lines.append(l4)
            
                else:   
                    l1 = Line(first_click, (first_click[0], first_click[1] + ymult * length))
                    l2 = Line(first_click, (first_click[0] + xmult * length, first_click[1]))
                    l3 = Line((first_click[0] + xmult* length,  first_click[1]), (first_click[0] + xmult * length, first_click[1] + ymult * length))
                    l4 = Line((first_click[0], first_click[1] + ymult * length), (first_click[0] + xmult * length, first_click[1] + ymult * length))
                    lines.append(l1)
                    lines.append(l2)
                    lines.append(l3)
                    lines.append(l4)


    pygame_widgets.update(event)
    # DRAW #################################

    current_mouse_pos = pygame.mouse.get_pos()

    if waiting_for_second_click:
        pygame.draw.line(canvas, "BLUE", first_click, current_mouse_pos, 2)

    if waiting_for_second_click_length:

        x1, y1 = first_click
        x2, y2 = current_mouse_pos
      
        mag = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)

        if mag < length:
             pygame.draw.line(canvas, "BLUE", first_click, current_mouse_pos, 2)
            
        else:   
            dx = ((x2 - x1) / mag) * length
            dy = ((y2 - y1) / mag) * length

            pygame.draw.line(canvas, "BLUE", first_click, (first_click[0] + dx, first_click[1]+ dy), 2)

        #pygame.draw.line(canvas, "BLUE", first_click, current_mouse_pos, 2)

    if waiting_for_second_click_length_box:
        pygame.draw.line(canvas, "GREEN", first_click, (first_click[0], current_mouse_pos[1]), 2)
        pygame.draw.line(canvas, "GREEN", first_click, (current_mouse_pos[0], first_click[1]), 2)
        pygame.draw.line(canvas, "GREEN", (first_click[0], current_mouse_pos[1]), current_mouse_pos, 2)
        pygame.draw.line(canvas, "GREEN", (current_mouse_pos[0], first_click[1]), current_mouse_pos, 2)

    

    for line in lines:
        pygame.draw.line(canvas, "RED", line.p1, line.p2, 2)

    for rect in rects:
        pygame.draw.polygon(canvas, "GREEN", rect, 2)

