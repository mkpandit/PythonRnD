#!/usr/bin/env python

import os, sys, json
import azureConfig
import pprint

if __name__ == "__main__":
    for vms in azureConfig.compute_client.virtual_machines.list_all():
        vmID = vms.id
        resourceGroup = vmID.split("/")[4]
        vm = azureConfig.compute_client.virtual_machines.get(resourceGroup, vms.name, expand = 'instanceview')
        pprint (vm)
