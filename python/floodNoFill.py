from typing import List
from PIL import Image

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


"""
Fills array with all pixel connected to the seed point (xy) with the same color.

:param image: Target image.
:param xy: Seed position (a 2-item coordinate tuple). See
    :ref:`coordinate-system`.
"""
def floodNofill(pixels, xy, elementToAddTo, debug = False):
    x, y = xy
    try:
        background = pixels[x, y]
        elementToAddTo.addPixel(Pixel(x, y, pixels[x, y]))
        if debug: debugPixels[x, y] = pixels[x, y]
        pixelsChecked.add((x, y))
        if (x, y) in pixelsNotChecked:
            pixelsNotChecked.remove((x, y))
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = {(x, y)}
    # use a set to keep record of current and previous edge pixels
    # to reduce memory consumption
    full_edge = set()
    while edge:
        new_edge = set()
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                # If already processed, or if a coordinate is negative, skip
                if (s, t) in full_edge or s < 0 or t < 0:
                    continue
                try:
                    p = pixels[s, t]
                except (ValueError, IndexError):
                    pass
                else:
                    full_edge.add((s, t))
                    fill = (p == background)
                    if fill:
                        elementToAddTo.addPixel(Pixel(s, t, pixels[s, t]))
                        if debug: debugPixels[s, t] = elementToAddTo.color
                        new_edge.add((s, t))
                        pixelsChecked.add((s, t))
                        if (s, t) in pixelsNotChecked:
                            pixelsNotChecked.remove((s, t))
                    else:
                        if (s, t) not in pixelsChecked:
                            pixelsNotChecked.add((s, t))
        full_edge = edge  # discard pixels processed
        edge = new_edge

"""
Cuts an input image in elements, each element is a part of the image, 
it's a bunch of pixels with the same color

:param image: Target image.
:param xy: Seed position (a 2-item coordinate tuple). See
    :ref:`coordinate-system`.
"""   
def getElemsInImg(imgWidth, imgHeight, imgPixels, debug = False):
    # an element is a part of the image, it's a bunch of pixels with 
    # approximately the same color
    # and each pixel touch at least one other pixel of the same element
    elements = [];

    #creates two sets for the function flooNoFill
    global pixelsChecked
    pixelsChecked = set()
    global pixelsNotChecked
    pixelsNotChecked = set()

    if debug:
        #creates a debug img to see the result
        debugImg  = Image.new(mode="RGB", size=(imgWidth, imgHeight))
        global debugPixels
        debugPixels = debugImg.load()

    pixelsNotChecked.add((0, 0))
    while(len(pixelsNotChecked) > 0):
        startingPoint = pixelsNotChecked.pop()
        while(startingPoint in pixelsChecked):
            if(len(pixelsNotChecked) == 0):
                break
            startingPoint = pixelsNotChecked.pop()
            
        elements.append(Element(imgPixels[startingPoint[0], startingPoint[1]]))
        floodNofill(imgPixels, startingPoint, elements[len(elements) - 1], debug = debug)

    if debug:
        debugImg.show()

    return elements
    