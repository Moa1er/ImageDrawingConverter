from PIL import Image

imgToDraw = Image.open('../assets-test/smile-face.png') # Can be many different formats.
imgPixels= imgToDraw.load()
print (imgToDraw.size)  # Get the width and hight of the image for iterating over
print (imgPixels[141,127])  # Get the RGBA Value of the a pixel of an image
# pix[x,y] = value  # Set the RGBA Value of the image (tuple)
# im.save('alive_parrot.png')  # Save the modified pixels as .png