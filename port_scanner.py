#!/usr/bin/env python3
"""
A Fast TCP Port Scanner.

This script scans TCP ports on a target host within a specified port range.
It utilizes threading for faster scanning.

Usage:
  python3 port_scanner.py -t <target> -p <port_range>

Example:
  python3 port_scanner.py -t 10.0.0.1 -p 1-100
"""

import socket
import argparse
import signal
import sys
from concurrent.futures import ThreadPoolExecutor
from termcolor import colored

open_sockets = []


def signal_handler(sig, frame):
    """
    Handles SIGINT signal (Ctrl+C) gracefully.
    Closes all open sockets and exits the program.

    Args:
        sig: Signal number
        frame: Current stack frame
    """
    print("[!] Ctrl + C pressed...")
    for sock in open_sockets:
        sock.close()
    sys.exit(1)


signal.signal(signal.SIGINT, signal_handler)


def get_arguments():
    """
    Parses command line arguments.

    Returns:
        tuple: A tuple containing the target IP address and port range.
    """
    parser = argparse.ArgumentParser(description='Fast TCP Port Scanner')
    parser.add_argument("-t", "--target", dest="target", required=True,
                        help="Victim target to scan (Ex: -t 192.168.1.1)")
    parser.add_argument("-p", "--port", dest="port", required=True,
                        help="Port range to scan (Ex: -p 1-100)")
    options = parser.parse_args()

    return options.target, options.port


def create_socket():
    """
    Creates a TCP socket.

    Returns:
        socket: A TCP socket object.
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(1)
    open_sockets.append(s)
    return s


def port_scanner(port, host):
    """
    Scans a single port on the target host.

    Args:
        port (int): The port number to scan.
        host (str): The target IP address.
    """
    s = create_socket()
    try:
        s.connect((host, port))
        s.sendall(b"HEAD / HTTP/1.0\r\n\r\n")
        response = s.recv(1024)
        response = response.decode(errors='ignore').split('\n')
        if response:
            print(colored(f"\n[+] Port {port} is open", 'green'))

            for line in response:
                print(colored(f"{line}", 'white'))
        else:
            print(colored(f"\n[+] Port {port} is open", 'green'))
    except (socket.timeout, ConnectionRefusedError):
        pass
    finally:
        s.close()


def scan_ports(ports, target):
    """
    Scans multiple ports on the target host using threading.

    Args:
        ports (list): List of port numbers to scan.
        target (str): The target IP address.
    """
    with ThreadPoolExecutor(max_workers=100) as executor:
        executor.map(lambda port: port_scanner(port, target), ports)


def parse_ports(ports_str):
    """
    Parses the port range string.

    Args:
        ports_str (str): String representing port range (Ex: '1-100').

    Returns:
        list: List of port numbers to scan.
    """
    if '-' in ports_str:
        start, end = map(int, ports_str.split('-'))
        return range(start, end + 1)
    elif ',' in ports_str:
        return map(int, ports_str.split(','))
    else:
        return [int(ports_str)]


def main():
    """
    Main function to execute the port scanning process.
    """
    target, ports_str = get_arguments()
    ports = parse_ports(ports_str)
    scan_ports(ports, target)


if __name__ == "__main__":
    main()
