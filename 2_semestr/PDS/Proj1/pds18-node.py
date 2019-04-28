#!/usr/bin/env python3
#################################################################################
# Description:  File contains pds18-node implemetation
#               
# Author:      Petr Buchal         <petr.buchal@lachub.cz>
#
# Date:     2019/04/28
# 
# Note:     This source code is part of PDS project 2019.
#################################################################################

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

        self.local_peers = []
        self.local_peers_timeouts = []
        self.acks = {}
        self.nodes = {}
        self.nodes_timeouts = {}
        self.nodes_last_notification = {}

        try:
            self.reg_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.reg_sock.bind((self.reg_ipv4, self.reg_port))
        except:
            err_print("Cannot assign requested reg address or port.")
            sys.exit(-1)


    def run(self):
        """
        main method
        """
        _thread.start_new_thread(self.listen_reg,  ( ))
        _thread.start_new_thread(self.listen_pipe, ( ))
        _thread.start_new_thread(self.timeout_hanle, ( ))

        while True:
            pass


    def timeout_hanle(self):
        """
        method for handeling of timeouts
        """
        while True:
            try:
                #delete inactive peers
                to_delete = []
                for i, item in enumerate(self.local_peers_timeouts):
                    if (timer() - item) > 30:
                        to_delete.append(i)

                for i, item in enumerate(reversed(to_delete)):
                    del self.local_peers[i]
                    del self.local_peers_timeouts[i]

                #delete inactive nodes
                to_delete = []
                for i, item in enumerate(self.nodes_timeouts.keys()):
                    if (timer() - self.nodes_timeouts[item]) > 12:
                        to_delete.append(item)

                for i, item in enumerate(to_delete):
                    del self.nodes[item]
                    del self.nodes_timeouts[item]
                    del self.nodes_last_notification[item]

                #waiting for ACKs
                to_delete = []
                for i, item in enumerate(self.acks.keys()):
                    if (timer() - self.acks[item][0]) > 2:
                        msg = Message_Error('error', self.txid, "ACK for message with txid {} wasn't recieved." .format(item))
                        msg_b = msg.encoded_msg()
                        self.send_message_to(msg_b, self.acks[item][2], self.acks[item][3])

                        err_print("ACK for message with txid {} wasn't recieved." .format(item))
                        to_delete.append(item)

                for i, item in enumerate(to_delete):
                    del self.acks[item]

                #send notification to nodes
                for i, item in enumerate(self.nodes_last_notification.keys()):
                    if (timer() - self.nodes_last_notification[item]) > 4:
                        recs = Db_Records()

                        records = Peer_Records()
                        for e, elem in enumerate(self.local_peers):
                            records.add_record(elem)

                        rec_db = Db_Record(self.reg_ipv4, self.reg_port, records)
                        recs.records.append(rec_db)

                        for e, elem in enumerate(self.nodes.keys()):
                            if self.nodes[elem] != -1:
                                rec_db = Db_Record(elem.split(",")[0], int(elem.split(",")[1]), self.nodes[elem])
                                recs.records.append(rec_db)

                        msg = Message_Update('update', self.txid, recs)
                        msg_b = msg.encoded_msg()
                        self.send_message_to(msg_b, item.split(",")[0], int(item.split(",")[1]))
                        self.nodes_last_notification[item] = timer()

                time.sleep(0.5)
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                err_print(exc_type, fname, exc_tb.tb_lineno)


    def listen_reg(self):
        """
        method for handeling of network listening
        """
        while True:
            try:
                data, addr = self.reg_sock.recvfrom(buffer_size)
                data = decode(data)
                if self.debug:
                    err_print(addr, data)
                type_ = data[str.encode("type")]
                type_ = type_.decode('UTF-8')


                if type_ == "hello":
                    if data[str.encode("ipv4")].decode('UTF-8') == "0.0.0.0" and data[str.encode("port")] == 0:
                        for i, item in enumerate(self.local_peers):
                            if data[str.encode("username")].decode('UTF-8') == item.username_:
                                del self.local_peers[i]
                                del self.local_peers_timeouts[i]
                    else:
                        record = Peer_Record(data[str.encode("username")], data[str.encode("ipv4")], data[str.encode("port")], bytes_=True)
                        existing = False
                        for i, item in enumerate(self.local_peers):
                            if item.username_ == record.username_ and item.ipv4_ == record.ipv4_ and item.port_ == record.port_:
                                self.local_peers_timeouts[i] = timer()
                                existing = True
                        if not existing:
                            self.local_peers.append(record)
                            self.local_peers_timeouts.append(timer())


                elif type_ == "getlist":
                    is_authorized = False
                    for i, item in enumerate(self.local_peers):
                        if item.ipv4_ == addr[0] and item.port_ == addr[1]:
                            is_authorized = True
                            self.acknowlidge(addr[0], addr[1], data[str.encode("txid")])

                    if not is_authorized:
                        msg = Message_Error('error', data[str.encode("txid")], "You aren't logged to this node, you don't have a permission to get LIST.")
                        encoded = msg.encoded_msg()
                        self.send_message_to(msg_b, addr[0], addr[1])
                        err_print("Not logged peer asked for LIST message.")
                    else:
                        records = Peer_Records()
                        for i, item in enumerate(self.local_peers):
                            records.add_record(item)

                        for i, item in enumerate(self.nodes.keys()):
                            if self.nodes[item] != -1:
                                for i, item in enumerate(self.nodes[item].records):
                                    records.add_record(item)

                        msg = Message_List('list', self.txid, records)
                        msg_b = msg.encoded_msg()
                        self.acks[self.txid] = [timer(), "list", addr[0], addr[1]]
                        self.send_message_to(msg_b, addr[0], addr[1])


                elif type_ == "error":
                    err_print(data[str.encode("verbose")].decode('UTF-8'))


                elif type_ == "update":
                    if (addr[0]+','+str(addr[1])) in self.nodes.keys():
                        new = False
                    else:
                        new = True

                    for e, elem in enumerate(sorted(data[str.encode("db")].keys())):
                        #authoritative record
                        if elem.decode('UTF-8').split(",")[0] == addr[0] and int(elem.decode('UTF-8').split(",")[1]) == addr[1]:
                            p_records = Peer_Records()
                            for i in range(len(data[str.encode("db")][elem].keys())):

                                rec_l = Peer_Record(data[str.encode("db")][elem][str.encode(str(i))][str.encode("username")], data[str.encode("db")][elem][str.encode(str(i))][str.encode("ipv4")], data[str.encode("db")][elem][str.encode(str(i))][str.encode("port")], bytes_=True)
                                p_records.add_record(rec_l)

                            self.nodes[elem.decode('UTF-8')] = p_records
                            self.nodes_timeouts[elem.decode('UTF-8')] = timer()
                        #nonauthoritative record
                        else:
                            if elem.decode('UTF-8').split(",")[0] == self.reg_ipv4 and int(elem.decode('UTF-8').split(",")[1]) == self.reg_port:
                                pass
                            elif elem.decode('UTF-8') not in self.nodes:
                            
                                self.nodes[elem.decode('UTF-8')] = -1
                                self.nodes_timeouts[elem.decode('UTF-8')] = timer()

                    for i, item in enumerate(self.nodes.keys()):
                        if self.nodes[item] == -1 or (addr[0] == item.split(",")[0] and addr[1] == int(item.split(",")[1]) and new):
                            recs = Db_Records()

                            records = Peer_Records()
                            for e, elem in enumerate(self.local_peers):
                                records.add_record(elem)

                            rec_db = Db_Record(self.reg_ipv4, self.reg_port, records)
                            recs.records.append(rec_db)

                            for e, elem in enumerate(self.nodes.keys()):
                                if self.nodes[elem] != -1:
                                    rec_db = Db_Record(elem.split(",")[0], int(elem.split(",")[1]), self.nodes[elem])
                                    recs.records.append(rec_db)

                            msg = Message_Update('update', self.txid, recs)
                            msg_b = msg.encoded_msg()
                            self.send_message_to(msg_b, item.split(",")[0], int(item.split(",")[1]))
                            self.nodes_last_notification[item] = timer()


                elif type_ == "disconnect":
                    if addr[0]+','+str(addr[1]) in self.nodes:
                        del self.nodes[addr[0]+','+str(addr[1])]
                        del self.nodes_timeouts[addr[0]+','+str(addr[1])]
                        del self.nodes_last_notification[addr[0]+','+str(addr[1])]
                    
                    self.acknowlidge(addr[0], addr[1], data[str.encode("txid")])


                elif type_ == "ack":
                    if data[str.encode("txid")] in self.acks:
                        del self.acks[data[str.encode("txid")]]
                    else:
                        err_print("Unexpected ACK with txid {} received." .format(data[str.encode("txid")]))


                else:
                    #ignore other messages
                    pass
            except Exception as e:
                exc_type, exc_obj, exc_tb = sys.exc_info()
                fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                err_print(exc_type, fname, exc_tb.tb_lineno)


    def listen_pipe(self):
        """
        method for handeling of named pipe listening
        """
        while True:
            try:
                with open(self.pipe) as p:
                    data = p.read()
                data = data.split()
                if self.debug:
                    err_print(data)


                if data[0] == "database":
                    counter = 0
                    string = "{"
                    for i, item in enumerate(self.local_peers):
                        string += str(item) + ','
                        counter += 1

                    for i, item in enumerate(self.nodes.keys()):
                        if self.nodes[item] != -1:
                            for e, elem in enumerate(self.nodes[item].records):
                                string += str(elem) + ','
                                counter += 1

                    if counter != 0:
                        string = string[:-1]

                    string += "}"

                    err_print(string)


                elif data[0] == "neighbors":
                    string = "{"
                    for i, item in enumerate(self.nodes.keys()):
                        string += "{\'ipv4\': \'" + item.split(',')[0] + "\', \'port\': " + str(int(item.split(',')[1])) + "}"
                        string += ','

                    if len(self.nodes) != 0:
                        string = string[:-1]

                    string += "}"

                    err_print(string)


                elif data[0] == "connect":
                    recs = Db_Records()

                    records = Peer_Records()
                    for i, item in enumerate(self.local_peers):
                        records.add_record(item)

                    rec_db = Db_Record(self.reg_ipv4, self.reg_port, records)
                    recs.records.append(rec_db)

                    for i, item in enumerate(self.nodes.keys()):
                        if self.nodes[item] != -1:
                            rec_db = Db_Record(item.split(",")[0], int(item.split(",")[1]), self.nodes[item])
                            recs.records.append(rec_db)

                    msg = Message_Update('update', self.txid, recs)
                    msg_b = msg.encoded_msg()
                    self.send_message_to(msg_b, data[1], int(data[2]))
                    self.nodes_last_notification[data[1]+','+str(data[2])] = timer()


                elif data[0] == "disconnect":
                    for i, item in enumerate(list(self.nodes.keys())):
                        msg = Message_Disconnect('disconnect', self.txid)
                        msg_b = msg.encoded_msg()
                        self.acks[self.txid] = [timer(), "disconnect", item.split(",")[0], int(item.split(",")[1])]
                        self.send_message_to(msg_b, item.split(",")[0], int(item.split(",")[1]))
                    self.nodes = {}
                    self.nodes_timeouts = {}
                    self.nodes_last_notification = {}


                elif data[0] == "sync":
                    recs = Db_Records()

                    records = Peer_Records()
                    for i, item in enumerate(self.local_peers):
                        records.add_record(item)

                    rec_db = Db_Record(self.reg_ipv4, self.reg_port, records)
                    recs.records.append(rec_db)

                    for i, item in enumerate(self.nodes.keys()):
                        if self.nodes[item] != -1:
                            rec_db = Db_Record(item.split(",")[0], int(item.split(",")[1]), self.nodes[item])
                            recs.records.append(rec_db)

                    for i, item in enumerate(self.nodes.keys()):
                        msg = Message_Update('update', self.txid, recs)
                        msg_b = msg.encoded_msg()
                        self.send_message_to(msg_b, item.split(",")[0], int(item.split(",")[1]))
                        self.nodes_last_notification[item] = timer()

                else:
                    #ignore other pipe messages
                    pass
            except Exception as e:
                if type(e).__name__ != 'FileNotFoundError': #pipe is not created
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
                    err_print(exc_type, fname, exc_tb.tb_lineno)


    def acknowlidge(self, ipv4, port, txid):
        """
        method sends ACK message to someone
        """
        msg = Message_Ack('ack', txid)
        msg_b = msg.encoded_msg()
        self.reg_sock.sendto(msg_b, (ipv4, port))


    def next_txid(self):
        """
        iterator method for txid indexing
        """
        if self.txid == 65535:
            self.txid = 0
        else:
            self.txid += 1


    def send_message_to(self, msg_b, ipv4, port):
        """
        method sends message to someone
        """
        self.reg_sock.sendto(msg_b, (ipv4, port))
        self.next_txid()


if __name__ == "__main__":
    args = get_args()
    node = Node(args)
    node.run()
