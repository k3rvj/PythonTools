#!/usr/bin/env python3
"""
ARP Scanner.

This script performs ARP scanning to discover hosts on a network.

Usage:
  python3 arp_scanner.py -t <target>

Example:
  python3 arp_scanner.py -t 10.0.0.1/24
"""

import scapy.all as scapy
import argparse

def get_arguments():
    """
    Parses command line arguments.

    Returns:
        str: The target host or IP range to scan.
    """
    parser = argparse.ArgumentParser(description="ARP Scanner")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host / IP Range to Scan")
    args = parser.parse_args()
    return args.target

def scan(ip):
    """
    Performs ARP scanning to discover hosts on the network.

    Args:
        ip (str): The target IP address or IP range.
    """
    arp_packet = scapy.ARP(pdst=ip)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_packet = broadcast_packet/arp_packet
    answered, unanswered = scapy.srp(arp_packet, timeout=1, verbose=False)
    response = answered.summary()
    
    if response:
        print(response)

def main():
    """
    Main function to execute the ARP scanning process.
    """
    target = get_arguments()
    scan(target)

if __name__ == "__main__":
    main()
