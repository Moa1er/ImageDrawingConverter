from typing import List
from floodNoFill import *

def cleanUpElements(imgWidth, imgHeight, imgPixels, elements: List[Element], nbPixelMin: int):
    global pixelsCantBeUsed
    pixelsCantBeUsed = set()
    for i in range(len(elements)):
        element = elements[i]
        if len(element.pixels) <= nbPixelMin:
            for pixel in element.pixels:
                pixelsCantBeUsed.add((pixel.x, pixel.y))

    nbColorNotFound = 0
    for i in range(len(elements)):
        element = elements[i]
        if len(element.pixels) <= nbPixelMin:
            color = findColorTouchingPixel(imgPixels, element.pixels)
            if color != (-1, -1, -1):
                for pixel in element.pixels:
                    imgPixels[pixel.x, pixel.y] = color
            else:
                nbColorNotFound += 1
    elements = getElemsInImg(imgWidth, imgHeight, imgPixels, debug = False)
    return elements

def findColorTouchingPixel(imgPixels, pixelsToCmp: List[Pixel]):
    for pixel in pixelsToCmp:
        edge = {(pixel.x, pixel.y)}
        # use a set to keep record of current and previous edge pixels
        # to reduce memory consumption
        full_edge = set()
        while edge:
            new_edge = set()
            for (x, y) in edge:  # 8 adjacent method
                for (s, t) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1), (x + 1, y + 1), (x - 1, y - 1), (x + 1, y - 1), (x - 1, y + 1)):
                    # If already processed, or if a coordinate is negative, skip
                    if (s, t) in full_edge or s < 0 or t < 0:
                        continue
                    try:
                        color = imgPixels[s, t]
                    except (ValueError, IndexError):
                        pass
                    else:
                        full_edge.add((s, t))
                        if color != pixel.color and ((s, t) not in pixelsCantBeUsed):
                            return color
                        else:
                            new_edge.add((s, t))
            full_edge = edge  # discard pixels processed
            edge = new_edge
    return (-1, -1, -1)