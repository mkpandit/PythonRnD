#!/usr/bin/env python

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.storage import StorageManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from haikunator import Haikunator

#Define credentials
subscription_id = "Azure Subscription ID"
clientid = "Azure Client ID"
secretkey = "Azure Secret Key"
tenantid = "Azure App Tenant ID"

credentials = ServicePrincipalCredentials( client_id=clientid, secret=secretkey, tenant=tenantid )

#Define different clients (Compute, Resource, Storage, Network)
resource_client = ResourceManagementClient( credentials, subscription_id )
compute_client = ComputeManagementClient( credentials, subscription_id )
storage_client = StorageManagementClient( credentials, subscription_id )
network_client = NetworkManagementClient( credentials, subscription_id )
