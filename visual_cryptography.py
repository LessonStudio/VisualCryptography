#Copyright, Robert Donovan, LessonStudio, 2014
#If you use this then tweet what you did with it @LessonStudio.

#This file takes one argument which is a file that you would like to split into two encrypted images.
#The original image can only be viewed by overlaying the two encrypted images.
#If printed on clear plastic, It can be very finicky to align the two images if the pixel count is too high.
#For best results keep the original image below 200x200 pixels and print as large as possible onto clear plastic to
# obtain the best results.

#You can go to higher resolutions but you then really have to be precise when aligning the two images.

#The resulting images will be twice as wide and twice as tall pixelwise and there is only 1 bit colour.#Copyright, Robert Donovan, LessonStudio, 2014
#If you use this then tweet what you did with it @LessonStudio.

#This file takes one argument which is a file that you would like to split into two encrypted images.
#The original image can only be viewed by overlaying the two encrypted images.
#If printed on clear plastic, It can be very finicky to align the two images if the pixel count is too high.
#For best results keep the original image below 200x200 pixels and print as large as possible onto clear plastic to
# obtain the best results.

#You can go to higher resolutions but you then really have to be precise when aligning the two images.

#The resulting images will be twice as wide and twice as tall pixelwise and there is only 1 bit colour.

#Future features should include alignment marks to make aligning the two transparancies easier.

#Maybe I will increase the efficiency of the conversion except that I find that I spend more prep time in
# photoshop by many orders of magnitude than any time savings that could be extracted.

#The reason I built this is that I found many tools out there for doing this that didn't work for a
# variety of reasons including being built for long dead versions of Python or PIL.

# USAGE: python visual_cryptography.py file_to_encrypt.png

from PIL import Image, ImageDraw
import os, sys
from random import SystemRandom
random = SystemRandom()
#If you want to use the more powerful PyCrypto (pip install pycrypto) then uncomment the next line and comment out the previous two lines
#from Crypto.Random import random

if len(sys.argv)!=2:
	print "This takes one argument; the image to be split."
	exit()
infile=str(sys.argv[1])

if not os.path.isfile(infile):
	print "That file does not exist."
	exit()

img = Image.open(infile)

f, e = os.path.splitext(infile)
out_filename_A=f+"_A.png"
out_filename_B=f+"_B.png"

img=img.convert('1')#convert image to 1 bit

#Prepare two empty slider images for drawing
width=img.size[0]*2
height=img.size[1]*2
out_image_A = Image.new('1', (width, height))
out_image_B = Image.new('1', (width, height))
draw_A = ImageDraw.Draw(out_image_A)
draw_B = ImageDraw.Draw(out_image_B)

#There are 6(4 choose 2) possible patterns and it is too late for me to think in binary and do these efficiently
patterns=((1,1,0,0), (1,0,1,0), (1,0,0,1), (0,1,1,0), (0,1,0,1), (0,0,1,1))
#Cycle through pixels
for x in xrange(0, width/2):
	for y in xrange(0, height/2):
		pixel=img.getpixel((x,y))
		pat=random.choice(patterns)
		#A will always get the pattern
		draw_A.point((x*2, y*2), pat[0])
		draw_A.point((x*2+1, y*2), pat[1])
		draw_A.point((x*2, y*2+1), pat[2])
		draw_A.point((x*2+1, y*2+1), pat[3])
		if pixel==0:#Dark pixel so B gets the anti pattern
			draw_B.point((x*2, y*2), 1-pat[0])
			draw_B.point((x*2+1, y*2), 1-pat[1])
			draw_B.point((x*2, y*2+1), 1-pat[2])
			draw_B.point((x*2+1, y*2+1), 1-pat[3])
		else:
			draw_B.point((x*2, y*2), pat[0])
			draw_B.point((x*2+1, y*2), pat[1])
			draw_B.point((x*2, y*2+1), pat[2])
			draw_B.point((x*2+1, y*2+1), pat[3])

out_image_A.save(out_filename_A, 'PNG')
out_image_B.save(out_filename_B, 'PNG')
print "Done."
