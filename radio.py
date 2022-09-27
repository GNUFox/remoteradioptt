""" radio.py --- Controls PTT of a (Ham-)Radio Transceiver and receives/sends audio over UDP

This part runs on the raspberry Pi that controls the radio

* PTT is being controlled by a GPIO pin.
* rx / tx binaries must be available through $PATH (http://www.pogo.org.uk/~mark/trx/)
* RPi.GPIO must be installed (pip) (https://pypi.org/project/RPi.GPIO/)

"""

__author__ = "Markus (GNU/Fox)"
__copyright__ = "Copyright 2021, Markus (GNU/Fox)"
__license__ = "GPLv2"
__version__ = "0.1"
__maintainer__ = "Markus (GNU/Fox)"
__status__ = "Prototype"


import RPi.GPIO as GPIO
import os
import sys
import subprocess
import socket
import threading
import time
import argparse

from audio_handler import AudioHandler
from dtmf import DTMF

ptt_pin = 21

server = None
ip = "0.0.0.0"
port = 27700
running = True
sTX = b"T"
sRX = b"R"
sNA = b"N"

ah = None
dialer = None
process_lock = threading.Lock()

#TODO: ERROR handling / locking / move stuffi into own file / class

def set_up_server(ip, port):
    global server
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((ip, port))
        server.listen(5)
    except:
        print("Error while starting the server")
    #endtry
#enddef

def handle_client(client_socket):
    global running
    # show the data from the client
    request = client_socket.recv(1024)

    # Return a packet
    client_socket.send("ACK!".encode())
    client_socket.close()

    if request == sTX:
        print("enable transmit ", end="")
        try:
            GPIO.output(ptt_pin, 1)
            ah.receive_audio()
            print("NOW TRANSMITTING")
        except:
            print("BAD STUFF HAPPENED while trying to transmit")
            GPIO.output(ptt_pin, 0)
        #endtry
    elif request == sRX:
        print("disable transmit ", end="")
        try:
            GPIO.output(ptt_pin, 0)
            ah.send_audio()
            print("NOW RECEIVING")
        except:
            print("BAD STUFF HAPPENED while trying to receive")
        #endtry
    elif request == sNA:
        print("disabling everything")
        GPIO.output(ptt_pin, 0)
        ah.stop_all_audio()
    elif request.decode('utf-8')[0] in ["d", "D"]:
        print("Dialing number")
        number = request.decode('utf-8')[1:]
        if number:
            GPIO.output(ptt_pin, 1)
            time.sleep(0.25)
            dialer.dial(number)
            time.sleep(0.25)
            GPIO.output(ptt_pin, 0)
            ah.send_audio()
        else:
            print("Warning, wrong input")
    else:
        print("WARNING: UNRECOGNIZED INPUT")
    #endif
#enddef



def main():
    global ah, dialer, ip
    br = 0

    # TODO: improve this (check input types + clean up)
    parser = argparse.ArgumentParser(description="Radio side of remoteradioptt")
    parser.add_argument('-v','--verbose', type=int, dest='verbose', help="verbostiy level")
    parser.add_argument('-i','--ip-address', dest='ip_address', help="IP address / Hostname of the operator pc")
    parser.add_argument('-b', '--bitrate', dest='trx_bitrate', help="bitrate passed to trx (for rx ad tx audio)")

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
        ip = args.ip_address
    else:
        print("ERROR: IP address must be given")
    #endif
    if args.trx_bitrate:
        br = args.trx_bitrate
    else:
        br = 12000
    #endif

    print("Hello")

    # init GPIO
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(ptt_pin, GPIO.OUT)
    GPIO.output(ptt_pin, 0)

    set_up_server("0.0.0.0", port)
    ah = AudioHandler(ip, br)
    dialer = DTMF()

    try:
        while running:
            client, addr = server.accept()
            #print(f"[*] Accepted connection from: {addr[0]}:{addr[1]}")
            # activate the function to handle the data from client
            client_handler = threading.Thread(target = handle_client, args=(client,))
            client_handler.start()
            client_handler.join()
    except KeyboardInterrupt:
        print("Keyboard interrupt, shutting down")
    #endif

    server.shutdown(socket.SHUT_RDWR)
    server.close()
    GPIO.output(ptt_pin, 0)
    GPIO.cleanup()

    exit(0)
#enddef


if __name__ == "__main__":
    main()
