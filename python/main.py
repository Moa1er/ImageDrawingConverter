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

imgName = "woman-bar"
imgPath = R'../assets-test/' + imgName + ".png"

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
NB_COLOR_TO_EXTRACT = 20
NB_MIN_PIXELS_PER_ELEM = 50

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
    listColors: tuple = getListColorsInImg(imgPath, 10, NB_COLOR_TO_EXTRACT)
    convertPixelsToClosestColor(imgWidth, imgHeight, imgPixels, listColors)
    print("ListColor+ConvertImageToTheseColors: %s seconds" % (time.time() - start_time))
    start_time = time.time()

    ## PART THAT CUTS THE IMAGE INTO ELEMENTS 
    # (each element is a bunch of pixels with same color)
    elements: List[Element] = getElemsInImg(imgWidth, imgHeight, imgPixels, debug = False)
    print("nb elements: ", len(elements))
    print("GetElementInImg: %s seconds" % (time.time() - start_time))
    start_time = time.time()

    ## PART THAT GETS RID OF THE ELEMENTS THAT ARE TOO SMALL
    ## and remake them
    elements: List[Element] = cleanUpElements(imgWidth, imgHeight, imgPixels, elements, NB_MIN_PIXELS_PER_ELEM)
    print("nb elements after cleanup: ", len(elements))
    print("CleanUpElements: %s seconds" % (time.time() - start_time))
    start_time = time.time()

    drawElements(elements)
    imgToDraw.save("results/" + imgName + "-" + str(NB_COLOR_TO_EXTRACT) + "-" + get_random_string(12) + ".png")
    print("Total time: %s seconds" % (time.time() - start_time_total))
    
