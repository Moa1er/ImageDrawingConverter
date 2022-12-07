import tkinter as tk
import random
from PIL import Image
import time

import sys
sys.setrecursionlimit(200000)

start_time = time.time()

## WINDOWS
# to launch in debug mode
imgToDraw = Image.open('assets-test\\smile-face-medium-large.png')
# to launch normaly
# imgToDraw = Image.open('..\\assets-test\\smile-face.png')
## LINUX
# imgToDraw = Image.open('../assets-test/smile-face-medium-large.png')

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
# isPixelChecked = [[ False for y in range( imgWidth ) ] for x in range( imgHeight )]

# min tolerable difference between two colors to consider them the same
# the higher the value is the more colors will be considered the same
COLOR_TOLERANCE = 10

actualX = 0

debugImg  = Image.new( mode = "RGB", size = (imgWidth, imgHeight))
debugPixels = debugImg.load()

root = tk.Tk()
canvas = tk.Canvas(root, height=imgHeight, width=imgWidth)
canvas.pack()

class Element:
    def __init__(self, color):
        self.pixels = [];
        self.color = color;
    
    def addPixel(self, pixel):
        self.pixels.append(pixel);

class Pixel:
  def __init__(self, x, y, color):
    self.x = x # x position of the pixel
    self.y = y # y position of the pixel
    self.color = color # color is a tuple (r,g,b)

def draw_point():
    global actualX
    if(len(elements) <= 0):
        return
    if(actualX >= len(elements[0].pixels)):
        return
    canvas.create_rectangle((elements[0].pixels[actualX].x, elements[0].pixels[actualX].y, elements[0].pixels[actualX].x + 1, elements[0].pixels[actualX].y + 1), fill='red', width=1)
    actualX += 1
    root.after(1, draw_point)

def cutImageInElements():
    print("cutImageInElements");
    for x in range(0, imgWidth):
        for y in range(0, imgHeight):
            if x == 63 and y == 66:
                print("debug")
                print("Actual: ", imgPixels[x, y])
                print("Next y: ", imgPixels[x, y + 1])
                print("Next x: ", imgPixels[x + 1, y])

            actualPixel = Pixel(x, y, imgPixels[x, y]);
            idxElement = getIdxPartOfOneElement(actualPixel)
            if(idxElement != -1):
                if idxElement == 0:
                    debugPixels[x, y] = elements[idxElement].color
                elements[idxElement].addPixel(actualPixel);
            else:
                elements.append(Element(actualPixel.color));
                elements[len(elements) - 1].addPixel(actualPixel);

    debugImg.show()

def getIdxPartOfOneElement(pixel):
    if pixel.x == 25 and pixel.y == 60:
        print("debug")
    for i in range(0, len(elements)):
        for j in range(0, len(elements[i].pixels)):
            if(doesPixelsTouch(elements[i].pixels[j], pixel) and isColorAlmostSame(elements[i].pixels[j].color, pixel.color)):
                return i;
    return -1
    
def doesPixelsTouch(pixel1, pixel2):
    if(pixel1.x == pixel2.x and pixel1.y == pixel2.y):
        return False
    if(pixel1.x == pixel2.x and abs(pixel1.y - pixel2.y) == 1):
        return True
    if(pixel1.y == pixel2.y and abs(pixel1.x - pixel2.x) == 1):
        return True
    return False

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

    
if __name__ == '__main__':
    cutImageInElements();
    print("--- %s seconds ---" % (time.time() - start_time))
    draw_point()
    root.mainloop()