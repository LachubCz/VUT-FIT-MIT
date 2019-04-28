#!/usr/bin/env python3
#################################################################################
# Description:  File tests for messages classes
#               
# Author:      Petr Buchal         <petr.buchal@lachub.cz>
#
# Date:     2019/04/28
# 
# Note:     This source code is part of PDS project 2019.
#################################################################################

import unittest

from messages import Message_Hello, Message_GetList, Message_List, Message_Message, Message_Update, Message_Disconnect, Message_Ack, Message_Error
from messages import Peer_Record, Peer_Records, Db_Record, Db_Records
from bencode import encode, decode

class TestAppRuns(unittest.TestCase):
    def test_01_Message_Hello_decode_01(self):
        decoded = decode("d4:ipv49:192.0.2.14:porti34567e4:txidi123e4:type5:hello8:username8:xlogin00e")
        msg = Message_Hello(decoded[str.encode("type")], decoded[str.encode("txid")], decoded[str.encode("username")], decoded[str.encode("ipv4")], decoded[str.encode("port")], bytes_=True)
        self.assertEqual(msg.type_, 'hello')
        self.assertEqual(msg.txid_, 123)
        self.assertEqual(msg.username_, 'xlogin00')
        self.assertEqual(msg.ipv4_, '192.0.2.1')
        self.assertEqual(msg.port_, 34567)

    def test_02_Message_Hello_decode_02(self):
        decoded = decode("d4:ipv47:0.0.0.04:porti0e4:txidi123e4:type5:hello8:username8:xlogin00e")
        msg = Message_Hello(decoded[str.encode("type")], decoded[str.encode("txid")], decoded[str.encode("username")], decoded[str.encode("ipv4")], decoded[str.encode("port")], bytes_=True)
        self.assertEqual(msg.type_, 'hello')
        self.assertEqual(msg.txid_, 123)
        self.assertEqual(msg.username_, 'xlogin00')
        self.assertEqual(msg.ipv4_, '0.0.0.0')
        self.assertEqual(msg.port_, 0)

    def test_03_Message_Hello_encode_01(self):
        msg = Message_Hello('hello', 123, 'xlogin00', '192.0.2.1', 34567)
        encoded = msg.encoded_msg()
        self.assertEqual(str.encode("d4:ipv49:192.0.2.14:porti34567e4:txidi123e4:type5:hello8:username8:xlogin00e"), encoded)

    def test_04_Message_Hello_encode_02(self):
        msg = Message_Hello('hello', 123, 'xlogin00', '0.0.0.0', 0)
        encoded = msg.encoded_msg()
        self.assertEqual(str.encode("d4:ipv47:0.0.0.04:porti0e4:txidi123e4:type5:hello8:username8:xlogin00e"), encoded)

    def test_05_Message_GetList_decode_01(self):
        decoded = decode("d4:txidi123e4:type7:getliste")
        msg = Message_GetList(decoded[str.encode("type")], decoded[str.encode("txid")], bytes_=True)
        self.assertEqual(msg.type_, 'getlist')
        self.assertEqual(msg.txid_, 123)

    def test_06_Message_GetList_encode_01(self):
        msg = Message_GetList('getlist', 123)
        encoded = msg.encoded_msg()
        self.assertEqual(str.encode("d4:txidi123e4:type7:getliste"), encoded)

    def test_07_Message_Error_decode_01(self):
        decoded = decode("d4:txidi123e4:type5:error7:verbose66:I refuse to send list of peers, requestor is not registered to me!e")
        msg = Message_Error(decoded[str.encode("type")], decoded[str.encode("txid")], decoded[str.encode("verbose")], bytes_=True)
        self.assertEqual(msg.type_, 'error')
        self.assertEqual(msg.txid_, 123)
        self.assertEqual(msg.verbose_, "I refuse to send list of peers, requestor is not registered to me!")

    def test_08_Message_Error_encode_01(self):
        msg = Message_Error('error', 123, "I refuse to send list of peers, requestor is not registered to me!")
        encoded = msg.encoded_msg()
        self.assertEqual(str.encode("d4:txidi123e4:type5:error7:verbose66:I refuse to send list of peers, requestor is not registered to me!e"), encoded)

    def test_09_Message_List_decode_01(self):
        decoded = decode("d5:peersd1:0d4:ipv49:192.0.2.14:porti34567e8:username8:xlogin00e1:1d4:ipv49:192.0.2.24:porti45678e8:username8:xnigol99ee4:txidi123e4:type4:liste")
        records = Peer_Records()
        for i in range(len(decoded[str.encode("peers")].keys())):
            rec = Peer_Record(decoded[str.encode("peers")][str.encode(str(i))][str.encode("username")], decoded[str.encode("peers")][str.encode(str(i))][str.encode("ipv4")], decoded[str.encode("peers")][str.encode(str(i))][str.encode("port")], bytes_=True)
            records.add_record(rec)

        msg = Message_List(decoded[str.encode("type")], decoded[str.encode("txid")], records, bytes_=True)

        self.assertEqual(msg.type_, 'list')
        self.assertEqual(msg.txid_, 123)
        self.assertEqual(msg.peers_.records[0].username_, 'xlogin00')
        self.assertEqual(msg.peers_.records[0].ipv4_, '192.0.2.1')
        self.assertEqual(msg.peers_.records[0].port_, 34567)
        self.assertEqual(msg.peers_.records[1].username_, 'xnigol99')
        self.assertEqual(msg.peers_.records[1].ipv4_, '192.0.2.2')
        self.assertEqual(msg.peers_.records[1].port_, 45678)

    def test_10_Message_List_encode_01(self):
        records = Peer_Records()
        rec_01 = Peer_Record("xlogin00", "192.0.2.1", 34567)
        records.add_record(rec_01)
        rec_02 = Peer_Record("xnigol99", "192.0.2.2", 45678)
        records.add_record(rec_02)

        msg = Message_List('list', 123, records)
        encoded = msg.encoded_msg()
        self.assertEqual(str.encode("d5:peersd1:0d4:ipv49:192.0.2.14:porti34567e8:username8:xlogin00e1:1d4:ipv49:192.0.2.24:porti45678e8:username8:xnigol99ee4:txidi123e4:type4:liste"), encoded)

    def test_11_Message_Message_decode_01(self):
        decoded = decode("d4:from8:xlogin007:message9:blablabla2:to8:xnigol994:txidi123e4:type7:messagee")
        msg = Message_Message(decoded[str.encode("type")], decoded[str.encode("txid")], decoded[str.encode("from")], decoded[str.encode("to")], decoded[str.encode("message")], bytes_=True)
        self.assertEqual(msg.type_, 'message')
        self.assertEqual(msg.txid_, 123)
        self.assertEqual(msg.from_, 'xlogin00')
        self.assertEqual(msg.to_, 'xnigol99')
        self.assertEqual(msg.message_, 'blablabla')

    def test_12_Message_Message_encode_01(self):
        msg = Message_Message('message', 123, 'xlogin00', 'xnigol99', 'blablabla')
        encoded = msg.encoded_msg()
        self.assertEqual(str.encode("d4:from8:xlogin007:message9:blablabla2:to8:xnigol994:txidi123e4:type7:messagee"), encoded)

    def test_13_Message_Update_decode_01(self):
        decoded = decode("d2:dbd17:192.0.2.198,12345d1:0d4:ipv49:192.0.2.14:porti34567e8:username8:xlogin00e1:1d4:ipv49:192.0.2.24:porti45678e8:username8:xnigol99ee17:192.0.2.199,12345d1:0d4:ipv49:192.0.2.34:porti65432e8:username8:xtestx00eee4:txidi123e4:type6:updatee")
        db_records = Db_Records()

        for e, elem in enumerate(sorted(decoded[str.encode("db")].keys())):
            p_records = Peer_Records()
            for i in range(len(decoded[str.encode("db")][elem].keys())):
                rec_l = Peer_Record(decoded[str.encode("db")][elem][str.encode(str(i))][str.encode("username")], decoded[str.encode("db")][elem][str.encode(str(i))][str.encode("ipv4")], decoded[str.encode("db")][elem][str.encode(str(i))][str.encode("port")], bytes_=True)
                p_records.add_record(rec_l)

            rec_h = Db_Record(elem.decode('UTF-8').split(",")[0], int(elem.decode('UTF-8').split(",")[1]), p_records)
            db_records.add_record(rec_h)

        msg = Message_Update(decoded[str.encode("type")], decoded[str.encode("txid")], db_records, bytes_=True)
        self.assertEqual(msg.type_, 'update')
        self.assertEqual(msg.txid_, 123)
        self.assertEqual(msg.db_.records[0].dotted_decimal_IP_, '192.0.2.198')
        self.assertEqual(msg.db_.records[0].ushort_port_, 12345)
        self.assertEqual(msg.db_.records[0].peers_.records[0].username_, 'xlogin00')
        self.assertEqual(msg.db_.records[0].peers_.records[0].ipv4_, '192.0.2.1')
        self.assertEqual(msg.db_.records[0].peers_.records[0].port_, 34567)
        self.assertEqual(msg.db_.records[0].peers_.records[1].username_, 'xnigol99')
        self.assertEqual(msg.db_.records[0].peers_.records[1].ipv4_, '192.0.2.2')
        self.assertEqual(msg.db_.records[0].peers_.records[1].port_, 45678)
        self.assertEqual(msg.db_.records[1].dotted_decimal_IP_, '192.0.2.199')
        self.assertEqual(msg.db_.records[1].ushort_port_, 12345)
        self.assertEqual(msg.db_.records[1].peers_.records[0].username_, 'xtestx00')
        self.assertEqual(msg.db_.records[1].peers_.records[0].ipv4_, '192.0.2.3')
        self.assertEqual(msg.db_.records[1].peers_.records[0].port_, 65432)
    
    def test_14_Message_Update_encode_01(self):
        recs = Db_Records()
        
        records = Peer_Records()
        rec_01 = Peer_Record("xlogin00", "192.0.2.1", 34567)
        records.add_record(rec_01)
        rec_02 = Peer_Record("xnigol99", "192.0.2.2", 45678)
        records.add_record(rec_02)
        rec_db_01 = Db_Record("192.0.2.198", 12345, records)
        recs.records.append(rec_db_01)
        
        records = Peer_Records()
        rec_01 = Peer_Record("xtestx00", "192.0.2.3", 65432)
        records.add_record(rec_01)
        rec_db_02 = Db_Record("192.0.2.199", 12345, records)

        recs.records.append(rec_db_02)

        msg = Message_Update('update', 123, recs)
        encoded = msg.encoded_msg()
        self.assertEqual(str.encode("d2:dbd17:192.0.2.198,12345d1:0d4:ipv49:192.0.2.14:porti34567e8:username8:xlogin00e1:1d4:ipv49:192.0.2.24:porti45678e8:username8:xnigol99ee17:192.0.2.199,12345d1:0d4:ipv49:192.0.2.34:porti65432e8:username8:xtestx00eee4:txidi123e4:type6:updatee"), encoded)

    def test_15_Message_Disconnect_decode_01(self):
        decoded = decode("d4:txidi123e4:type10:disconnecte")
        msg = Message_Disconnect(decoded[str.encode("type")], decoded[str.encode("txid")], bytes_=True)
        self.assertEqual(msg.type_, 'disconnect')
        self.assertEqual(msg.txid_, 123)

    def test_16_Message_Disconnect_encode_01(self):
        msg = Message_Disconnect('disconnect', 123)
        encoded = msg.encoded_msg()
        self.assertEqual(str.encode("d4:txidi123e4:type10:disconnecte"), encoded)

    def test_17_Message_Ack_decode_01(self):
        decoded = decode("d4:txidi123e4:type3:acke")
        msg = Message_Ack(decoded[str.encode("type")], decoded[str.encode("txid")], bytes_=True)
        self.assertEqual(msg.type_, 'ack')
        self.assertEqual(msg.txid_, 123)

    def test_18_Message_Ack_encode_01(self):
        msg = Message_Ack('ack', 123)
        encoded = msg.encoded_msg()
        self.assertEqual(str.encode("d4:txidi123e4:type3:acke"), encoded)

if __name__ == "__main__":
    unittest.main()
