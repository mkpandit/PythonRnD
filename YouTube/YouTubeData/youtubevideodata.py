#!/usr/bin/env python

from __future__ import print_function

import argparse
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
import csv, json

class YoutubeTomParticle:
    def __init__( self ):
        self.api_key = "API KEY"
        self.youtube_api_service_name = "youtube"
        self.youtube_api_version = "v3"

    #Parse postmedia youtube channel list from file
    def youtube_channel_list ( self ):
        youtube_channel_ids = []
        with open ( 'youtube-channels.csv' ) as channel_list_file:
            read_channel_list = csv.reader ( channel_list_file, delimiter = ',' )
            next ( read_channel_list, None )
            for row in read_channel_list:
                if int ( row[3] ) > 0:
                    youtube_channel_ids.append ( row[0] )
        channel_list_file.close()
        return youtube_channel_ids

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

    #Check and push data into dictionary
    def youtube_data_check( self, data, dict_check, dict_push ):
        if data in dict_check:
            if isinstance( dict_check[data], list ):
                dict_check[data] = ', '.join( dict_check[data] )
            dict_push[data] = dict_check[data]

if __name__ == '__main__':
    data_flow = YoutubeTomParticle()
    video_description = {}
    try:
        youtube_channel_ids = data_flow.youtube_channel_list()
        for channel_id in youtube_channel_ids:
            video_description[channel_id] = {}
            playlist_id = data_flow.youtube_playlist_id( channel_id )
            video_ids = data_flow.youtube_video_ids( playlist_id )
            if video_ids:
                video_details = data_flow.youtube_video_details( video_ids )
                for video_detail in video_details['items']:
                    video_description[channel_id][video_detail['id']] = {}
                    data_flow.youtube_data_check( 'title',  video_detail['snippet'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'duration',  video_detail['contentDetails'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'channelTitle',  video_detail['snippet'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'categoryId',  video_detail['snippet'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'viewCount',  video_detail['statistics'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'publishedAt',  video_detail['snippet'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'likeCount',  video_detail['statistics'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'favoriteCount',  video_detail['statistics'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'commentCount',  video_detail['statistics'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'tags',  video_detail['snippet'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'caption',  video_detail['contentDetails'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'projection',  video_detail['contentDetails'], video_description[channel_id][video_detail['id']] )
                    data_flow.youtube_data_check( 'liveBroadcastContent',  video_detail['snippet'], video_description[channel_id][video_detail['id']] )
        with open( 'youtube_video_details.json', 'w' ) as fp:
            fp.write( json.dumps( video_description, sort_keys=True, indent=4, separators=(',', ': ') ) )
        fp.close()
    except HttpError as e:
        print ( "An HTTP error %d occurred:\n%s" % ( e.resp.status, e.content ) )