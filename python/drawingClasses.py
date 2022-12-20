from typing import List

# a line as an array of pixelsCoord (x, y) that are connected
class Line:
    def __init__(self, pixelsCoord: List[tuple] = []):
        # pixels in order that why this is not a set
        self.pixelsCoord = pixelsCoord
        self.pixelsCoordSet = set()
        self.avgXY = (0, 0)
    
    def calculateAvgXY(self):
        x = 0
        y = 0
        for (x, y) in self.pixelsCoord:
            x += x
            y += y
        self.avgXY = (x / len(self.pixelsCoord), y / len(self.pixelsCoord))

class Pixel:
  def __init__(self, x: int, y: int, color: tuple):
    self.x = x # x position of the pixel
    self.y = y # y position of the pixel
    self.color = color # color is a tuple (r,g,b)
    
class Element:
    def __init__(self, color: tuple):
        self.color = color;
        self.pixels = [];
        self.edgePixels = [];
        self.edgeLines = [];
    def addPixel(self, pixel: Pixel):
        self.pixels.append(pixel);
    
    def getEdgesPixels(self):
        pixelsSet = set()
        for pixel in self.pixels:
            pixelsSet.add((pixel.x, pixel.y))
        
        edgePixelsSet = set()
        for pixel in self.pixels:
            if self.isEdgePixel(pixel, pixelsSet):
                edgePixelsSet.add((pixel.x, pixel.y))
                self.edgePixels.append(pixel)
        
        # now we have all the edge pixels, we create the lines to draw
        while(len(edgePixelsSet) > 0):
            startPixelCoord = edgePixelsSet.pop()
            self.createLine(startPixelCoord, edgePixelsSet)

    def isEdgePixel(self, pixel: Pixel, pixelsAsSet: set):
        for (s, t) in ((pixel.x + 1, pixel.y), (pixel.x - 1, pixel.y), (pixel.x, pixel.y + 1), (pixel.x, pixel.y - 1), (pixel.x + 1, pixel.y + 1), (pixel.x - 1, pixel.y - 1), (pixel.x + 1, pixel.y - 1), (pixel.x - 1, pixel.y + 1)):
            if (s, t) not in pixelsAsSet:
                return True
        return False
    
    def createLine(self, startPixelCoord: tuple, edgePixelsSet: set):
        line = Line()
        # getting all the pixels coords for each line
        pixelsCoordUpRight = []
        nextPixelCoordUpRight = self.getUpRightEdgePixel(startPixelCoord, edgePixelsSet)
        while nextPixelCoordUpRight != (-1, -1):
            pixelsCoordUpRight.append(nextPixelCoordUpRight)
            edgePixelsSet.remove(nextPixelCoordUpRight)
            nextPixelCoordUpRight = self.getNextEdgePixel(nextPixelCoordUpRight, edgePixelsSet)
        pixelsCoordDownLeft = []
        nextPixelCoordDownLeft = self.getDownLeftEdgePixel(startPixelCoord, edgePixelsSet)
        while nextPixelCoordDownLeft != (-1, -1):
            pixelsCoordDownLeft.append(nextPixelCoordDownLeft)
            edgePixelsSet.remove(nextPixelCoordDownLeft)
            nextPixelCoordDownLeft = self.getNextEdgePixel(nextPixelCoordDownLeft, edgePixelsSet)
        # order the pixels coords in the line to have only one direction (no forks when drawing the line)
        pixelsCoordDownLeft.reverse()
        # adding the pixels coords to the line
        line.pixelsCoord = pixelsCoordDownLeft + [startPixelCoord] + pixelsCoordUpRight
        line.pixelsCoordSet = set(line.pixelsCoord)
        # calculate the average x and y for the line
        line.calculateAvgXY()
        self.edgeLines.append(line)

    def getNextEdgePixel(self, pixelCoord: tuple, edgePixelsSet):
        for (s, t) in ((pixelCoord[0] + 1, pixelCoord[1]), (pixelCoord[0] - 1, pixelCoord[1]), (pixelCoord[0], pixelCoord[1] + 1), (pixelCoord[0], pixelCoord[1] - 1)):
            if (s, t) in edgePixelsSet:
                return (s, t)
        return (-1, -1)
    def getUpRightEdgePixel(self, pixelCoord: tuple, edgePixelsSet):
        for (s, t) in ((pixelCoord[0] + 1, pixelCoord[1]), (pixelCoord[0], pixelCoord[1] + 1)):
            if (s, t) in edgePixelsSet:
                return (s, t)
        return (-1, -1)
    def getDownLeftEdgePixel(self, pixelCoord: tuple, edgePixelsSet):
        for (s, t) in ((pixelCoord[0] - 1, pixelCoord[1]), (pixelCoord[0], pixelCoord[1] - 1)):
            if (s, t) in edgePixelsSet:
                return (s, t)
        return (-1, -1)
