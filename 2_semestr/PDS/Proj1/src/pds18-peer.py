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

    parser.add_argument('--id', action="store", type=int, required=True, dest="id_",
        help="unique peer instance identifier, where you need to distinguish between them within a single guest")
    parser.add_argument('--username', action="store", type=str, required=True,
        help="unique username identifying this peera within the chat")
    parser.add_argument('--chat-ipv4', action="store", type=str, required=True,
        help="IP address on which the peer listens and receives messages from other peers or nodes")
    parser.add_argument('--chat-port', action="store", type=int, required=True,
        help="port on which the peer listens and receives messages from other peers or nodes")
    parser.add_argument('--reg-ipv4', action="store", type=str, required=True,
        help="IP address to which the peer will regularly send HELLO messages and GETLIST queries")
    parser.add_argument('--reg-port', action="store", type=int, required=True,
        help="registration node port to which the peer will regularly send HELLO messages and GETLIST queries")

    args = parser.parse_args()

    return args


class Peer(object):
    def __init__(self, args):
        self.id = args.id_
        self.username = args.username
        self.chat_ipv4 = args.chat_ipv4
        self.chat_port = args.chat_port
        self.reg_ipv4 = args.reg_ipv4
        self.reg_port = args.reg_port

        self.pipe = get_pipe_name("peer", self.id)

        self.txid = 0

        try:
            self.chat_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.chat_sock.bind((self.chat_ipv4, self.chat_port))
        except:
            err_print("Cannot assign requested chat address or port.")
            sys.exit(-1)

    def run(self):
        _thread.start_new_thread(self.listen_chat, ( ))
        _thread.start_new_thread(self.listen_pipe, ( ))

        while True:
            pass

    def listen_chat(self):
        while True:
            data, addr = self.chat_sock.recvfrom(1024)
            data = decode(data)
            type_ = decoded[str.encode("type")]
            if type_ == "hello":
                print(data)
            elif type_ == "getlist":
                print(data)
            elif type_ == "error":
                print(data)
            elif type_ == "list":
                print(data)
            elif type_ == "message":
                print(data)
            elif type_ == "update":
                print(data)
            elif type_ == "disconnect":
                print(data)
            elif type_ == "ack":
                print(data)
            else:
                print(data)


    def listen_pipe(self):
        while True:
            try:
                with open(self.pipe) as p:
                    data = p.read()
                data = data.split()
                if data[0] == "message":
                    print(data)
                elif data[0] == "getlist":
                    print(data)
                elif data[0] == "peers":
                    print(data)
                elif data[0] == "reconnect":
                    print(data)
                    #disconnect from node
                    msg = Message_Hello('hello', self.txid, self.username, '0.0.0.0', 0)
                    msg_b = msg.encoded_msg()

                    self.chat_sock.sendto(msg_b, (self.reg_ipv4, self.reg_port))
                    self.next_txid()
                    #connect from node
                    self.reg_ipv4 = data[1]
                    self.reg_port = data[2]

                    msg = Message_Hello('hello', self.txid, self.username, self.chat_ipv4, self.chat_port)
                    msg_b = msg.encoded_msg()
                    self.chat_sock.sendto(msg_b, (self.reg_ipv4, self.reg_port))
                else:
                    #ignoring of wrong pipe messages
                    pass
            except:
                #pipe is not created
                pass

    def next_txid(self):
        if txid == 65535:
            self.txid = 0
        else:
            self.txid += 1

if __name__ == "__main__":
    args = get_args()
    peer = Peer(args)
    peer.run()
