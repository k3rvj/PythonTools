#!/usr/bin/python3

# Imports
import os, sys

try:

    os.system("clear") 
    print("%-20s | %-18s |" % ("CIDR Range:",sys.argv[1]+"/"+sys.argv[2]))
    # IP
    ip = str(sys.argv[1]).split(".",4)
    octet_1 = int(ip[0])
    octet_2 = int(ip[1])
    octet_3 = int(ip[2])
    octet_4 = int(ip[3])

    # each IP octet to binary
    octet_1_bin = bin(octet_1)[2:].zfill(8)
    octet_2_bin = bin(octet_2)[2:].zfill(8)
    octet_3_bin = bin(octet_3)[2:].zfill(8)
    octet_4_bin = bin(octet_4)[2:].zfill(8)

    ip = str(octet_1)+"."+str(octet_2)+"."+str(octet_3)+"."+str(octet_4)
    left = str(octet_1_bin)+str(octet_2_bin)+str(octet_3_bin)+str(octet_4_bin)
    binaryIP = str(octet_1_bin)+str(octet_2_bin)+str(octet_3_bin)+str(octet_4_bin)
    binary = str(octet_1_bin)+"."+str(octet_2_bin)+"."+str(octet_3_bin)+"."+str(octet_4_bin)

    binary = ""
    for number in range(0, 32):
        if number < int(sys.argv[2]):
            binary += "1"
        else:
            binary += "0"            


    octet_1 = int(binary[0:8], 2)
    octet_2 = int(binary[8:16], 2)
    octet_3 = int(binary[16:24], 2)       
    octet_4 = int(binary[24:32], 2)       

    # each IP octet to binary
    octet_1_bin = bin(octet_1)[2:].zfill(8)
    octet_2_bin = bin(octet_2)[2:].zfill(8)
    octet_3_bin = bin(octet_3)[2:].zfill(8)
    octet_4_bin = bin(octet_4)[2:].zfill(8)

    networkMask = str(octet_1)+"."+str(octet_2)+"."+str(octet_3)+"."+str(octet_4)
    right = str(octet_1_bin)+str(octet_2_bin)+str(octet_3_bin)+str(octet_4_bin)
    binary = str(octet_1_bin)+"."+str(octet_2_bin)+"."+str(octet_3_bin)+"."+str(octet_4_bin)
    networkMarkBinary = str(octet_1_bin)+str(octet_2_bin)+str(octet_3_bin)+str(octet_4_bin)

    print("%-20s | %-18s | %-18s |" % ("Netmask:",networkMask,binary))

    binary = ""
    for i in range(0,32):
        if i < int(sys.argv[2]): 
            if left[i] == right[i]:
                binary+="1"
            else:
                binary+="0"
        else:
            binary+="0"

    octet_1 = int(binary[0:8], 2)
    octet_2 = int(binary[8:16], 2)
    octet_3 = int(binary[16:24], 2)       
    octet_4 = int(binary[24:32], 2)       

    # each IP octet to binary
    octet_1_bin = bin(octet_1)[2:].zfill(8)
    octet_2_bin = bin(octet_2)[2:].zfill(8)
    octet_3_bin = bin(octet_3)[2:].zfill(8)
    octet_4_bin = bin(octet_4)[2:].zfill(8)

    networkID = str(octet_1)+"."+str(octet_2)+"."+str(octet_3)+"."+str(octet_4)
    binary = str(octet_1_bin)+"."+str(octet_2_bin)+"."+str(octet_3_bin)+"."+str(octet_4_bin)

    print("%-20s | %-18s | %-18s |" % ("Network ID:",networkID,binary))

    binary = ""
    for i in range(0,32):
        if binaryIP[i] != str("."):
            if i < int(sys.argv[2]):
                binary += binaryIP[i]
            else:
                binary += "1"
        else:
            binary+=""

    octet_1 = int(binary[0:8], 2)
    octet_2 = int(binary[8:16], 2)
    octet_3 = int(binary[16:24], 2)       
    octet_4 = int(binary[24:32], 2)       

    # each IP octet to binary
    octet_1_bin = bin(octet_1)[2:].zfill(8)
    octet_2_bin = bin(octet_2)[2:].zfill(8)
    octet_3_bin = bin(octet_3)[2:].zfill(8)
    octet_4_bin = bin(octet_4)[2:].zfill(8)

    broadcast = str(octet_1)+"."+str(octet_2)+"."+str(octet_3)+"."+str(octet_4)
    binary = str(octet_1_bin)+"."+str(octet_2_bin)+"."+str(octet_3_bin)+"."+str(octet_4_bin)

    print("%-20s | %-18s | %-18s |" % ("Broadcast Address:",broadcast,binary))

    counter=0
    networkMarkBinary = "".join(reversed(networkMarkBinary))
    for i in range(0,32):
        if networkMarkBinary[i] == "0":
            counter+=1 
        else:
            break

    print("%-20s | %-18d |" % ("Total Hosts:",pow(2,counter)))


except:
    print("[!] Usage --> python3 CIDR_to_IP_Range.py 192.160.3.9 23")