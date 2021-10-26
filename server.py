#!/usr/bin/env python3
# ------------------------------------------------------------------------------
#  Server side
#   By Dmitri Dan
# ------------------------------------------------------------------------------
from socket import *
import time
import sqlite3
# ------------------------------------------------------------------------------------
HOST = '127.0.0.1'              # Standard loopback interface address (localhost)
PORT = 55555                    # Port to listen on
SERVER_ADDRESS = (HOST, PORT)
BUFFER_SIZE = 1024
DB_Name = 'example.db'
# socket.settimeout(0)  # --- no needs run in loop. easier just wait to someone who will connect
# -----------------------------------------------------------------------------------

with socket() as acceptSocket:  # AF_INET, SOCK_STREAM <=> IP4, TCP
    acceptSocket.bind(SERVER_ADDRESS)
    acceptSocket.listen(16)

    while True:
        client_socket, client_address = acceptSocket.accept()
        data = client_socket.recv(BUFFER_SIZE)
        client_socket.close()

        report = str.split(data.decode())                       # ---convert received data to list[]
        currentTime = time.strftime("%Y-%m-%d  %H:%M", time.localtime())

        try:
            db_connector = sqlite3.connect(DB_Name)
            db_cursor = db_connector.cursor()

            sql_create_table = """ CREATE TABLE IF NOT EXISTS station_status (
                                            id integer PRIMARY KEY,
                                            time text ,
                                            alarm1 integer,
                                            alarm2 integer
                                        ); """

            db_cursor.execute(sql_create_table)

            sql_insert = ''' INSERT OR REPLACE INTO station_status( id, time, alarm1, alarm2 )
                                     VALUES(?,?,?,?) '''
            sql_data = (report[0], currentTime, report[1], report[2])

            db_cursor.execute(sql_insert, sql_data)
            db_connector.commit()

            '''   # --- just to see all table after action ------
            print(db_cursor.rowcount, " record inserted, ID:", db_cursor.lastrowid)

            db_cursor.execute("SELECT * FROM station_status")
            rows = db_cursor.fetchall()
            for row in rows:
                print(row)
            '''

        except BaseException as e:
            print("UnEXPECTED ERROR \n" + e.__repr__())
        finally:
            if db_connector:
                db_connector.close()
