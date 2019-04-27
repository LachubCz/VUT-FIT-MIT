import os
import sys
import time
import _thread
import socket
import argparse

from messages import Message_Hello, Message_GetList, Message_List, Message_Message, Message_Update, Message_Disconnect, Message_Ack, Message_Error
from messages import Peer_Record, Peer_Records, Db_Record, Db_Records
from bencode import encode, decode
from tools import err_print, get_pipe_name

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--id', action="store", type=int,
        help="unique peer instance identifier, where you need to distinguish between them within a single guest")
    parser.add_argument('--reg-ipv4', action="store", type=str,
        help="IP address to which the peer will regularly send HELLO messages and GETLIST queries")
    parser.add_argument('--reg-port', action="store", type=int,
        help="registration node port to which the peer will regularly send HELLO messages and GETLIST queries")

    args = parser.parse_args()

    return args

class Node(object):
    def __init__(self, args):
        self.id = args.id_
        self.reg_ipv4 = args.reg_ipv4
        self.reg_port = args.reg_port

        self.pipe = get_pipe_name("node", self.id)

        try:
            self.reg_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.reg_sock.bind((self.reg_ipv4, self.reg_port))
        except:
            err_print("Cannot assign requested reg address or port.")
            sys.exit(-1)

    def run(self):
        _thread.start_new_thread(self.listen_reg,  ( ))
        _thread.start_new_thread(self.listen_pipe, ( ))

        while True:
            pass

    def listen_reg(self):
        while True:
            data, addr = self.reg_sock.recvfrom(1024)
            data = decode(data)
            type_ = decoded[str.encode("type")]
            if type_ == "hello":
                pass
            elif type_ == "getlist":
                pass
            elif type_ == "error":
                pass
            elif type_ == "list":
                pass
            elif type_ == "message":
                pass
            elif type_ == "update":
                pass
            elif type_ == "disconnect":
                pass
            elif type_ == "ack":
                pass
            else:
                pass


    def listen_pipe(self):
        while True:
            try:
                with open(self.pipe) as p:
                    data = p.read()
                data = data.split()
                if data[0] == "database":
                    print(data)
                elif data[0] == "neighbors":
                    print(data)
                elif data[0] == "connect":
                    print(data)
                elif data[0] == "disconnect":
                    print(data)
                elif data[0] == "sync":
                    print(data)
                else:
                    #ignoring of wrong pipe messages
                    pass
            except:
                #pipe is not created
                pass


if __name__ == "__main__":
    args = get_args()
    node = Node(args)
    node.run()
