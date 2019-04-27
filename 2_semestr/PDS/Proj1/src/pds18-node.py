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
        self.debug = args.debug

        self.pipe = get_pipe_name("node", self.id)

        self.txid = 0

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
            if self.debug:
                print(data)
            type_ = data[str.encode("type")]
            type_ = type_.decode('UTF-8')


            if type_ == "hello":
                if data[str.encode("ipv4")].decode('UTF-8') == "0.0.0.0" and data[str.encode("port")] == 0:
                    for i, item in enumerate(self.peers):
                        if data[str.encode("username")].decode('UTF-8') == item.username_:
                            del self.peers[i]
                else:
                    self.peers.append(Peer_Record(data[str.encode("username")], data[str.encode("ipv4")], data[str.encode("port")], bytes_=True))


            elif type_ == "getlist":
                is_authorized = False
                for i, item in enumerate(self.peers):
                    if item.ipv4_ == addr[0] and item.port_ == addr[1]:
                        is_authorized = True
                        self.acknowlidge(addr[0], addr[1], data[str.encode("txid")])

                if not is_authorized:
                    #error send
                    #continue
                    pass
                else:
                    records = Peer_Records()
                    for i, item in enumerate(self.peers):
                        records.add_record(item)
    
                    msg = Message_List('list', data[str.encode("txid")], records)
                    msg_b = msg.encoded_msg()
                    self.send_message_to(msg_b, addr[0], addr[1])



            elif type_ == "error":
                pass


            elif type_ == "update":
                #db_records = Db_Records()

                new_nodes_ipv4 = []
                new_nodes_port = []
                for e, elem in enumerate(sorted(data[str.encode("db")].keys())):
                    if elem.decode('UTF-8').split(",")[0] == addr[0] and int(elem.decode('UTF-8').split(",")[1]) == addr[1]:
                        p_records = Peer_Records()
                        for i in range(len(data[str.encode("db")][elem].keys())):

                            rec_l = Peer_Record(data[str.encode("db")][elem][str.encode(str(i))][str.encode("username")], data[str.encode("db")][elem][str.encode(str(i))][str.encode("ipv4")], data[str.encode("db")][elem][str.encode(str(i))][str.encode("port")], bytes_=True)
                            p_records.add_record(rec_l)

                        rec_h = Db_Record(elem.decode('UTF-8').split(",")[0], int(elem.decode('UTF-8').split(",")[1]), p_records)
                        #db_records.add_record(rec_h)
                        #merge records without duplicates
                    else:
                        new_nodes_ipv4.append(elem.decode('UTF-8').split(",")[0])
                        new_nodes_port.append(int(elem.decode('UTF-8').split(",")[1]))

                #update messages to new nodes


            elif type_ == "disconnect":
                pass


            elif type_ == "ack":
                pass


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


                if data[0] == "database":
                    string = "{"
                    for i, item in enumerate(self.peers):
                        string += str(item) + ','

                    if len(self.peers) != 0:
                        string = string[:-1]

                    string += "}"

                    err_print(string)


                elif data[0] == "neighbors":
                    string = "{"
                    for i, item in enumerate(self.nodes):
                        string += "{\'ipv4\': \'" + item.split(',')[0] + "\', \'port\': " + int(item.split(',')[1]) + "}"
                        string += item + ','

                    if len(self.nodes) != 0:
                        string = string[:-1]

                    string += "}"

                    err_print(string)


                elif data[0] == "connect":
                    #send update message
                    pass
                elif data[0] == "disconnect":
                    #send disconnect message
                    pass
                elif data[0] == "sync":
                    #send update message to all nodes
                    pass


                else:
                    #ignore other pipe messages
                    pass
            except:# Exception as e:
                #print(e)
                #pipe is not created
                pass

    def acknowlidge(self, ipv4, port, txid):
        msg = Message_Ack('ack', txid)
        msg_b = msg.encoded_msg()
        self.reg_sock.sendto(msg_b, (ipv4, port))



    def next_txid(self):
        if self.txid == 65535:
            self.txid = 0
        else:
            self.txid += 1


    def send_message_to(self, msg_b, ipv4, port):
        self.chat_sock.sendto(msg_b, (ipv4, port))
        self.next_txid()


if __name__ == "__main__":
    args = get_args()
    node = Node(args)
    node.run()
