#!/usr/bin/python3
"""
This script calculates network details from a given CIDR range.
It provides the netmask, network ID, broadcast address, and total number of hosts.

Usage:
    python3 cidr_to_ip_range.py <IP> <CIDR>
"""

import os
import sys

def int_to_bin_octet(value):
    """ Convert an integer to a binary string with 8 digits. """
    return bin(value)[2:].zfill(8)

def calculate_network_details(ip, cidr):
    """ Calculate and return network details based on IP and CIDR. """
    octets = [int(octet) for octet in ip.split(".")]
    binary_ip = "".join([int_to_bin_octet(octet) for octet in octets])
    
    # Calculate netmask
    netmask_binary = "1" * cidr + "0" * (32 - cidr)
    netmask_octets = [int(netmask_binary[i:i + 8], 2) for i in range(0, 32, 8)]
    netmask = ".".join(map(str, netmask_octets))
    
    # Calculate other details
    network_id_binary = binary_ip[:cidr] + "0" * (32 - cidr)
    network_id_octets = [int(network_id_binary[i:i + 8], 2) for i in range(0, 32, 8)]
    network_id = ".".join(map(str, network_id_octets))

    broadcast_binary = binary_ip[:cidr] + "1" * (32 - cidr)
    broadcast_octets = [int(broadcast_binary[i:i + 8], 2) for i in range(0, 32, 8)]
    broadcast = ".".join(map(str, broadcast_octets))

    total_hosts = 2**(32 - cidr) - 2

    return netmask, network_id, broadcast, total_hosts

def main():
    try:
        os.system("clear")
        if len(sys.argv) != 3:
            raise ValueError("[!] Usage --> python3 cidr_to_ip_range.py 192.160.3.9 23")
        
        ip = sys.argv[1]
        cidr = int(sys.argv[2])
        netmask, network_id, broadcast, total_hosts = calculate_network_details(ip, cidr)

        print(f"CIDR Range: {ip}/{cidr}")
        print(f"Netmask: {netmask}")
        print(f"Network ID: {network_id}")
        print(f"Broadcast Address: {broadcast}")
        print(f"Total Hosts: {total_hosts}")

    except ValueError as ve:
        print(ve)
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
