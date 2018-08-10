#!/usr/bin/env python

from __future__ import print_function

import os, sys
sys.path.append( os.path.join( os.getcwd(), 'YouTubeToMp3/' ) )
import youtubevideodownloader

if __name__ == '__main__':
    download_path = os.path.join( os.getcwd(), 'videos' )
    try:
        YouTubeVideo = youtubevideodownloader.YoutubeVideo()
        video_ids = YouTubeVideo.youtube_video_ids( 'RD7YKjr4U-hWM' )
        for video_id in video_ids:
            downloaded_file = YouTubeVideo.youtube_video_download( video_id, download_path )
            if downloaded_file == False:
                print ( 'Requested video already exists.' )
            else:
                output_file = YouTubeVideo.youtube_video_conversion( download_path, downloaded_file, downloaded_file.replace( 'mp4', 'mp3' ) )
                if output_file == False:
                    print( 'Conversion error' )
                else:
                    print( 'File converted: ' + output_file )
    except HttpError as e:
        print ( "An HTTP error %d occurred:\n%s" % ( e.resp.status, e.content ) )