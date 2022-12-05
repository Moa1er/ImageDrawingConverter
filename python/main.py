#how to use pil for images
# print (imgToDraw.size)  # Get the width and hight of the image for iterating over
# print (imgPixels[141,127])  # Get the RGBA Value of the a pixel of an image
# print (imgPixels[399,399])
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .

import tkinter as tk
import random
from PIL import Image

import sys
print(sys.setrecursionlimit(200000))

imgToDraw = Image.open('../assets-test/smile-face.png') # Can be many different formats.
imgPixels = imgToDraw.load()

imgWidth = imgToDraw.size[0]
imgHeight = imgToDraw.size[1]

# an element is a part of the image, it's a bunch of pixels with approximately the same color
# and each pixel touch at least one other pixel of the same element
elements = [];

# array to check if a pixel has already been checked
# if a pixel is checked, it means that it's part of an element
# it's not pretty the better way to do it is to use the imgPixels object and set the pixel to a specific color recognisable
# but it's not comphrehensive enough to do it
# TODO : find a better way to do it
isPixelChecked = [[ False for y in range( imgWidth ) ] for x in range( imgHeight )]

# min tolerable difference between two colors to consider them the same
# the higher the value is the more colors will be considered the same
COLOR_TOLERANCE = 10

element = "test"
actualX = 0

debugImg  = Image.new( mode = "RGB", size = (imgWidth, imgHeight))
debugPixels = debugImg.load()

root = tk.Tk()
canvas = tk.Canvas(root, height=400, width=400)
canvas.pack()

    
class Element:
    def __init__(self, firstPixel, color):
        self.pixels = [];
        self.addPixel(firstPixel)
        self.color = color;

    def addPixel(self, pixel):
        self.pixels.append(pixel);

class Pixel:
  def __init__(self, x, y, color):
    self.x = x # x position of the pixel
    self.y = y # y position of the pixel
    self.color = color # color is a tuple (r,g,b)

print(imgPixels[191, 307])    

def draw_point():
    global actualX
    global element
    if(actualX >= len(element.pixels)):
        return
    canvas.create_rectangle((element.pixels[actualX].x, element.pixels[actualX].y, element.pixels[actualX].x + 1, element.pixels[actualX].y + 1), fill='red', width=1)
    actualX += 10
    root.after(1, draw_point)

def cutImageInElements():
    global element
    print("cutImageInElements");
    print(imgPixels[0, 0])

    pixel = Pixel(0, 200, imgPixels[0, 200]);
    element = Element(pixel, pixel.color);
    completeElement(element.pixels)
    debugImg.show()

    # printPixelsArr(element.pixels)
    # completeElemResult = completeElement(element)
    # while(completeElemResult != (-1, -1)):
    #     firstPixel = Pixel(completeElemResult[0], completeElemResult[1], imgPixels[completeElemResult[0], completeElemResult[1]]);
    #     newElement = Element(firstPixel, firstPixel.color);
    #     completeElemResult = completeElement(newElement.pixels)


def completeElement(elemPixels):
    # print("createElement");

    nbPixels = len(elemPixels);
    xIndex = elemPixels[nbPixels - 1].x
    # print(xIndex)
    yIndex = elemPixels[nbPixels - 1].y
    # print(yIndex)
    xRightIdx = elemPixels[nbPixels - 1].x + 1
    # print(xRightIdx)
    xLeftIdx = elemPixels[nbPixels - 1].x - 1
    # print(xLeftIdx)
    yBottomIdx = elemPixels[nbPixels - 1].y + 1
    # print(yBottomIdx)
    yTopIdx = elemPixels[nbPixels - 1].y - 1
    # print(yTopIdx)

    isPixelChecked[xIndex][yIndex] = True
    debugPixels[xIndex, yIndex] = elemPixels[nbPixels - 1].color

    if(xRightIdx < imgWidth and isPixelChecked[xRightIdx][yIndex] == False):
        if(isColorAlmostSame(imgPixels[elemPixels[0].x, elemPixels[0].y], imgPixels[xRightIdx, yIndex])):
            pixelAppended = Pixel(xRightIdx, yIndex, imgPixels[xRightIdx, yIndex])
            elemPixels.append(pixelAppended)
            
            # print("Going right") 
            # print(pixelAppended.x, pixelAppended.y, pixelAppended.color)
            completeElement(elemPixels)
        else:
            return
    
    # if(xLeftIdx >= 0 and isColorAlmostSame(imgPixels[xIndex, yIndex], imgPixels[xLeftIdx, yIndex]) and isPixelChecked[xLeftIdx][yIndex] == False):
    #     pixelAppended = Pixel(xLeftIdx, yIndex, imgPixels[xLeftIdx, yIndex])
    #     elemPixels.append(pixelAppended)

    #     # print("Going left")
    #     # print(pixelAppended.x, pixelAppended.y, pixelAppended.color)
    #     completeElement(elemPixels)

    if(yBottomIdx < imgHeight and isColorAlmostSame(imgPixels[elemPixels[0].x, elemPixels[0].y], imgPixels[xIndex, yBottomIdx]) and isPixelChecked[xIndex][yBottomIdx] == False):
        pixelAppended = Pixel(xIndex, yBottomIdx, imgPixels[xIndex, yBottomIdx])
        elemPixels.append(pixelAppended)

        # print("Going bottom")
        # print(pixelAppended.x, pixelAppended.y, pixelAppended.color)
        completeElement(elemPixels)
    
    if(yTopIdx >= 0 and isColorAlmostSame(imgPixels[elemPixels[0].x, elemPixels[0].y], imgPixels[xIndex, yTopIdx]) and isPixelChecked[xIndex][yTopIdx] == False):
        pixelAppended = Pixel(xIndex, yTopIdx, imgPixels[xIndex, yTopIdx])
        elemPixels.append(pixelAppended)

        # print("Going top")
        # print(pixelAppended.x, pixelAppended.y, pixelAppended.color)
        completeElement(elemPixels)
    

def printPixelsArr(pixelsArr):
    for x in range(0, len(pixelsArr)):
        print(pixelsArr[x].x, pixelsArr[x].y, pixelsArr[x].color)

def isColorAlmostSame(pixel1, pixel2):
    redDiff = abs(pixel1[0] - pixel2[0])
    greenDiff = abs(pixel1[1] - pixel2[1])
    blueDiff = abs(pixel1[2] - pixel2[2])
    if(redDiff < COLOR_TOLERANCE and greenDiff < COLOR_TOLERANCE and blueDiff < COLOR_TOLERANCE):
        return True
    else:
        return False

def testPointer(testArr):
    testArr[0] = 100

    
if __name__ == '__main__':
    cutImageInElements();
    draw_point()
    root.mainloop()