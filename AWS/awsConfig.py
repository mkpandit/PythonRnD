#!/usr/bin/env python

import os, MySQLdb, json, sys
import boto3
from phpserialize import serialize, unserialize

class aws:
    
    def __init__(self):
        self.author = "Manish Pandit"

    def awsConnection(self):
        db = MySQLdb.connect(host="localhost", user="root", passwd="password", db="database")
        cur = db.cursor()
        cur.execute("SELECT * FROM aws_credential WHERE id = 1")
        row = cur.fetchone()
        unserializedData = unserialize(row[2]) 
        awsaccesskeyid = unserializedData['aws_access_key_id']
        awssecretaccesskey = unserializedData['aws_secret_access_key']
        session = boto3.Session(aws_access_key_id=awsaccesskeyid, aws_secret_access_key=awssecretaccesskey, region_name='us-east-1')
        s3 = boto3.resource('s3', aws_access_key_id = awsaccesskeyid, aws_secret_access_key = awssecretaccesskey, region_name='us-east-1')
        client = boto3.resource('ec2', aws_access_key_id=awsaccesskeyid, aws_secret_access_key=awssecretaccesskey, region_name='us-east-1')
        ec2 = session.resource('ec2', region_name='us-east-1')
        return client