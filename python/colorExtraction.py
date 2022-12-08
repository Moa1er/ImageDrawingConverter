import extcolors
import string
from colormap import rgb2hex
import pandas as pd

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

def convertStringRgbToTuple(listColorsString: string):
    listColorsTuple = []
    for color in listColorsString:
        color = color.replace('(', '')
        color = color.replace(')', '')
        listColorsTuple.append(tuple(map(int, color.split(', '))))
    return listColorsTuple

def getListColorsInImg(input_image: string, tolerance: int, nbColorToExtract: int):
    colors_x = extcolors.extract_from_path(input_image, tolerance = tolerance, limit = nbColorToExtract)
    df_color = color_to_df(colors_x)
    #annotate text (color in hexadecimal)
    listColors = list(df_color['c_code'])
    return convertStringRgbToTuple(listColors)
