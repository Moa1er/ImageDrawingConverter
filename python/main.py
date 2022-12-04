#how to use pil for images
# print (imgToDraw.size)  # Get the width and hight of the image for iterating over
# print (imgPixels[141,127])  # Get the RGBA Value of the a pixel of an image
# print (imgPixels[399,399])
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .


from PIL import Image

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

def cutImageInElements():
    print("cutImageInElements");

    pixel = Pixel(0, 0, imgPixels[0, 0]);
    element = Element(pixel, pixel.color);


if __name__ == '__main__':
    cutImageInElements();