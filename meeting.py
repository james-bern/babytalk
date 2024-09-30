# TODO: numpy 2D arrays might be useful?

import pygame
import sys
import os

pygame.init()
os.system('clear')

########################################

canvas = pygame.display.set_mode((512, 512)) 
clock = pygame.time.Clock()
event_queue = None

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
        self.p1 = p1;
        self.p2 = p2;

########################################

lines = []

########################################

if (True):
    lines.append(Line((0, 0), (100, 100)))
    lines.append(Line((100, 100), (300, 200)))

########################################

MODE_NONE   = 0
MODE_LINE   = 1
MODE_BOX    = 2
MODE_CIRCLE = 3

mode = MODE_NONE
waiting_for_second_click = False
first_click = None

########################################

while beginFrame():

    # USER INPUT & UPDATE ##################

    for event in event_queue:
        if event.type == pygame.KEYDOWN:
            pass
        if event.type == pygame.MOUSEBUTTONDOWN:
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


    # DRAW #################################

    current_mouse_pos = pygame.mouse.get_pos()

    if waiting_for_second_click:
        pygame.draw.line(canvas, "BLUE", first_click, current_mouse_pos, 2)

    for line in lines:
        pygame.draw.line(canvas, "RED", line.p1, line.p2, 2)

