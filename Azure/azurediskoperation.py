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


class azureDisks:
    
    def __init__( self ):
        self.author = "Manish Pandit, updatedmanish@gmail.com"
    
    def azureDiskList( self, clientid, secretkey, tenantid, subscription_id ):
        credentials = ServicePrincipalCredentials( client_id=clientid, secret=secretkey, tenant=tenantid )
        compute_client = ComputeManagementClient( credentials,subscription_id )
        resource_client = ResourceManagementClient( credentials, subscription_id )
        storage_client = StorageManagementClient( credentials, subscription_id )
        
        managed_disk = compute_client.disks.list()
        storage_disks = []
        for item in compute_client.disks.list():
            resource_group = item.id.split("/")[4]
            if item.owner_id:
                disk_status = 'in-use'
            else:
                disk_status = 'available'
            
            if item.name:
                storage_disks.append( str(item.name) + "_*_" +str(item.disk_size_gb) + "_*_" + str(item.location) + "_*_" + str(item.type) + "_*_" + str(item.os_type) +"_*_"+disk_status+"_*_"+resource_group)
        return storage_disks
        
    def azureDiskDelete( self, disk_name, resource_group, client ):
        operation_status = []
        async_creation = client.disks.delete( resource_group, disk_name )
        disk_resource = async_creation.result()
        if disk_resource.status == 'Succeeded':
            operation_status.append( "Disk "+disk_name+" has been deleted successfully" )
        else:
            operation_status.append( "Disk deletion failed" )
        return operation_status
    
    def azureAttachDisk( self, disk_name, resource_group, vm_name, client ):
        disk_details = client.disks.get(resource_group, disk_name)
        disk_id = disk_details.id
        
        virtual_machine = client.virtual_machines.get(resource_group, vm_name)
        virtual_machine.storage_profile.data_disks.append({
            'lun': 16,
            'name': disk_name,
            'create_option': DiskCreateOption.attach,
            'managed_disk': {
                'id': disk_id
            }
        })
        async_disk_attach = client.virtual_machines.create_or_update(resource_group, virtual_machine.name, virtual_machine)
        async_disk_attach.wait()
        attach_status_details = async_disk_attach.result()
        operation_status = []
        if attach_status_details.provisioning_state == 'Succeeded':
            operation_status.append("Disk "+disk_name+" has been successfully attached to "+vm_name)
        else:
            operation_status.append("Disk attach failed")
        return operation_status
    
    def azureDetachDisk (self, disk_name, resource_group, client):
        disk_details = client.disks.get(resource_group, disk_name)
        
        vm_name = disk_details.owner_id.split("/")[8]
        virtual_machine = client.virtual_machines.get(resource_group, vm_name)
        data_disks = virtual_machine.storage_profile.data_disks
        data_disks[:] = [disk for disk in data_disks if disk.name != disk_name]
        
        async_vm_update = client.virtual_machines.create_or_update(resource_group, vm_name, virtual_machine)
        virtual_machine = async_vm_update.result()
        operation_status = []
        if virtual_machine.provisioning_state == 'Succeeded':
            operation_status.append("Disk "+disk_name+" has been successfully detached from "+vm_name)
        else:
            operation_status.append("Disk detach failed")
        return operation_status

if __name__ == "__main__":
    Disk = azureDisks()
    
    tenantid = configuration.tenantid
    clientid = configuration.clientid
    secretkey = configuration.secretkey
    subscription_id = configuration.subscription_id
    
    if sys.argv[1] == 'delete':
        disk_name = sys.argv[2]
        resource_group = sys.argv[3]
        operation_status = Disk.azureDiskDelete(disk_name, resource_group, configuration.compute_client)
        print json.dumps(operation_status, sort_keys=True, separators=(',', ': '))
        sys.exit(1)
    elif sys.argv[1] == 'attach':
        disk_name = sys.argv[2]
        resource_group = sys.argv[3]
        vm_name = sys.argv[4]
        operation_status = Disk.azureAttachDisk(disk_name, resource_group, vm_name, configuration.compute_client)
        print json.dumps(operation_status, sort_keys=True, separators=(',', ': '))
        sys.exit(1)
    elif sys.argv[1] == 'detach':
        disk_name = sys.argv[2]
        resource_group = sys.argv[3]
        operation_status = Disk.azureDetachDisk(disk_name, resource_group, configuration.compute_client)
        print json.dumps(operation_status, sort_keys=True, separators=(',', ': '))
        sys.exit(1)
    else:
        try:
            availableDisk = Disk.azureDiskList(clientid, secretkey, tenantid, subscription_id)
            print json.dumps(availableDisk, sort_keys=True, separators=(',', ': '))
            sys.exit(1)
        except Exception as e:
            print str(e)