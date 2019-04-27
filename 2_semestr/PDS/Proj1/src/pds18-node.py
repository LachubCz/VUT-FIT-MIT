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

buffer_size = 16384

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--id', action="store", type=int, required=True, dest="id_",
        help="unique peer instance identifier, where you need to distinguish between them within a single guest")
    parser.add_argument('--reg-ipv4', action="store", type=str, required=True,
        help="IP address to which the peer will regularly send HELLO messages and GETLIST queries")
    parser.add_argument('--reg-port', action="store", type=int, required=True,
        help="registration node port to which the peer will regularly send HELLO messages and GETLIST queries")
    parser.add_argument('--debug', action="store_true", default=False,
        help="debug logging")

    args = parser.parse_args()

    return args

class Node(object):
    def __init__(self, args):
        self.id = args.id_
        self.reg_ipv4 = args.reg_ipv4
        self.reg_port = args.reg_port

        self.pipe = get_pipe_name("node", self.id)

        self.peers = []
        self.nodes = []

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
            data, addr = self.reg_sock.recvfrom(buffer_size)

            data = decode(data)
            type_ = data[str.encode("type")]
            type_ = type_.decode('UTF-8')

            if type_ == "hello":
                print(data)
                if data[str.encode("ipv4")].decode('UTF-8') == "0.0.0.0" and data[str.encode("port")] == 0:
                    for i, item in enumerate(self.peers):
                        if data[str.encode("username")].decode('UTF-8') == item.username_:
                            del self.peers[i]
                else:
                    self.peers.append(Peer_Record(data[str.encode("username")], data[str.encode("ipv4")], data[str.encode("port")], bytes_=True))
                print(self.peers)
            elif type_ == "getlist":
                print(data)
                self.acknowlidge(addr[0], addr[1], data[str.encode("txid")])
                is_authorized = False
                for i, item in enumerate(self.peers):
                    if item.ipv4_ == addr[0] and item.port_ == addr[1]:
                        is_authorized = True

                records = Peer_Records()
                for i, item in enumerate(self.peers):
                    records.add_record(item)

                msg = Message_List('list', 123, records)
                msg_b = msg.encoded_msg()

                if is_authorized:
                    self.reg_sock.sendto(msg_b, (addr[0], addr[1]))

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
                if data[0] == "database":
                    print(data)

                    string = "{"
                    for i, item in enumerate(self.peers):
                        string += str(item) + ','

                    if self.peers != 0:
                        string = string[:-1]

                    string += "}"

                    err_print(string)
                elif data[0] == "neighbors":
                    print(data)
                    err_print("wrong combination of command and peer/node")
                elif data[0] == "connect":
                    print(data)

                   #msg = Message_Hello('hello', self.txid, self.username, '0.0.0.0', 0)
                   #msg_b = msg.encoded_msg()
                   #self.chat_sock.sendto(msg_b, (self.reg_ipv4, self.reg_port))

                   ##changes in peer class
                   #self.next_txid()
                   #self.reg_ipv4 = data[1]
                   #self.reg_port = int(data[2])

                   ##connect from node
                   #msg = Message_Hello('hello', self.txid, self.username, self.chat_ipv4, self.chat_port)
                   #msg_b = msg.encoded_msg()
                   #self.chat_sock.sendto(msg_b, (self.reg_ipv4, self.reg_port))

                elif data[0] == "disconnect":
                    print(data)
                elif data[0] == "sync":
                    print(data)
                else:
                    #ignoring of wrong pipe messages
                    pass
            except:# Exception as e:
                #pipe is not created
                #print(e)
                pass

    def acknowlidge(self, ipv4, port, txid):
        msg = Message_Ack('ack', txid)
        msg_b = msg.encoded_msg()
        self.reg_sock.sendto(msg_b, (ipv4, port))

if __name__ == "__main__":
    args = get_args()
    node = Node(args)
    node.run()
