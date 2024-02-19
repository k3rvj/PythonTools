#!/usr/bin/env python3
"""
MAC Address Changer Tool.

This script changes the MAC address of a specified network interface.

Usage:
  python3 mac_changer.py -i <interface> -m <mac_address>

Example:
  python3 mac_changer.py -i eth0 -m aa:bb:cc:11:22:33
"""

import argparse
import subprocess
from termcolor import colored
import re

def get_arguments():
    """
    Parses command line arguments.

    Returns:
        argparse.Namespace: An object containing the parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Tool to change the MAC address of a network interface")
    parser.add_argument("-i", "--interface", required=True, dest="interface", help="Network interface name")
    parser.add_argument("-m", "--mac", required=True, dest="mac_address", help="New MAC address for the network interface")
    return parser.parse_args()

def is_valid_input(interface, mac_address):
    """
    Checks if the input data (interface name and MAC address) is valid.

    Args:
        interface (str): The network interface name.
        mac_address (str): The MAC address.

    Returns:
        bool: True if the input is valid, False otherwise.
    """
    is_valid_interface = re.match(r'^[eE][nN][tTsS][0-9]{1,2}$', interface)
    is_valid_mac_address = re.match(r'^([A-Fa-f0-9]{2}[:]){5}[A-Fa-f0-9]{2}$', mac_address)
    return is_valid_interface and is_valid_mac_address

def change_mac_address(interface, mac_address):
    """
    Changes the MAC address of the specified network interface.

    Args:
        interface (str): The network interface name.
        mac_address (str): The new MAC address.
    """
    if is_valid_input(interface, mac_address):
        subprocess.run(["ifconfig", interface, "down"])
        subprocess.run(["ifconfig", interface, "hw", "ether", mac_address])
        subprocess.run(["ifconfig", interface, "up"])
        print(colored("\n[+] The MAC has been successfully changed", 'green'))
    else:
        print(colored("\n[!] The input data is not correct", 'red'))

def main():
    """
    Main function to execute the MAC address changing process.
    """
    args = get_arguments()
    change_mac_address(args.interface, args.mac_address)

if __name__ == "__main__":
    main()
