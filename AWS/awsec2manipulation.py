#!/usr/bin/env python

#Python class to scan AWS Storage

import sys, json
import os, gc, pprint
import boto3

class awsEC2:
    
    def __init__(self):
        self.author = "Manish Pandit, updatedmanish@gmail.com"
        
    def processDictionary(self, d):
        instanceDetails = []
        for k, v in d.iteritems():
            if isinstance(v, dict):
                instanceDetails.extend(self.processDictionary(v))
            elif isinstance(v, list):
                for item in v:
                    if isinstance(item, dict):
                        instanceDetails.extend(self.processDictionary(v[0]))
            else:
                instanceDetails.append(str(k) + "->" + str(v))
        return instanceDetails
    
    def awsConnectionClient(self, awsR):
        awsaccesskeyid = "awsaccesskeyid"
        awssecretaccesskey = "awssecretaccesskey"
        session = boto3.Session(aws_access_key_id=awsaccesskeyid,aws_secret_access_key=awssecretaccesskey)
        ec2 = session.resource('ec2', region_name='us-east-1')
        client = boto3.client(awsR, aws_access_key_id=awsaccesskeyid, aws_secret_access_key=awssecretaccesskey, region_name='us-east-1')
        return client
    
    def awsConnectionResource(self):
        awsaccesskeyid = "awsaccesskeyid"
        awssecretaccesskey = "awssecretaccesskey"
        session = boto3.Session(aws_access_key_id=awsaccesskeyid,aws_secret_access_key=awssecretaccesskey)
        ec2 = session.resource('ec2', region_name='us-east-1')
        return ec2
    
    def describeInstance(self, ec2ID):
        client = self.awsConnectionClient('ec2')
        ec2Details = client.describe_instances(Filters=[], InstanceIds=[ec2ID])
        return ec2Details
    
    def stopInstance(self, ec2ID):
        client = self.awsConnectionClient('ec2')
        ec2Details = client.stop_instances(InstanceIds=[ec2ID])
        return True
    
    def stopInstances(self, ec2ID):
        client = self.awsConnectionClient('ec2')
        ids = []
        for items in ec2ID.split(","):
            ids.append(items)
        ec2Details = client.stop_instances(InstanceIds=ids)
        return True
        
    def startInstance(self, ec2ID):
        client = self.awsConnectionClient('ec2')
        ec2Details = client.start_instances(InstanceIds=[ec2ID])
        return True
    
    def startInstances(self, ec2ID):
        client = self.awsConnectionClient('ec2')
        ids = []
        for items in ec2ID.split(","):
            ids.append(items)
        ec2Details = client.start_instances(InstanceIds=ids)
        return True
    
    def terminateInstance(self, ec2ID):
        client = self.awsConnectionClient('ec2')
        ec2Details = client.terminate_instances(InstanceIds=[ec2ID])
        return True

if __name__ == "__main__":
    AWSInstances = awsEC2()
    try:
        if sys.argv[2] == 'stop':
            stopMsg = []
            if AWSInstances.stopInstance(sys.argv[1]):
                stopMsg.append("Instance " + str(sys.argv[1]) + " has been Stopped")
            print json.dumps(stopMsg, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
        
        if sys.argv[2] == 'mstop':
            stopMsg = []
            if AWSInstances.stopInstances(sys.argv[1]):
                stopMsg.append("Instance " + str(sys.argv[1]) + " has been Stopped. Its might take a while for the change to appear or refresh the page.")
            print json.dumps(stopMsg, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
        
        if sys.argv[2] == 'mstart':
            stopMsg = []
            if AWSInstances.startInstances(sys.argv[1]):
                stopMsg.append("Instance " + str(sys.argv[1]) + " has been started. Its might take a while for the change to appear or refresh the page.")
            print json.dumps(stopMsg, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
        
        if sys.argv[2] == 'start':
            startMsg = []
            if AWSInstances.startInstance(sys.argv[1]):
                startMsg.append("Instance " + str(sys.argv[1]) + " has been Started")
            print json.dumps(startMsg, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
        
        if sys.argv[2] == 'terminate':
            terminateMsg = []
            if AWSInstances.terminateInstance(sys.argv[1]):
                terminateMsg.append("Instance " + str(sys.argv[1]) + " has been terminated")
            print json.dumps(terminateMsg, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
        if sys.argv[2] == 'details':
            ec2Details = AWSInstances.describeInstance(sys.argv[1])
            print json.dumps(AWSInstances.processDictionary(ec2Details), sort_keys=True, separators=(',', ': '))
            sys.exit(1)
    except Exception as e:
        print str(e)