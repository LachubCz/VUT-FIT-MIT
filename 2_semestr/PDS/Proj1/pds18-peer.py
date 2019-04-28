import os
import sys
import time
import socket
import _thread
import argparse
from timeit import default_timer as timer

from messages import Message_Hello, Message_GetList, Message_List, Message_Message, Message_Update, Message_Disconnect, Message_Ack, Message_Error
from messages import Peer_Record, Peer_Records, Db_Record, Db_Records
from bencode import encode, decode
from tools import err_print, get_pipe_name

buffer_size = 16384

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
    parser.add_argument('--debug', action="store_true", default=False,
        help="debug logging")

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
        self.debug = args.debug

        self.peers = Peer_Records()
        self.pipe = get_pipe_name("peer", self.id)
        
        self.txid = 0

        self.print_ack = False
        self.actual_peers = False
        self.print_nextlist = False

        try:
            self.chat_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.chat_sock.bind((self.chat_ipv4, self.chat_port))
        except:
            err_print("Cannot assign requested chat address or port.")
            sys.exit(-1)


    def run(self):
        _thread.start_new_thread(self.timeout_hanle, ( ))
        _thread.start_new_thread(self.listen_chat, ( ))
        _thread.start_new_thread(self.listen_pipe, ( ))
        
        while True:
            pass


    def timeout_hanle(self):
        while True:
            msg = Message_Hello('hello', self.txid, self.username, self.chat_ipv4, self.chat_port)
            msg_b = msg.encoded_msg()
            self.send_message(msg_b)
            time.sleep(10)


    def listen_chat(self):
        while True:
            data, addr = self.chat_sock.recvfrom(buffer_size)
            data = decode(data)
            if self.debug:
                print(data)
            type_ = data[str.encode("type")]
            type_ = type_.decode('UTF-8')


            if type_ == "error":
                pass


            elif type_ == "list":
                
                self.peers = Peer_Records()
                for i in range(len(data[str.encode("peers")].keys())):
                    rec = Peer_Record(data[str.encode("peers")][str.encode(str(i))][str.encode("username")], data[str.encode("peers")][str.encode(str(i))][str.encode("ipv4")], data[str.encode("peers")][str.encode(str(i))][str.encode("port")], bytes_=True)
                    self.peers.add_record(rec)

                self.actual_peers = True

                if self.print_nextlist:
                    string = "{"
                    for i, item in enumerate(self.peers.records):
                        string += str(item) + ','

                    if self.peers != 0:
                        string = string[:-1]

                    string += "}"
                    err_print(string)
                    self.print_nextlist = False


            elif type_ == "message":
                print(data[str.encode("message")].decode('UTF-8'))


            elif type_ == "ack":
                if self.print_ack:
                    print("Message GETLIST acknowlidged.")
                    self.print_ack = False


            else:
                #ignore other messages
                pass


    def listen_pipe(self):
        while True:
            try:
                with open(self.pipe) as p:
                    data = p.read()
                data = data.split()
                if self.debug:
                    print(data)


                if data[0] == "message":
                    self.actual_peers = False

                    msg = Message_GetList('getlist', self.txid)
                    msg_b = msg.encoded_msg()
                    self.send_message(msg_b)

                    while True:
                        if self.actual_peers:
                            break

                    if data[1] == self.username:
                        for i, item in enumerate(self.peers.records):
                            if data[2] == item.username_:
                                text = ""
                                for e, elem in enumerate(data[3:]):
                                    if e == 0:
                                        text += elem
                                    else:
                                        text += " " + elem

                                msg = Message_Message('message', self.txid, self.username, item.username_, text)
                                msg_b = msg.encoded_msg()
                                self.send_message_to(msg_b, item.ipv4_, item.port_)


                elif data[0] == "getlist":
                    msg = Message_GetList('getlist', self.txid)
                    msg_b = msg.encoded_msg()
                    self.print_ack = True
                    self.send_message(msg_b)


                elif data[0] == "peers":
                    msg = Message_GetList('getlist', self.txid)
                    msg_b = msg.encoded_msg()
                    self.print_nextlist = True
                    self.send_message(msg_b)


                elif data[0] == "reconnect":
                    msg = Message_Hello('hello', self.txid, self.username, '0.0.0.0', 0)
                    msg_b = msg.encoded_msg()
                    self.send_message(msg_b)

                    self.reg_ipv4 = data[1]
                    self.reg_port = int(data[2])

                    msg = Message_Hello('hello', self.txid, self.username, self.chat_ipv4, self.chat_port)
                    msg_b = msg.encoded_msg()
                    self.send_message(msg_b)


                else:
                    #ignore other pipe messages
                    pass
            except Exception as e:
                if type(e).__name__ != 'FileNotFoundError':
                    print(e)
                #pipe is not created
                pass


    def next_txid(self):
        if self.txid == 65535:
            self.txid = 0
        else:
            self.txid += 1


    def send_message(self, msg_b):
        self.chat_sock.sendto(msg_b, (self.reg_ipv4, self.reg_port))
        self.next_txid()


    def send_message_to(self, msg_b, ipv4, port):
        self.chat_sock.sendto(msg_b, (ipv4, port))
        self.next_txid()


if __name__ == "__main__":
    args = get_args()
    peer = Peer(args)
    peer.run()
