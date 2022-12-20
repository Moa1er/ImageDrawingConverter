import tkinter as tk
from PIL import Image
import time
from imgColorSwap import *
from colorExtraction import *
from floodNoFill import *
from elementsCleaner import *
from drawingClasses import *
from utilityFuncs import *

start_time_total = time.time()
start_time = time.time()

imgName = "woman-bar-chosen-colors-20-200-20"
imgName = "woman-bar-chosen-colors-20-200-20"
imgPath = R'../assets-test/' + imgName + ".png"
# imgPath = R'assets-test\\' + imgName + '.png'

imgToDraw = Image.open(imgPath)
# imgToDraw = Image.open(R'../assets-test/smile-face.png')
# imgToDraw = Image.open('assets-test\\smile-face.png')
imgPixels = imgToDraw.load()

imgWidth = imgToDraw.size[0]
imgHeight = imgToDraw.size[1]

#creates a debug img to see the result
# debugImg  = Image.new(mode="RGB", size=(imgWidth, imgHeight))
# debugPixels = debugImg.load()

# creates a canvas to draw the result
root = tk.Tk()
canvas = tk.Canvas(root, height=imgHeight/2, width=imgWidth/2)
canvas.pack()

## constants part

# for woman-bar.png
# NB_COLOR_TO_EXTRACT = 20
# NB_MIN_PIXELS_PER_ELEM = 200
# TRESHOLD_COLOR_DIFF = 20

# for smile-face.png
NB_COLOR_TO_EXTRACT = 5
NB_MIN_PIXELS_PER_ELEM = 10
TRESHOLD_COLOR_DIFF = 50

# for smile-face-small.png
NB_COLOR_TO_EXTRACT = 5
NB_MIN_PIXELS_PER_ELEM = 0
TRESHOLD_COLOR_DIFF = 50

actualIdx = 0
allPointsInOrder = []

# function used to draw each point of the image on the canvas
def draw_point():
    global actualIdx
    global allPointsInOrder
    if(actualIdx >= len(allPointsInOrder)):
        print("Total time to draw img: %s seconds" % (time.time() - start_time_total))
        return
    canvas.create_rectangle((allPointsInOrder[actualIdx][0]/2, allPointsInOrder[actualIdx][1]/2, allPointsInOrder[actualIdx][0]/2, allPointsInOrder[actualIdx][1]/2), fill='red', width=1)
    actualIdx += 1
    root.after(1, draw_point)

if __name__ == '__main__':
    ## PART TO CHANGE THE COLORS OF THE IMAGE TO A GIVEN NUMBER OF COLORS
    # the two next commented function produced the result img woman-bar-20-colors.png
    # listColors: tuple = getListColorsInImg(imgPath, TRESHOLD_COLOR_DIFF, NB_COLOR_TO_EXTRACT)
    # print(listColors)
    # convertPixelsToClosestColor(imgWidth, imgHeight, imgPixels, listColors)
    # print("ListColor+ConvertImageToTheseColors: %s seconds" % (time.time() - start_time))
    # start_time = time.time()

    ## PART THAT CUTS THE IMAGE INTO ELEMENTS 
    # (each element is a bunch of pixels with same color)
    elements: List[Element] = getElemsInImg(imgWidth, imgHeight, imgPixels, debug = False)
    print("nb elements: ", len(elements))
    print("GetElementInImg: %s seconds" % (time.time() - start_time))
    start_time = time.time()

    ## PART THAT GETS RID OF THE ELEMENTS THAT ARE TOO SMALL
    ## and remake them
    countWhile = 0
    while(len([elem for elem in elements if len(elem.pixels) <= NB_MIN_PIXELS_PER_ELEM]) > 0):
        elements: List[Element] = cleanUpElements(imgWidth, imgHeight, imgPixels, elements, NB_MIN_PIXELS_PER_ELEM)
        countWhile += 1
        if(countWhile > 5):
            break
    print("nb elements after cleanup: ", len(elements))
    print("CleanUpElements: %s seconds" % (time.time() - start_time))
    start_time = time.time()

    ## PART THAT GETS THE EDGES PIXEL OF EACH ELEMENT
    for element in elements:
        element.getEdgesPixels()
    print("GetEdgesPixels: %s seconds" % (time.time() - start_time))
    start_time = time.time()

    allLinesToDrawSet = set()
    for element in elements:
        for line in element.edgeLines:
            allLinesToDrawSet.add(line)

    #avant modif il y avait 16894 lignes à dessiner
    #avant modif il y avait 373616 pixels à dessiner
    #après modif il y a 12420 lignes à dessiner
    #après modif il y a 241854 pixels à dessiner
    #après modif il y a 11025 lignes à dessiner
    #après modif il y a 156192 pixels à dessiner
    ## PART THAT GETS RID of the lines that touch each other
    allLinesToDrawSet = rmTouchingLines(allLinesToDrawSet)
    print("rmTouchingLines: %s seconds" % (time.time() - start_time))
    start_time = time.time()

    ## we order the lines so that the lines close to each other are next to each other
    allLinesToDraw = sortLines(allLinesToDrawSet)
    print("sortLines: %s seconds" % (time.time() - start_time))
    start_time = time.time()

    pixelForDrawing(allPointsInOrder, allLinesToDraw);
    # print("nb Lines to draw: ", len(allLinesToDrawSet))
    # nbPixels = 0
    # for line in allLinesToDrawSet:
    #     nbPixels += len(line.pixelsCoord)
    # print("nb Pixels to draw: ", nbPixels)

    # we pull all the pixels in an array so that tk can draw them on the canvas later
    # pixelForDrawing(elements)
    print("pixelForDrawing: %s seconds" % (time.time() - start_time))
    
    # we draw the elements on the image that gets saved
    drawElements(elements, imgPixels)
    imgToDraw.show()
    imgToDraw.save("results-trash/" + imgName + "-" + str(NB_COLOR_TO_EXTRACT) + "-" + str(NB_MIN_PIXELS_PER_ELEM) + "-" + str(TRESHOLD_COLOR_DIFF)+ "-" + get_random_string(6) + ".png")
    print("Total time: %s seconds" % (time.time() - start_time_total))

    draw_point(root, canvas, start_time_total)
    root.mainloop()
    
