import random
import string
import math
import copy
from drawingClasses import *

# function that fills the debug img with the elements
def drawElements(elements: List[Element], imgPixels):
    for element in elements:
        for pixel in element.pixels:
            imgPixels[pixel.x, pixel.y] = element.color


def get_random_string(length: int):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

# def pixelForDrawing(elements: List[Element]):
#     global allPointsInOrder
#     for element in elements:
#         for line in element.edgeLines:
#             for pixel in line.pixelsCoord:
#                 allPointsInOrder.append(pixel)

def pixelForDrawing(allPointsInOrder, lines):
    for line in lines:
        for pixel in line.pixelsCoord:
            allPointsInOrder.append(pixel)

def sortLines(lines: set) -> List[Line]:
    linesSorted: List[Line] = []
    startingPoint: tuple = (0, 0)
    while(len(lines) > 0):
        startingPoint, closestLine = calculateClosestLine(startingPoint, lines)
        if closestLine is not None:
            lines.remove(closestLine)
            linesSorted.append(closestLine)
    return linesSorted
    
# funtion that calculate the closest line comparing the starting point with the first point of the line
def calculateClosestLine(startingPoint: tuple, lines: set):
    minDist = 100000000
    minLine = None
    for line in lines:
        dist = math.dist(startingPoint, line.pixelsCoord[0])
        if(dist < minDist):
            minDist = dist
            minLine = line
    return minLine.pixelsCoord[len(minLine.pixelsCoord) - 1], minLine

def rmTouchingLines(lines: List[Line]):
    newLines = set()
    didBreak = False
    while(len(lines) > 0):
        print(len(lines))
        line = lines.pop()
        didBreak = False
        for pixelCoord in line.pixelsCoord:
            linesCpy = copy.deepcopy(lines)
            while(len(linesCpy) > 0):
                cmpLine = linesCpy.pop()
                idxPop = len(linesCpy)
                for (s, t) in ((pixelCoord[0] + 1, pixelCoord[1]), (pixelCoord[0] - 1, pixelCoord[1]), (pixelCoord[0], pixelCoord[1] + 1), (pixelCoord[0], pixelCoord[1] - 1)):
                    if (s, t) not in cmpLine.pixelsCoordSet:
                        continue
                    lines.pop(idxPop)
                    idxPixel = cmpLine.pixelsCoord.index((s, t))
                    newLine1 = Line(cmpLine.pixelsCoord[:idxPixel])
                    newLine2 = Line(cmpLine.pixelsCoord[idxPixel + 1:])
                    if(len(newLine1.pixelsCoord) > 0):
                        lines.append(newLine1)
                        linesCpy.append(newLine1)
                    if(len(newLine2.pixelsCoord) > 0):
                        lines.append(newLine2)
                        linesCpy.append(newLine2)
                    didBreak = True
                    break
        newLines.add(line)
    return newLines