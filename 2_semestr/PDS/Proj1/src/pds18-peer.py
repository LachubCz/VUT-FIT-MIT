import os
import sys
import time
import _thread
import socket
import argparse


from messages import Message_Hello, Message_GetList, Message_List, Message_Message, Message_Update, Message_Disconnect, Message_Ack, Message_Error
from messages import Peer_Record, Peer_Records, Db_Record, Db_Records
from tools import err_print

def get_args():
    """
    method for parsing of arguments
    """
    parser = argparse.ArgumentParser()

    parser.add_argument('--id', action="store", type=int, required=True,
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
        self.args = args
        try:
            self.chat_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.chat_sock.bind((args.chat_ipv4, args.chat_port))
        except:
            err_print("Cannot assign requested chat address or port.")
            sys.exit(-1)

        try:
            self.reg_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            self.reg_sock.bind((args.reg_ipv4, args.reg_port))
        except:
            err_print("Cannot assign requested reg address or port.")
            sys.exit(-1)

    def run(self):
        
        _thread.start_new_thread(self.listen_chat, (self.chat_sock, ))
        _thread.start_new_thread(self.listen_reg,  (self.reg_sock, ))
        _thread.start_new_thread(self.listen_pipe, ("/tmp/hourly", ))

        while True:
            pass

    def listen_chat(self, chat_sock):
        while True:
            data, addr = chat_sock.recvfrom(1024)


    def listen_reg(self, reg_sock):
        while True:
            data, addr = reg_sock.recvfrom(1024)


    def listen_pipe(self, FIFO):
        while True:
            with open(FIFO) as fifo:
                print("heher")

if __name__ == "__main__":
    args = get_args()
    peer = Peer(args)
    peer.run()










    #msg = Message_Hello('hello', 123, 'xlogin00', '127.0.0.1', 5005)
    #UDP_IP = msg.ipv4_
    #UDP_PORT = msg.port_
    #MESSAGE = msg.encoded_msg()

    #print ("UDP target IP:", UDP_IP)
    #print ("UDP target port:", UDP_PORT)
    #print ("message:", MESSAGE)

    #sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
