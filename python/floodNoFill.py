from PIL import Image
from drawingClasses import *

"""
Fills array with all pixel connected to the seed point (xy) with the same color.

:param image: Target image.
:param xy: Seed position (a 2-item coordinate tuple). See
    :ref:`coordinate-system`.
"""
def floodNofill(pixels, xy, elementToAddTo, debug = False):
    x, y = xy
    try:
        background = pixels[x, y]
        elementToAddTo.addPixel(Pixel(x, y, pixels[x, y]))
        if debug: debugPixels[x, y] = pixels[x, y]
        pixelsChecked.add((x, y))
        if (x, y) in pixelsNotChecked:
            pixelsNotChecked.remove((x, y))
    except (ValueError, IndexError):
        return  # seed point outside image
    edge = {(x, y)}
    # use a set to keep record of current and previous edge pixels
    # to reduce memory consumption
    full_edge = set()
    while edge:
        new_edge = set()
        for (x, y) in edge:  # 4 adjacent method
            for (s, t) in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                # If already processed, or if a coordinate is negative, skip
                if (s, t) in full_edge or s < 0 or t < 0:
                    continue
                try:
                    p = pixels[s, t]
                except (ValueError, IndexError):
                    pass
                else:
                    full_edge.add((s, t))
                    fill = (p == background)
                    if fill:
                        elementToAddTo.addPixel(Pixel(s, t, pixels[s, t]))
                        if debug: debugPixels[s, t] = elementToAddTo.color
                        new_edge.add((s, t))
                        pixelsChecked.add((s, t))
                        if (s, t) in pixelsNotChecked:
                            pixelsNotChecked.remove((s, t))
                    else:
                        if (s, t) not in pixelsChecked:
                            pixelsNotChecked.add((s, t))
        full_edge = edge  # discard pixels processed
        edge = new_edge

"""
Cuts an input image in elements, each element is a part of the image, 
it's a bunch of pixels with the same color

:param image: Target image.
:param xy: Seed position (a 2-item coordinate tuple). See
    :ref:`coordinate-system`.
"""   
def getElemsInImg(imgWidth, imgHeight, imgPixels, debug = False):
    # an element is a part of the image, it's a bunch of pixels with 
    # approximately the same color
    # and each pixel touch at least one other pixel of the same element
    elements = [];

    #creates two sets for the function flooNoFill
    global pixelsChecked
    pixelsChecked = set()
    global pixelsNotChecked
    pixelsNotChecked = set()

    if debug:
        #creates a debug img to see the result
        debugImg  = Image.new(mode="RGB", size=(imgWidth, imgHeight))
        global debugPixels
        debugPixels = debugImg.load()

    pixelsNotChecked.add((0, 0))
    while(len(pixelsNotChecked) > 0):
        startingPoint = pixelsNotChecked.pop()
        while(startingPoint in pixelsChecked):
            if(len(pixelsNotChecked) == 0):
                break
            startingPoint = pixelsNotChecked.pop()
            
        elements.append(Element(imgPixels[startingPoint[0], startingPoint[1]]))
        floodNofill(imgPixels, startingPoint, elements[len(elements) - 1], debug = debug)

    if debug:
        debugImg.show()

    return elements
    