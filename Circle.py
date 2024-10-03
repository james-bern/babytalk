import pygame
import sys
import math

class Circle:

    def __init__(self, canvas):
        self.circles = []
        self.canvas = canvas

    def drawCircle(self):
        points = []
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Add the position of the click to the points list
                    points.append(pygame.mouse.get_pos())
                
                    # If two points are clicked, draw the line
                    if len(points) == 2:
                        rad = math.sqrt(math.pow(points[1][0] - points[0][0], 2) + math.pow(points[1][1] - points[0][1], 2))
                        pygame.draw.circle(self.canvas, color = "blue", center = points[0], radius = rad , width = 2)
                        coords = (points[0], rad)
                        self.circles.append(coords)
                        pygame.display.flip()
                        running = False