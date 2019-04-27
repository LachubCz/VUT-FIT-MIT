import os
import sys
import time
import _thread
import socket
import argparse


from messages import Message_Hello, Message_GetList, Message_List, Message_Message, Message_Update, Message_Disconnect, Message_Ack, Message_Error
from messages import Peer_Record, Peer_Records, Db_Record, Db_Records
from tools import err_print

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
msg = Message_Hello('hello', 123, 'xlogin00', '192.168.2.102', 10001)
UDP_IP = msg.ipv4_
UDP_PORT = msg.port_
MESSAGE = msg.encoded_msg()

print ("UDP target IP:", UDP_IP)
print ("UDP target port:", UDP_PORT)
print ("message:", MESSAGE)

sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
