#!/usr/bin/env python

import os, json, sys
import boto3
import configuration

class awsVolumes:
    
    def __init__(self):
        self.author = "Manish Pandit, updatedmanish@gmail.com"

    def awsConnection(self, region):
        awsaccesskeyid = configuration.aws_access_key_id
        awssecretaccesskey = configuration.aws_secret_access_key
        client = boto3.resource('ec2', aws_access_key_id=awsaccesskeyid, aws_secret_access_key=awssecretaccesskey, region_name=region)
        return client

    def delAwsVolume(self, id, region):
        client = self.awsConnection(region)
        vol = client.Volume(id)
        response = vol.delete()
        if response:
            return id+" has been deleted successfully"
        else:
            return id+" is not deleted"
    
    def attachAwsVolume(self, vol_id, ec2_id, region):
        awsaccesskeyid = configuration.aws_access_key_id
        awssecretaccesskey = configuration.aws_secret_access_key

        session = boto3.Session(aws_access_key_id=awsaccesskeyid, aws_secret_access_key=awssecretaccesskey, region_name=region)
        client = session.client('ec2')

        response = client.attach_volume(
            Device='/dev/sdb',
            InstanceId=ec2_id,
            VolumeId=vol_id,
        )
        return response
    
    def detachAwsVolume(self, vol_id, region):
        awsaccesskeyid = configuration.aws_access_key_id
        awssecretaccesskey = configuration.aws_secret_access_key
        
        session = boto3.Session(aws_access_key_id=awsaccesskeyid, aws_secret_access_key=awssecretaccesskey, region_name=region)
        client = session.client('ec2')
        
        response = client.detach_volume(
            VolumeId=vol_id,
        )
        return response
    
    def createAwsVolume(self, region, availabilityzone, sizeingb, vtype, iops):
        client = self.awsConnection(region)
        if iops == 0:
            response = client.create_volume(AvailabilityZone=availabilityzone, Size=sizeingb, VolumeType=vtype)
        else:
            response = client.create_volume(AvailabilityZone=availabilityzone, Iops=iops, Size=sizeingb, VolumeType=vtype)
        if response:
            return "A "+vtype+" type volume sized " + str(sizeingb) + "GB has been created in " + availabilityzone

if __name__ == "__main__":
    Disk = awsVolumes()
    awsVolumes = []
    
    if sys.argv[1] == 'create':
        try:
            createStatus = Disk.createAwsVolume(sys.argv[2], sys.argv[3], int(sys.argv[4]), sys.argv[5], int(sys.argv[6]))
            awsVolumes.append(createStatus)
        except Exception as e:
            awsVolumes.append(str(e))
        print json.dumps(awsVolumes, sort_keys=True, separators=(',', ': '))
        sys.exit(1)

    if sys.argv[1] == 'delete':
        try:
            delStatus = Disk.delAwsVolume(sys.argv[2], sys.argv[3])
            awsVolumes.append(delStatus)
        except Exception as e:
            awsVolumes.append(str(e))
        print json.dumps(awsVolumes, sort_keys=True, separators=(',', ': '))
        sys.exit(1)

    if sys.argv[1] == 'attach':
        try:
            attachStatus = Disk.attachAwsVolume(sys.argv[2], sys.argv[3], sys.argv[4])
            if attachStatus:
                awsVolumes.append("Volume " + sys.argv[2] + " has been attached to instance " + sys.argv[3])
        except Exception as e:
            awsVolumes.append(str(e))
        print json.dumps(awsVolumes, sort_keys=True, separators=(',', ': '))
    
    if sys.argv[1] == 'detach':
        try:
            attachStatus = Disk.detachAwsVolume(sys.argv[2], sys.argv[3])
            if attachStatus:
                awsVolumes.append("Volume " + sys.argv[2] + " has been detached from associate instance")
        except Exception as e:
            awsVolumes.append(str(e))
        print json.dumps(awsVolumes, sort_keys=True, separators=(',', ': '))