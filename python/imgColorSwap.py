from typing import List

def findColorWithClosestDistance(colorToCmp: tuple, listColors: List[tuple]):
    bestDist = 100000
    closestColor = (0, 0, 0)
    for color in listColors:
        tmpDist = 0.3 * ((colorToCmp[0] - color[0])**2) + 0.59 * ((colorToCmp[1] - color[1])**2) + 0.11 * ((colorToCmp[2] - color[2])**2)
        if(tmpDist < bestDist):
            bestDist = tmpDist
            closestColor = color
    return closestColor

def convertPixelsToClosestColor(imgWidth: int, imgHeight:int, imgPixels, listColors: List[tuple]):
    for x in range(imgWidth):
        for y in range(imgHeight):
            color = findColorWithClosestDistance(imgPixels[x, y], listColors)
            imgPixels[x, y] = color

# use this function for more accurate color comparison
# but it's a loooot slower like a lot (6 to 10 times) and the benefits are not that great
# but it's more accurate to the humain eye (I think)
# https://www.baeldung.com/cs/compute-similarity-of-colours
# def findColorWithClosestDistance(colorToCmp: tuple, listColors: List[tuple]):
#     colorToCmp = rgbTupleToCIELABTuple(colorToCmp)
#     bestDist = 100000
#     closestColor = (0, 0, 0)
#     for color in listColors:
#         colorCielab = rgbTupleToCIELABTuple(color)
#         tmpDist = math.sqrt((colorToCmp[0] - colorCielab[0])**2 + (colorToCmp[1] - colorCielab[1])**2 + (colorToCmp[2] - colorCielab[2])**2)
#         if(tmpDist < bestDist):
#             bestDist = tmpDist
#             closestColor = color
#     return closestColor

# def rgbTupleToCIELABTuple(colorToConvert: tuple):
#     # rgbColor = [colorToConvert[0]/255, colorToConvert[1]/255, colorToConvert[2]/255]
#     colorCielab = rgb2lab(colorToConvert)
#     return colorCielab

# def rgb2lab(inputColor):
#     num = 0
#     RGB = [0, 0, 0]

#     for value in inputColor:
#         value = float(value) / 255

#         if value > 0.04045:
#             value = ((value + 0.055) / 1.055) ** 2.4
#         else:
#             value = value / 12.92

#         RGB[num] = value * 100
#         num = num + 1

#     XYZ = [0, 0, 0, ]

#     X = RGB[0] * 0.4124 + RGB[1] * 0.3576 + RGB[2] * 0.1805
#     Y = RGB[0] * 0.2126 + RGB[1] * 0.7152 + RGB[2] * 0.0722
#     Z = RGB[0] * 0.0193 + RGB[1] * 0.1192 + RGB[2] * 0.9505
#     XYZ[0] = round(X, 4)
#     XYZ[1] = round(Y, 4)
#     XYZ[2] = round(Z, 4)

#     # Observer= 2°, Illuminant= D65
#     XYZ[0] = float(XYZ[0]) / 95.047         # ref_X =  95.047
#     XYZ[1] = float(XYZ[1]) / 100.0          # ref_Y = 100.000
#     XYZ[2] = float(XYZ[2]) / 108.883        # ref_Z = 108.883

#     num = 0
#     for value in XYZ:

#         if value > 0.008856:
#             value = value ** (0.3333333333333333)
#         else:
#             value = (7.787 * value) + (16 / 116)

#         XYZ[num] = value
#         num = num + 1

#     Lab = [0, 0, 0]

#     L = (116 * XYZ[1]) - 16
#     a = 500 * (XYZ[0] - XYZ[1])
#     b = 200 * (XYZ[1] - XYZ[2])

#     Lab[0] = round(L, 4)
#     Lab[1] = round(a, 4)
#     Lab[2] = round(b, 4)

#     return Lab