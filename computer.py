""" computer.py --- Controls PTT of a (Ham-)Radio Transceiver and receives/sends audio over UDP

This part runs on the operators computer 

* rx / tx binaries must be available through $PATH (http://www.pogo.org.uk/~mark/trx/)

"""

__author__ = "Markus (GNU/Fox)"
__copyright__ = "Copyright 2021, Markus (GNU/Fox)"
__license__ = "GPLv2"
__version__ = "0.1"
__maintainer__ = "Markus (GNU/Fox)"
__status__ = "Prototype"

import os
import sys
import socket
import time
import subprocess
from pynput import keyboard
from pynput.keyboard import Key
from threading import Lock
import argparse

from audio_handler import AudioHandler


ip = "radio-berry"
port = 27700

sTX = b"T"
sRX = b"R"
sNA = b"N"

state = sNA
state_lock = Lock()

ah = None

def open_conn_and_send(tx_rx_none):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((ip, port))     
    client.send(tx_rx_none)
    response = client.recv(4096)
    client.shutdown(socket.SHUT_RDWR)
    client.close()
    #time.sleep(1)
#enddef

def transmit():
    global state
    with state_lock:
        if state == sRX:
            state = sTX
            ah.send_audio()
            open_conn_and_send(sTX)
        elif state == sNA:
            print("transmitting not available, disable standby first --> 'R'")
        else:
            print("already transmitting")
        #endif
    #endwith
#enddef

def receive(s=False):
    global state
    with state_lock:
        if state == sTX or (state == sNA and s):
            state = sRX
            ah.receive_audio()
            open_conn_and_send(sRX)          
        else:
            print("already receiving")
        #endif
    #endiwth
#enddef

def standby(keep_rx=False):
    global state
    with state_lock:
        state = sNA
        if not keep_rx:
            ah.stop_all_audio()
            open_conn_and_send(sNA)
        else:
            ah.receive_audio()
            open_conn_and_send(sRX)
        #endif
    #endwith
#enddef

def on_press(key):
    global state
    if key == Key.alt:
        transmit()
    #endif
#enddef

def on_release(key):
    global state
    if key == Key.alt:
       receive()
    #endif
#enddef

def print_help():
    """ 
    computer.py  

    Commands are:

    exit:   will exit the program
    T:      continuous transmit
    R:      switch to receive (disables standby)
    S:      standby (disable all audio streaming on remote),
            can only be disabled with 'R'
    SR:     standby but keep receiving
    D<Nums> Send DTMF Numbers. <Nums> is a string of numbers
            example: 'D12345' would send "12345"
            All DTMF-Numbers/Charactes are available
    help:   print help  
    """
    print(print_help.__doc__)

def main():

    global ah, ip
    br = 0

    # TODO: improve this (check input types + clean up)
    parser = argparse.ArgumentParser(description="Radio side of remoteradioptt")
    parser.add_argument('-v','--verbose', type=int, dest='verbose')
    parser.add_argument('-i','--ip-address', dest='ip_address')
    parser.add_argument('-b', '--bitrate', dest='trx_bitrate')

    args = parser.parse_args()

    if args.verbose:
        if args.verbose <= 5 and args.verbose >=0:
            pass # TODO: implement debug verbosity
        else:
            print("ERROR: stdout verbosity level must be between 0 and 5")
            sys.exit()
        #endif
    #endif
    if args.ip_address:
        ip = str(args.ip_address)
    else:
        print("ERROR: IP address must be given")
    #endif
    if args.trx_bitrate:
        br = args.trx_bitrate
    else:
        br = 12000
    #endif

    print("Hello")
    print(f"IP = {ip}")
    print(f"Bitrate = {br}")

    listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
    listener.start()

    ah = AudioHandler(ip, br)

    running = True
    while running:
        try:  
            i = input("> ")
            if i == "exit":
                running = False
            elif i in ["T", "t"]:
                transmit()
            elif i in ["R", "r"]:
                receive(True)
            elif i in ["S" ,"s"]:
                standby()
            elif i in ["SR", "sr"]:
                standby(True)
            elif i in ["h", "help", "H"]:
                print_help()
            elif i[0] in ["d" ,"D"]:
                open_conn_and_send(str.encode(i))
            else:
                print("unknown command")
                print_help()
            #endif
        except:
            print("Exiting")
            running = False
    #endwhile

    standby()


if __name__ == "__main__":
    main()
