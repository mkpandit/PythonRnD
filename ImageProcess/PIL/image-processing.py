#!/usr/bin/env python
# -*- coding: utf-8 -*-

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

        fnt = ImageFont.truetype( '/Library/Fonts/SolaimanLipi.ttf', 20, encoding='unic' ) #Georgia.ttf
        d = ImageDraw.Draw( im )
        d.text( ( ( width / 2 ) - 100 , ( height / 2) - 100 ), textLine, font = fnt, fill = ( 255, 255, 0 ) )
        im.save( 'img/text_image.png' )
        im.show()
    
    def composeImage( self, imgOne, imgTwo, vertical = 1 ):
        imOne = Image.open( imgOne )
        imOneWidth, imOneHeight = imOne.size
        imOne.thumbnail( ( 300, 300 ) )

        imTwo = Image.open( imgTwo )
        imTwoWidth, imTwoHeight = imTwo.size
        imTwo.thumbnail( ( 300, 300 ) )
        
        if vertical == 1:
            imBase = Image.new( 'RGB', ( 630, 320 ), ( 255, 255, 255 ) )
            imBase.paste( imOne, ( 10, 10 ) )
            imBase.paste( imTwo, ( 320, 10 ) )
        else:
            imBase = Image.new( 'RGB', ( 320, 630 ), ( 255, 255, 255 ) )
            imBase.paste( imOne, ( 10, 10 ) )
            imBase.paste( imTwo, ( 10, 320 ) )

        imBase.save( 'img/compose.jpg' )
        imBase.show()

    def rotateImage( self, imgPath ):
        im = Image.open( imgPath )
        im_rotated = im.rotate( 45 )
        print ( im_rotated.size )
        im_rotated.show()

if __name__ == "__main__":
    image = processImage()
    image.createNewImage( 'img/8.jpg', 'মনিষ পন্ডিত বাড়ি নেই' )