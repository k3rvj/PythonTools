#!/usr/bin/python3

""" Libraries """
import sys, signal, requests

""" Variables """
main_url = "http://192.168.3.187" # edit this section with your local IP
squid_proxy = {'http':'http://192.168.3.187:3128'} # edit this section with your local IP

""" Functions """
# stop attack function
def stop_attack(sig, frame):
    print("ctrl + c  -> Exiting.")
    sys.exit(1)

signal.signal(signal.SIGINT, stop_attack)

# port discovery function
def port_discovery():
    # common TCP ports
    ports = {20, 21, 22, 23, 25, 53, 80, 110, 119, 123, 143, 161, 194, 443, 465, 514, 587, 631, 636, 993, 995, 1080, 1433, 1521, 1723, 2082, 2083, 3306, 3389, 5432, 5900, 5901, 8080, 8443, 10000, 10050, 10051, 20000, 32768, 32769, 32770, 32771, 32772, 32773, 32774, 32775, 32776, 32777, 32778, 32779, 49152, 49153, 49154, 49155, 49156, 49157, 49158, 49159, 49160, 49161, 49162, 49163, 49164, 49165, 49166, 49167, 49168, 49169, 49170, 49171, 49172, 49173, 49174, 49175, 49176, 49177, 49178, 49179, 49180, 49181, 49182, 49183, 49184, 49185, 49186, 49187, 49188, 49189, 49190, 49191, 49192, 49193, 49194, 49195, 49196, 49197, 49198, 49199, 49200}
    # iterate over each port
    for port in ports:
        response = requests.get(main_url + ':' + str(port), proxies=squid_proxy)
        if response.status_code != 503:
            print("\n[+] Port " + str(port) + " - OPEN")

""" Main """
if __name__ == "__main__":
    port_discovery()

