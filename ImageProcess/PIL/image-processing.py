#!/usr/bin/env python

from PIL import Image, ImageDraw, ImageFont
import math

class processImage:
    def __init__( self ):
        self.author = "Manish Pandit, updatedmanish@gmail.com"

    def describeImage( self, imgPath ):
        im = Image.open( imgPath )
        width, height = im.size
        image_type = im.format
        image_mode = im.mode
        return [ height, width, image_type, image_mode ]
    
    def createNewImage( self, imgPath, textLine ):
        im = Image.open( imgPath )
        #im = Image.new( 'RGB', ( 200, 200 ), color = 'red' )
        width = self.describeImage( imgPath )[1]
        height = self.describeImage( imgPath )[0]

        fnt = ImageFont.truetype( '/Library/Fonts/Georgia.ttf', 24 )
        d = ImageDraw.Draw( im )
        d.text( ( ( width / 2 ) - 100 , ( height / 2) - 100 ), textLine, font = fnt, fill = ( 255, 255, 0 ) )
        im.save( 'img/new.png' )
        im.show()

if __name__ == "__main__":
    image = processImage()
    print( image.describeImage( 'img/5.jpg' ) )