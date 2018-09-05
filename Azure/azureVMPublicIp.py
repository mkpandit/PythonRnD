#!/usr/bin/env python

import os, sys, json
import configuration

if __name__ == "__main__":
    vm = azureConfig.compute_client.virtual_machines.get(GROUP_NAME, VMNAME)
    #Processing Network Interface Card (NIC) information
    net_interface = vm.network_profile.network_interfaces[0]
    net_interface = net_interface.id.split('/')
    net_interface_group = net_interface[4]
    net_interface_name = net_interface[8]
    net_interface_details = azureConfig.network_client.network_interfaces.get(net_interface_group, net_interface_name)
    #Processing IP Address information
    ip_address_reference = net_interface_details.ip_configurations[0].public_ip_address
    if ip_address_reference:
        ip_address_reference = ip_address_reference.id.split('/')
        ip_address_group = ip_address_reference[4]
        ip_address_name = ip_address_reference[8]

        public_ip_address = azureConfig.network_client.public_ip_addresses.get(ip_address_group, ip_address_name)
        public_ip_address = public_ip_address.ip_address
    else:
        public_ip_address = "IP address is not assigned"
    print public_ip_address