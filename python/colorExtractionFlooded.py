import math
from typing import List
from PIL import Image
import pandas as pd
import extcolors
from colormap import rgb2hex
import time
import random
import string

start_time = time.time()

imgName = "woman-bar"
imgPath = R'../assets-test/' + imgName + ".png"

imgToDraw = Image.open(imgPath)
# imgToDraw = Image.open(R'../assets-test/smile-face.png')
# imgToDraw = Image.open('assets-test\\smile-face.png')
imgPixels = imgToDraw.load()

imgWidth = imgToDraw.size[0]
imgHeight = imgToDraw.size[1]

## constants part
NB_COLOR_TO_EXTRACT = 10

## color extraction part
## see https://towardsdatascience.com/image-color-extraction-with-python-in-4-steps-8d9370d9216e for reference
def color_to_df(input):
    colors_pre_list = str(input).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]
    
    #convert RGB to HEX code
    df_color_up = [rgb2hex(int(i.split(", ")[0].replace("(","")),
                          int(i.split(", ")[1]),
                          int(i.split(", ")[2].replace(")",""))) for i in df_rgb]
    
    # replace df_rgb to df_color_up if you want to use hex code
    df = pd.DataFrame(zip(df_rgb, df_percent), columns = ['c_code','occurence'])
    return df

def getListColorsInImg(input_image: string, tolerance: int):
    colors_x = extcolors.extract_from_path(input_image, tolerance = tolerance, limit = NB_COLOR_TO_EXTRACT)
    df_color = color_to_df(colors_x)
    #annotate text (color in hexadecimal)
    listColors = list(df_color['c_code'])
    return listColors

def convertStringRgbToTuple(listColorsString: string):
    listColorsTuple = []
    for color in listColorsString:
        color = color.replace('(', '')
        color = color.replace(')', '')
        listColorsTuple.append(tuple(map(int, color.split(', '))))
    return listColorsTuple

# TODO check last method in this document for better color comparison
# https://www.baeldung.com/cs/compute-similarity-of-colours
def findColorWithClosestDistance(colorToCmp: tuple, listColors: List[tuple]):
    bestDist = 100000
    closestColor = (0, 0, 0)
    for color in listColors:
        tmpDist = 0.3 * ((colorToCmp[0] - color[0])**2) + 0.59 * ((colorToCmp[1] - color[1])**2) + 0.11 * ((colorToCmp[2] - color[2])**2)
        if(tmpDist < bestDist):
            bestDist = tmpDist
            closestColor = color
    return closestColor

def convertPixelsToClosestColor(listColors: List[tuple]):
    for x in range(imgWidth):
        for y in range(imgHeight):
            color = findColorWithClosestDistance(imgPixels[x, y], listColors)
            imgPixels[x, y] = color

def get_random_string(length):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str

if __name__ == '__main__':
    listColors: string = getListColorsInImg(imgPath, 20)
    listColors: tuple = convertStringRgbToTuple(listColors)
    convertPixelsToClosestColor(listColors)
    imgToDraw.save("results/" + imgName + "-" + str(NB_COLOR_TO_EXTRACT) + "-" + get_random_string(12) + ".png")
    print("--- %s seconds ---" % (time.time() - start_time))
    
