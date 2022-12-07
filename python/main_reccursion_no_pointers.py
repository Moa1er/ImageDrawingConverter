import tkinter as tk
from typing import List
from PIL import Image, ImageDraw

import sys
sys.setrecursionlimit(200000)

## WINDOWS
# to launch in debug mode
# imgToDraw = Image.open('assets-test\\smile-face.png')
# to launch normaly
# imgToDraw = Image.open('assets-test\\smile-face.png')
## LINUX
imgToDraw = Image.open(R'../assets-test/smile-face-300.png').convert("RGB")
imgPixels = imgToDraw.load()

seed = (0, 0)
rep_value = (100, 100, 100)
ImageDraw.floodfill(imgToDraw, seed, rep_value, thresh=50)
imgToDraw.show()




# imgWidth = imgToDraw.size[0]
# imgHeight = imgToDraw.size[1]

# imgPixelsArr = [[ imgPixels[x, y] for y in range( imgHeight ) ] for x in range( imgWidth )]
# print(imgPixelsArr)

# print(imgPixels)
# print(imgToDraw)
# print(imgToDraw.convert("RGB"))
# print(imgToDraw.convert("RGB").load())

# # an element is a part of the image, it's a bunch of pixels with approximately the same color
# # and each pixel touch at least one other pixel of the same element
# elements = [];

# isPixelChecked = [[ False for y in range( imgWidth ) ] for x in range( imgHeight )]

# # debugImg  = Image.new(mode = "RGB", size = (imgWidth, imgHeight))
# # debugPixels = debugImg.load()

# # min tolerable difference between two colors to consider them the same
# # the higher the value is the more colors will be considered the same
# COLOR_TOLERANCE = 10

# reccursionCount = 0

# class Element:
#     def __init__(self, color):
#         self.pixels = [];
#         self.color = color;
    
#     def addPixel(self, pixel):
#         self.pixels.append(pixel);

# class Pixel:
#   def __init__(self, x, y, color):
#     self.x = x # x position of the pixel
#     self.y = y # y position of the pixel
#     self.color = color # color is a tuple (r,g,b)

def floodNoFill(imgPixelsArr: List[List[tuple]], x: int, y: int, newColor: tuple):
    startingPixel = imgPixelsArr[x][y];
    dfs(imgPixelsArr, x, y, newColor, startingPixel)
    # debugImg.show()

def dfs(imgPixelsArr: List[List[tuple]], xStart: int, yStart: int, newColor: tuple, startingPixel: tuple):
    # global reccursionCount
    # reccursionCount += 1

    if(xStart < 0 or xStart >= imgWidth or yStart < 0 or yStart >= imgHeight or imgPixelsArr[xStart][yStart] == newColor or imgPixelsArr[xStart][yStart] != startingPixel):
        return

    # isPixelChecked[yStart][xStart] = True
    # elements[0].addPixel(Pixel(xStart, yStart, imgPixels[xStart, yStart]))
    # debugPixels[xStart, yStart] = startingPixel.color
    imgPixelsArr[xStart][yStart] = newColor
    dfs(imgPixelsArr, xStart, yStart - 1, newColor, startingPixel)
    dfs(imgPixelsArr, xStart, yStart + 1, newColor, startingPixel)
    dfs(imgPixelsArr, xStart - 1, yStart, newColor, startingPixel)
    dfs(imgPixelsArr, xStart + 1, yStart, newColor, startingPixel)


# def isColorAlmostSame(pixel1, pixel2):
#     redDiff = abs(pixel1[0] - pixel2[0])
#     greenDiff = abs(pixel1[1] - pixel2[1])
#     blueDiff = abs(pixel1[2] - pixel2[2])
#     if(redDiff < COLOR_TOLERANCE and greenDiff < COLOR_TOLERANCE and blueDiff < COLOR_TOLERANCE):
#         return True
#     else:
#         return False

# def printPixelsArr(pixelsArr):
#     for x in range(0, len(pixelsArr)):
#         print(pixelsArr[x].x, pixelsArr[x].y, pixelsArr[x].color)
        
# if __name__ == '__main__':
#     # elements.append(Element(imgPixels[0, 0]))
#     floodNoFill(imgPixelsArr, 0, 0, (100, 100, 100));
#     # print("NbReccursive call: ", reccursionCount)
#     print('ended')