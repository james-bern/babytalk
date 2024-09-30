import pygame
import sys

clock = pygame.time.Clock()

class Line:

    def __init__(self, canvas, boxWidth, center, wallWidth):
        self.lines = []
        self.canvas = canvas
        self.boxWidth = boxWidth
        (self.centerX, self.centerY) = center
        self.wallWidth = wallWidth


    # function designed to snap clicked points to those on the non-editable goemetry
    def hardcodeSnap(self, point):
        (x,y) = point

        #inside square
        if x > (self.centerX - (self.boxWidth + 25)) and x < (self.centerX - (self.boxWidth - 25)) and y > (self.centerY - (self.boxWidth + 25)) and y < (self.centerY - (self.boxWidth - 25)):
            x = (self.centerX - self.boxWidth)
            y = (self.centerY - self.boxWidth)
        if x > (self.centerX - (self.boxWidth + 25)) and x < (self.centerX - (self.boxWidth - 25)) and y > (self.centerY + (self.boxWidth - 25)) and y < (self.centerY + (self.boxWidth + 25)):
            x = (self.centerX - self.boxWidth)
            y = (self.centerY + self.boxWidth)
        if x > (self.centerX + (self.boxWidth - 25)) and x < (self.centerX + (self.boxWidth + 25)) and y > (self.centerY - (self.boxWidth + 25)) and y < (self.centerY - (self.boxWidth - 25)):
            x = (self.centerX + self.boxWidth)
            y = (self.centerY - self.boxWidth)
        if x > (self.centerX + (self.boxWidth - 25)) and x < (self.centerX + (self.boxWidth + 25)) and y > (self.centerY + (self.boxWidth - 25)) and y < (self.centerY + (self.boxWidth + 25)):
            x = (self.centerX + self.boxWidth)
            y = (self.centerY + self.boxWidth)

        #outside square
        #left side
        if x > (self.centerX - (self.boxWidth + self.wallWidth) - 25) and x < (self.centerX - (self.boxWidth + self.wallWidth) + 25) and y > (self.centerY - (self.boxWidth + self.wallWidth) - 25) and y < (self.centerY - (self.boxWidth + self.wallWidth) + 25):
            x = (self.centerX - self.boxWidth - self.wallWidth)
            y = (self.centerY - self.boxWidth - self.wallWidth)
        if x > (self.centerX - (self.boxWidth + self.wallWidth) - 25) and x < (self.centerX - (self.boxWidth + self.wallWidth) + 25) and y > (self.centerY + (self.boxWidth + self.wallWidth) - 25) and y < (self.centerY + (self.boxWidth + self.wallWidth) + 25):
            x = (self.centerX - self.boxWidth - self.wallWidth)
            y = (self.centerY + self.boxWidth + self.wallWidth)

        #right side
        if x > (self.centerX + (self.boxWidth + self.wallWidth) - 25) and x < (self.centerX + (self.boxWidth + self.wallWidth) + 25) and y > (self.centerY - (self.boxWidth + self.wallWidth) - 25) and y < (self.centerY - (self.boxWidth + self.wallWidth) + 25):
            x = (self.centerX + self.boxWidth + self.wallWidth)
            y = (self.centerY - self.boxWidth - self.wallWidth)
        if x > (self.centerX + (self.boxWidth + self.wallWidth) - 25) and x < (self.centerX + (self.boxWidth + self.wallWidth) + 25) and y > (self.centerY + (self.boxWidth + self.wallWidth) - 25) and y < (self.centerY + (self.boxWidth + self.wallWidth) + 25):
            x = (self.centerX + self.boxWidth + self.wallWidth)
            y = (self.centerY + self.boxWidth + self.wallWidth)

        return (x,y)

    def click(self, xy):
        pygame.draw.circle(self.canvas, color = "blue", center = xy, radius = 4, width = 2)

    # Main function
    def drawLine(self, num):
        points = []
        running = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                current = pygame.mouse.get_pos()

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Add the position of the click to the points list
                    xy = pygame.mouse.get_pos()
                    points.append(xy)
                    self.click(xy)

                    if len(points) == 1:
                        p1 = points[0]
                        if num == 2:
                            p1 = self.hardcodeSnap(p1)


                    if len(points) == 2:
                        p2 = points[1]
                        if num == 2:
                            p2 = self.hardcodeSnap(p2)
                        pygame.draw.line(self.canvas, color = "red", start_pos = p1, end_pos = p2, width = 2)
                        coords = (points[0], points[1])
                        self.lines.append(coords)
                        pygame.display.flip()
                        running = False


        
