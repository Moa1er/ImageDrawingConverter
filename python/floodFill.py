from PIL import Image

COLOR_TOLERANCE = 20

# imgToDraw = Image.open(R'../assets-test/woman-bar.png')
imgToDraw = Image.open(R'../assets-test/smile-face.png')
# imgToDraw = Image.open('assets-test\\smile-face.png')
imgPixels = imgToDraw.load()

imgWidth = imgToDraw.size[0]
imgHeight = imgToDraw.size[1]
debugImg  = Image.new( mode = "RGB", size = (imgWidth, imgHeight))
debugPixels = debugImg.load()

# an element is a part of the image, it's a bunch of pixels with approximately the same color
# and each pixel touch at least one other pixel of the same element
elements = [];

class Pixel:
  def __init__(self, x: int, y: int, color: tuple):
    self.x = x # x position of the pixel
    self.y = y # y position of the pixel
    self.color = color # color is a tuple (r,g,b)
    
class Element:
    def __init__(self, color: tuple):
        self.pixels = [];
        self.color = color;
    
    def addPixel(self, pixel: Pixel):
        self.pixels.append(pixel);


def floodNofill(pixels, xy):
    """
    Fills array with all pixel connected to the seed point (xy) with the same color.

    :param image: Target image.
    :param xy: Seed position (a 2-item coordinate tuple). See
        :ref:`coordinate-system`.
    """
    x, y = xy
    try:
        background = pixels[x, y]
        elements[0].addPixel(Pixel(x, y, pixels[x, y]))
        debugPixels[x, y] = pixels[x, y]
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
                    fill = isColorAlmostSame(p, background)
                    if fill:
                        elements[0].addPixel(Pixel(s, t, pixels[s, t]))
                        debugPixels[s, t] = pixels[s, t]
                        new_edge.add((s, t))
        full_edge = edge  # discard pixels processed
        edge = new_edge


def isColorAlmostSame(pixel1, pixel2):
    redDiff = abs(pixel1[0] - pixel2[0])
    greenDiff = abs(pixel1[1] - pixel2[1])
    blueDiff = abs(pixel1[2] - pixel2[2])
    if(redDiff < COLOR_TOLERANCE and greenDiff < COLOR_TOLERANCE and blueDiff < COLOR_TOLERANCE):
        return True
    else:
        return False

if __name__ == "__main__":
    startingPoint = (0, 0)
    elements.append(Element(imgPixels[startingPoint[0], startingPoint[1]]))
    floodNofill(imgPixels, startingPoint)
    # imgToDraw.show()
    debugImg.show()