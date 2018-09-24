#!/usr/bin/env python

import sys, json
import os, gc
import configuration

from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.network import *
from azure.common.credentials import *
from azure.mgmt.compute.models import DiskCreateOption

from haikunator import Haikunator
from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.storage.models import (
    StorageAccountCreateParameters,
    StorageAccountUpdateParameters,
    Sku,
    SkuName,
    Kind
)


class azureStorage:
    
    def __init__(self):
        self.author = "Manish Pandit, updatedmanish@gmail.com"
    
    #List storages from Azure account
    def azureStorageList(self, client):
        storageList = []
        for storage in client.storage_accounts.list():
            storageList.append(storage.name + '_*_' + storage.location + '_*_' + str(storage.creation_time) + '_*_' + str(storage.encryption) + '_*_' + str(storage.type)+"_*_"+str(storage.id.split("/")[4])+"_*_"+str(storage.status_of_primary))
        return storageList

    #Delete a storage from Azure
    def azureStorageDelete(self, storage_name, resource_group, client):
        operation_status = []
        async_creation = client.storage_accounts.delete(resource_group, storage_name)
        list_storage_account = self.azureStorageList(client)
        storage_list = []
        for items in list_storage_account:
            storage_list.append(items.split("_*_")[0])
        
        if storage_name in storage_list:
            operation_status.append("Storage deletion failed")
        else:
            operation_status.append("Storage "+storage_name+" has been deleted successfully")
        return operation_status

    #Empty a storage from Azure
    def azureStorageEmpty(self, storage_name, resource_group, client, location):
        operation_status = []
        delete_storage = self.azureStorageDelete(storage_name, resource_group, client)
        storage_async_operation = client.storage_accounts.create(
            resource_group,
            storage_name,
            {
                'sku': {'name': 'standard_lrs'},
                'kind': 'storage',
                'location': location
            }
        )
        storage_async_operation.wait()
        
        storage_list = []
        list_storage_account = self.azureStorageList(client)
        for items in list_storage_account:
            storage_list.append(items.split("_*_")[0])
        
        if storage_name in storage_list:
            operation_status.append("Storage "+storage_name+" has been emptied successfully")
        else:
            operation_status.append("Failed to empty the storage "+storage_name)
        return operation_status
        

if __name__ == "__main__":
    Storage = azureStorage()
    if sys.argv[1] == 'delete':
        storage_name = sys.argv[2]
        resource_group = sys.argv[3]
        operation_status = Storage.azureStorageDelete(storage_name, resource_group, configuration.storage_client)
        print json.dumps(operation_status, sort_keys=True, separators=(',', ': '))
        sys.exit(1)
        
    elif sys.argv[1] == 'empty':
        storage_name = sys.argv[2]
        resource_group = sys.argv[3]
        location = sys.argv[4]
        operation_status = Storage.azureStorageEmpty(storage_name, resource_group, configuration.storage_client, location)
        print json.dumps(operation_status, sort_keys=True, separators=(',', ': '))
        sys.exit(1)

    else:
        try:
            availableStorage = Storage.azureStorageList(configuration.storage_client)
            print json.dumps(availableStorage, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
        except Exception as e:
            print str(e)