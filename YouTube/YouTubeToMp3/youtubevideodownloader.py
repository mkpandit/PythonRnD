#!/usr/bin/env python

from __future__ import print_function

import argparse
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import csv, json, os
import pytube
import subprocess

class YoutubeVideo:
    def __init__( self ):
        self.api_key = "AIzaSyB1PV_bmG46usQuC-UW7UwNXexgdyv1570"
        self.youtube_api_service_name = "youtube"
        self.youtube_api_version = "v3"

    #Youtube API Client
    def youtube_client ( self ):
        client = build( self.youtube_api_service_name, self.youtube_api_version, developerKey = self.api_key )
        return client

    #Playlist ID for a Youtube Channel
    def youtube_playlist_id( self, channel_id ):
        responses = self.youtube_client().channels().list( part = 'contentDetails', id = channel_id ).execute()
        play_list_id = responses['items'][0]['contentDetails']['relatedPlaylists']['uploads']
        return play_list_id

    #Video IDs for a Youtube Channel
    def youtube_video_ids( self, play_list_id ):
        video_ids = []
        play_list_details = self.youtube_client().playlistItems().list(
            part = 'snippet,contentDetails',
            maxResults = 50,
            playlistId = play_list_id
        ).execute()
        #nextPageToken = play_list_details['nextPageToken']
        for video in play_list_details['items']:
            if video['contentDetails']['videoId']:
                video_ids.append ( video['contentDetails']['videoId'] )
        return video_ids

    #Get video data from YouTube Data API
    def youtube_video_details( self, video_ids ):
        video_details = self.youtube_client().videos().list(
            part = 'snippet,contentDetails,statistics,status',
            id = ',' . join ( video_ids )
        ).execute()
        return video_details
    
    def youtube_video_download( self, video_id, download_path ):
        video_object = pytube.YouTube( 'https://www.youtube.com/watch?v=' + video_id )
        youtube_streams = video_object.streams.filter( file_extension='mp4' ).all()
        youtube_file_name = youtube_streams[0].default_filename
        saved_file_name = youtube_file_name.replace( ' ', '-' )

        if saved_file_name not in self.existing_files( download_path ):
            youtube_streams[0].download( download_path, saved_file_name.replace( 'mp4', '' ) )
            if saved_file_name in self.existing_files( download_path ):
                return saved_file_name
        else:
            return False

    def youtube_video_conversion( self, path, input_file, output_file ):
        video_download_command = ['ffmpeg', '-i', path+ '/' + input_file, path+ '/' + output_file ]
        subprocess.call( video_download_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE )
        if output_file in self.existing_files( path ):
            os.remove( path+ '/' + input_file )
            return output_file
        else:
            return False

    def existing_files( self, path ):
        return [ f for f in os.listdir( path ) if os.path.isfile( os.path.join( path, f ) ) ]