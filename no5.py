#!/usr/bin/env python3
# Foundations of Python Network Programming, Third Edition
# https://github.com/brandon-rhodes/fopnp/blob/m/py3/chapter03/tcp_sixteen.py
# Simple TCP client and server that send and receive 16 octets

import argparse, socket
import sys
import time
import glob
import os
# import string

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received'
                           ' %d bytes before the socket closed'
                           % (length, len(data)))
        data += more
    return data

def server(interface, port):
    c = 0
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((interface, port))
        sock.listen(1)
        sc, sockname = sock.accept()
        if c==0:
            print('Waiting to accept a new connection...')
            print('We have accepted a connection from', sockname)
            c+=1
        print('Socket name:', sc.getsockname())
        print('Socket peer:', sc.getpeername())
        len_msg = recvall(sc, 3)
        message = recvall(sc, int(len_msg))

        #Decode and split the message from client
        acc_message = message.decode()
        str_message = acc_message.split()

        #Condition to follow for quit command
        if str_message[0] == "quit":
            print("Server shutdown..")
            sc.close()
            sys.exit(0)

def client(host, port):
    while True:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        print('Client has been assigned socket name', sock.getsockname())
        #Input and split message
        input_msg = input("> ")
        msgSplit = input_msg.split()
       
        #Condition to follow for quit command
        if msgSplit[0] == "quit":
            msg = input_msg.encode()
            len_msg = b"%03d" % (len(msg),)
            msg = len_msg + msg
            sock.sendall(msg) 
            time.sleep(2)
            print('Client shutdown...')
            sock.close()
            sys.exit(0)

if __name__ == '__main__':
    choices = {'client': client, 'server': server}
    parser = argparse.ArgumentParser(description='Send and receive over TCP')
    parser.add_argument('role', choices=choices, help='which role to play')
    parser.add_argument('host', help='interface the server listens at;'
                        ' host the client sends to')
    parser.add_argument('-p', metavar='PORT', type=int, default=1060,
                        help='TCP port (default 1060)')
    args = parser.parse_args()
    function = choices[args.role]
    function(args.host, args.p)