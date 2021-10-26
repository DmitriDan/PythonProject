#!/usr/bin/env python3
# ------------------------------------------------------------------------------
#  Client side
#   By Dmitri Dan
# ------------------------------------------------------------------------------
import time
from socket import *
# ------------------------------------------------------------------------------
SOURCE_FILE = "status.txt"
HOST = '127.0.0.1'                       # Standard loopback interface address (localhost)
PORT = 55555                             # Port to listen on
SERVER_ADDRESS = (HOST, PORT)
SLEEP_TIME = 60                          # Sleep time in seconds
# ------------------------------------------------------------------------------
# TCP connect to server and run in loop
while True:
    try:
        with open(SOURCE_FILE) as f:
            reportStr = f.read()

    except FileNotFoundError as e:
        print("Cannot find file " + SOURCE_FILE + "\n" + e.strerror)
    except PermissionError as e:
        print("Cannot read from " + SOURCE_FILE + "\n" + e.strerror)
    except BaseException as e:
        print("Some unexpected error")

    try:
        s = socket()
        s.connect(SERVER_ADDRESS)
        s.send(reportStr.encode())
        s.close()
    except ConnectionRefusedError as e:
        print("CONNECTION ERROR \n" + e.strerror)
    except ConnectionError as e:
        print("CONNECTION ERROR \n" + e.strerror)
    except BaseException as e:
        print("UnEXPECTED ERROR \n" + e.__repr__())

    time.sleep(SLEEP_TIME)

