#!/usr/bin/env python

import os, MySQLdb, json, sys
from os import chmod
import boto3
from phpserialize import serialize, unserialize
from Crypto.PublicKey import RSA

class awsKeyPairs:
    
    def __init__(self):
        self.author = "Manish Pandit, updatedmanish@gmail.com"

    def awsConnection(self):
        db = MySQLdb.connect(host="localhost", user="database_user", passwd="database_password", db="database_name")
        cur = db.cursor()
        cur.execute("SELECT * FROM aws_credential WHERE id = 1")
        row = cur.fetchone()
        unserializedData = unserialize(row[2])
        awsaccesskeyid = unserializedData['aws_access_key_id']
        awssecretaccesskey = unserializedData['aws_secret_access_key']
        
        session = boto3.Session(aws_access_key_id=awsaccesskeyid, aws_secret_access_key=awssecretaccesskey)
        return session

    def describeKeyPairs(self, region):
        session = self.awsConnection()
        keyPair = []
        cli = session.client('ec2', region_name=region)
        response = cli.describe_key_pairs()
        for items in response['KeyPairs']:
            keyPair.append(items['KeyName'])
        return keyPair
        
    def describeSecurityGroups(self, region):
        session = self.awsConnection()
        cli = session.client('ec2', region_name=region)
        securityGroups = []
        security_groups = cli.describe_security_groups()
        for items in security_groups['SecurityGroups']:
            securityGroups.append(items['GroupId'])
        return securityGroups
    
    def createKeyPair(self, region, key_pair_name):
        session = self.awsConnection()
        cli = session.client('ec2', region_name=region)
        return cli.create_key_pair(KeyName=key_pair_name)
        
    def importKeyPair(self, region, key_name, pub_key):
        session = self.awsConnection()
        cli = session.client('ec2', region_name=region)
        if len(pub_key) > 1:
            return cli.import_key_pair(KeyName=key_name, PublicKeyMaterial=pub_key)
        else:
            key = RSA.generate(2048)
            with open("/home/tmp/private_"+key_name+".key", 'w') as content_file:
                chmod("/home/tmp/private_"+key_name+".key", 0644)
                content_file.write(key.exportKey('PEM'))
            pubkey = key.publickey()
            with open("/home/tmp/public_"+key_name+".key", 'w') as content_file:
                chmod("/home/tmp/public_"+key_name+".key", 0644)
                content_file.write(pubkey.exportKey('OpenSSH'))
            public_key = pubkey.exportKey('OpenSSH')
            return cli.import_key_pair(KeyName=key_name, PublicKeyMaterial=public_key)
        

if __name__ == "__main__":
    keyPairs = awsKeyPairs()
    if len(sys.argv) > 1:
        if sys.argv[1] == 'listkey':
            keys = keyPairs.describeKeyPairs(sys.argv[2])
            security_groups = keyPairs.describeSecurityGroups(sys.argv[2])
            print json.dumps(keys + security_groups, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
        if sys.argv[1] == 'createkey':
            response = keyPairs.createKeyPair(sys.argv[2], sys.argv[3])
            print response
            sys.exit(1)
        if sys.argv[1] == 'importkey':
            response = keyPairs.importKeyPair(sys.argv[2], sys.argv[3], sys.argv[4])
            import_key_response = []
            import_key_response.append(response['KeyName'])
            import_key_response.append(response['KeyFingerprint'])
            print json.dumps(import_key_response, sort_keys=True, separators=(',', ': '))
            sys.exit(1)