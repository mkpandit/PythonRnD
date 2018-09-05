#!/usr/bin/env python

import os, json, sys
import awsConfig

class awsVolumes:
    
    def __init__(self):
        self.author = "Manish Pandit"

   def awsVolumeCreate(self, sizeingb, vtype):
        client = awsConfig.awsConnection()
        response = client.create_volume(AvailabilityZone='us-east-1a', Size=sizeingb, VolumeType=vtype)
        if response:
	    return response

if __name__ == "__main__":
    Disk = awsVolumes()
    awsVolumes = []
    sizeingb = int(sys.argv[1])
    vtype = sys.argv[2]
    try:
        vCreateMsg = Disk.awsVolumeCreate(sizeingb, vtype)
        awsVolumes = vCreateMsg
    except Exception as e:
        awsVolumes.append(str(e))
    print json.dumps(awsVolumes, sort_keys=True, separators=(',', ': '))
    sys.exit(1)
