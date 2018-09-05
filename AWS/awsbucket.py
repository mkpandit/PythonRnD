#!/usr/bin/env python

import os, json, sys
import boto3

class awsBucket:
    
    def __init__(self):
        self.author = "Manish Pandit"
		self.awsaccesskeyid = "aws_access_key_id"
        self.awssecretaccesskey = "aws_secret_access_key"
		# self.region = "region"

	# awsConnection(), method to establish SDK connection with AWS
	# returns list
    def awsConnection(self):
        session = boto3.Session(aws_access_key_id=self.awsaccesskeyid, aws_secret_access_key=self.awssecretaccesskey)
        aws3 = session.resource('s3')
		# aws3 = session.resource('s3', region_name=self.region) if a region is prefered
        return aws3

	# createAWSBucket(bucketName), method to create bucket
	# returns list
    def createAWSBucket(self, bucketName):
        aws3 = self.awsConnection()
        create_bucket_msg = []
        try:
            if aws3.create_bucket(Bucket=bucketName):
                create_bucket_msg.append( "Bucket "+ bucketName + " has been created successfully" )
        except Exception as e:
            create_bucket_msg.append( e.message )
    
        return create_bucket_msg
    
	# listAWSBucket(), method to list all buckets
	# returns list
    def listAWSBucket(self):
        aws3 = self.awsConnection()
        list_bucket_msg = []
        try:
            for bucket in aws3.buckets.all():
                if bucket.name:
                    list_bucket_msg.append( str(bucket.name) + '_*_' + str(bucket.creation_date) )
        except Exception as e:
            list_bucket_msg.append( e.message )
            
        return list_bucket_msg
    
	# deleteAWSBucket(bucketName), method to delete a bucket
	# returns list
    def deleteAWSBucket(self, bucketName):
        aws3 = self.awsConnection()
        bucket = aws3.Bucket(bucketName)
        
        delete_bucket_msg = []
        objects_to_delete = []
        for obj in bucket.objects.all():
            objects_to_delete.append({'Key': obj.key})

        if len(objects_to_delete) > 0:
            response = bucket.delete_objects(
                Delete={
                    'Objects': objects_to_delete
                }
            )
        try:
            if bucket.delete():
                delete_bucket_msg.append( bucketName + " has been deleted successfully")
        except Exception as e:
            delete_bucket_msg.append( e.message )
        
        return delete_bucket_msg
    
	# emptyAWSBucket(bucketName), method to empty a bucket
	# returns list
    def emptyAWSBucket(self, bucketName):
        aws3 = self.awsConnection()
        bucket = aws3.Bucket(bucketName)

        empty_bucket_msg = ""
        objects_to_delete = []
        try:
            for obj in bucket.objects.all():
                objects_to_delete.append({'Key': obj.key})

            if len(objects_to_delete) > 0:
                response = bucket.delete_objects(Delete={'Objects': objects_to_delete})
                if response:
                    empty_bucket_msg.append( bucketName + " is empty" )
                else:
                    empty_bucket_msg.append( "Can not empty this "+bucketName )
            else:
                empty_bucket_msg.append( bucketName+" is already empty" )
        except Exception as e:
            empty_bucket_msg.append( e.message )

        return empty_bucket_msg

if __name__ == "__main__":
    bucket = awsBucket()
    
    if len(sys.argv) > 1:
	
        #Create a bucket
        if sys.argv[1] == 'create':
            create_bucket_msg = []
            create_bucket_msg = bucket.createAWSBucket(sys.argv[2])
            print json.dumps(create_bucket_msg, sort_keys=True, separators=(',', ': '))
            sys.exit(1)

        #List all buckets
        if sys.argv[1] == 'list':
            list_bucket_msg = []
            list_bucket_msg = bucket.listAWSBucket()
            print json.dumps(list_bucket_msg, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
            
        #Delete a bucket
        if sys.argv[1] == 'delete':
            delete_bucket_msg = []
            delete_bucket_msg = bucket.deleteAWSBucket(sys.argv[2])
            print json.dumps(delete_bucket_msg, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
            
        #Empty a bucket
        if sys.argv[1] == 'empty':
            empty_bucket_msg = []
            empty_bucket_msg = bucket.emptyAWSBucket(sys.argv[2])
            print json.dumps(empty_bucket_msg, sort_keys=True, separators=(',', ': '))
            sys.exit(1)