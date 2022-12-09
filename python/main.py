from PIL import Image
import time
import random
import string
from imgColorSwap import *
from colorExtraction import *
from floodNoFill import *
from elementsCleaner import *

start_time_total = time.time()
start_time = time.time()

imgName = "woman-bar-chosen-colors-20-200-20"
imgName = "smile-face-small-dur"
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

# function that fills the debug img with the elements
def drawElements(elements: List[Element]):
    for element in elements:
        for pixel in element.pixels:
            imgPixels[pixel.x, pixel.y] = element.color


def get_random_string(length: int):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

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
    for element in elements:
        print("nb pixels in elem: ", len(element.pixels))
        print("nb pixels in edge: ", len(element.edgePixels))
        print("nb lines: ", len(element.edgeLines))
        countPixelsLine = 0
        for line in element.edgeLines:
            countPixelsLine += len(line.pixelsCoord)
            print("linePixels: ", line.pixelsCoord)
        print("nb pixels in edge lines: ", countPixelsLine)
        
    print("GetEdgesPixels: %s seconds" % (time.time() - start_time))


    drawElements(elements)
    imgToDraw.show()
    imgToDraw.save("results-trash/" + imgName + "-" + str(NB_COLOR_TO_EXTRACT) + "-" + str(NB_MIN_PIXELS_PER_ELEM) + "-" + str(TRESHOLD_COLOR_DIFF)+ "-" + get_random_string(6) + ".png")
    print("Total time: %s seconds" % (time.time() - start_time_total))
    
