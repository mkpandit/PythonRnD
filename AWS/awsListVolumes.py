#!/usr/bin/env python

import os, json, sys
import awsConfig

class awsVolumes:
    
    def __init__(self):
        self.author = "Manish Pandit"

    def awsVolumeList(self, awsClient):
        awsVolumes = []
        for v in awsClient.volumes.all():
            print v

if __name__ == "__main__":
    awsCon = awsConfig.aws()
    awsClient = awsCon.awsConnection()
    Disk = awsVolumes()
    try:
        awsVolumes = Disk.awsVolumeList(awsClient)
    except Exception as e:
        print str(e)
