#!/usr/bin/env python3
"""
DNS Traffic Analyzer.

This script analyzes DNS traffic to detect new domains accessed by clients.

Usage:
  python3 dns_analyzer.py

Example:
  python3 dns_analyzer.py
"""

import scapy.all as scapy

def process_dns_packet(packet):
    """
    Processes DNS packets and extracts domain names.

    Args:
        packet (scapy.Packet): The DNS packet to process.
    """
    if packet.haslayer(scapy.DNSQR):
        domain = packet[scapy.DNSQR].qname.decode()
        exclude_keywords = ["google", "cloud", "bing", "static", "sensic"]

        if domain not in domains_seen and not any(keyword in domain for keyword in exclude_keywords):
            domains_seen.add(domain)
            print(f"[+] Domain: {domain}")

def sniff(interface):
    """
    Sniffs DNS traffic on the specified interface.

    Args:
        interface (str): The network interface to sniff on.
    """
    scapy.sniff(iface=interface, filter="udp and port 53", prn=process_dns_packet, store=0)

def main():
    """
    Main function to execute the DNS traffic analysis.
    """
    sniff("ens33")

if __name__ == "__main__":
    global domains_seen
    domains_seen = set()
    main()
