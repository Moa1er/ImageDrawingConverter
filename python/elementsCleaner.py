from typing import List
from floodNoFill import *

# function that deletes the element that have less than 10 pixels and replace those pixels
# with the color aroung them
# def cleanUpElements(elements: List[Element]) -> List[Element]:
#     for element in elements:
#         if len(element.pixels) < 10:
#             elements.remove(element)
#             idxElemTouching = findIdxElemTouchingPixel(element.pixels[0], elements)
#             if idxElemTouching != -1:
#                 for pixel in element.pixels:
#                     pixel.color = elements[idxElemTouching].color
#                     elements[idxElemTouching].addPixel(pixel)
#             else:
#                 print("error, no element touching")
#     return elements

# def findIdxElemTouchingPixel(pixelToCmp: Pixel, elements: List[Element]) -> int:
#     for element in elements:
#         for pixel in element.pixels:
#             if (pixelToCmp.x == pixel.x and pixelToCmp.y == pixel.y - 1) or (pixelToCmp.x == pixel.x and pixelToCmp.y == pixel.y + 1) or (pixelToCmp.x == pixel.x - 1 and pixelToCmp.y == pixel.y) or (pixelToCmp.x == pixel.x + 1 and pixelToCmp.y == pixel.y):
#                 return elements.index(element)
#     return -1

def cleanUpElements(imgWidth, imgHeight, imgPixels, elements: List[Element], nbPixelMin: int):
    nbElemRm = 0
    for i in range(len(elements)):
        element = elements[i]
        if len(element.pixels) <= nbPixelMin:
            nbElemRm += 1
            color = findColorTouchingPixel(imgWidth, imgHeight, imgPixels, element.pixels)
            if color != (-1, -1, -1):
                for pixel in element.pixels:
                    imgPixels[pixel.x, pixel.y] = color
    elements = getElemsInImg(imgWidth, imgHeight, imgPixels, debug = False)
    return elements

def findColorTouchingPixel(imgWidth, imgHeight, imgPixels, pixelsToCmp: List[Pixel]):
    for pixel in pixelsToCmp:
        xLeft = pixel.x - 1
        xRight = pixel.x + 1
        yUp = pixel.y - 1
        yDown = pixel.y + 1
        if xLeft >= 0:
            colorLeft = imgPixels[pixel.x - 1, pixel.y]
            if(colorLeft != pixel.color):
                return colorLeft
        if xRight < imgWidth:
            colorRight = imgPixels[pixel.x + 1, pixel.y]
            if(colorRight != pixel.color):
                return colorRight
        if yUp >= 0:
            colorUp = imgPixels[pixel.x, pixel.y - 1]
            if(colorUp != pixel.color):
                return colorUp
        if yDown < imgHeight:
            colorDown = imgPixels[pixel.x, pixel.y + 1]
            if(colorDown != pixel.color):
                return colorDown
    return (-1, -1, -1)