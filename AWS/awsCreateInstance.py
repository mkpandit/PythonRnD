#!/usr/bin/env python

import os, json, sys
import awsConfig

class awsEC2:
    def __init__(self):
        self.author = "Manish Pandit"
   def awsCreateEC2(self, ami_id, min_count, max_count, instance_type, volume_size, volume_type):
        client = awsConfig.awsConnection()
        instances = client.create_instances(
            BlockDeviceMappings=[
                {
                    'DeviceName': '/dev/sdh',
                    'VirtualName': 'OSDisk0',
                    'Ebs': {
                        'Encrypted': False,
                        'DeleteOnTermination': True,
                        'VolumeSize': volume_size,
                        'VolumeType': volume_type
                    },
                },
            ],
            ImageId=ami_id, 
            MinCount=min_count, 
            MaxCount=max_count, 
            InstanceType=instance_type,
            KeyName='ProvideKeyName',
            SecurityGroupIds=['SecurityGroup1', 'SecurityGroup2'],
        )
        if instances:
            return instances
        else:
            return "Instance(s) not created"

if __name__ == "__main__":
    createEC2 = awsEC2()
    instanceCreateMsg = []
    ami_id = 'ami-NUMBER'
    min_count = 1 #Minimum number of instances
    max_count =  1 #Maximum number of instances
    instance_type = 'instance-type'
    volume_size = 64 #Size in GB
    volume_type = 'volume-type'
    
    try:
        createInstance = createEC2.awsCreateEC2(ami_id, min_count, max_count, instance_type, volume_size, volume_type)
        instanceCreateMsg.append(createInstance)
    except Exception as e:
        instanceCreateMsg.append(str(e))
        
    print json.dumps(instanceCreateMsg)
    sys.exit(0)