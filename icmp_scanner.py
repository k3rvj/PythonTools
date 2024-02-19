#!/usr/bin/env python3
"""
Network Host Discovery Tool.

This script discovers active hosts on a network using ICMP ping requests.

Usage:
  python3 host_discovery.py -t <target>

Example:
  python3 host_discovery.py -t 10.0.0.1-100
"""

import argparse
import subprocess
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

def signal_handler(sig, frame):
    """
    Handles SIGINT signal (Ctrl+C) gracefully.
    Exits the program with an appropriate message.

    Args:
        sig: Signal number
        frame: Current stack frame
    """
    print(colored("\n[!] Ctrl + C pressed...\n", 'red'))
    sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)

def get_arguments():
    """
    Parses command line arguments.

    Returns:
        str: The target host or network range to scan.
    """
    parser = argparse.ArgumentParser(description="Tool to discover active hosts on a network (ICMP)")
    parser.add_argument("-t", "--target", required=True, dest="target", help="Host or network range to scan")
    args = parser.parse_args()
    return args.target

def parse_target(target_str):
    """
    Parses the target string to extract individual IP addresses or IP ranges.

    Args:
        target_str (str): The target string provided by the user.

    Returns:
        list: List of individual IP addresses or IP ranges.
    """
    target_str_splitted = target_str.split('.')
    first_three_octets = '.'.join(target_str_splitted[:-1])
    if len(target_str_splitted) == 4:
        if "-" in target_str_splitted[3]:
            start, end = target_str_splitted[3].split('-')
            return [f"{first_three_octets}.{i}" for i in range(int(start), int(end)+1)]
        else:
            return [target_str]
    else:
        print(colored("\n[!] IP or IP range format is not valid\n", 'red'))

def host_discovery(target):
    """
    Discovers active hosts on the network using ICMP ping requests.

    Args:
        target (str): IP address to ping.
    """
    try:
        ping = subprocess.run(["ping", "-c", "1", target], timeout=1, stdout=subprocess.DEVNULL)
        if ping.returncode == 0:
            print(colored(f"[i] IP {target} is active", 'green'))
    except subprocess.TimeoutExpired:
        pass

def main():
    """
    Main function to execute the host discovery process.
    """
    target_str = get_arguments()
    targets = parse_target(target_str)
    print(colored("\n[+] Active hosts on the network:\n", 'green'))
    
    max_threads = 100
    with ThreadPoolExecutor(max_workers=max_threads) as executor:
        executor.map(host_discovery, targets)

if __name__ == "__main__":
    main()
