class Message(object):
    def __init__(self, type_, txid_):
        self.type_ = type_
        self.txid_ = txid_


class Message_Hello(Message):
    def __init__(self, type_, txid_, username_, ipv4_, port_):
        super().__init__(type_, txid_)
        self.username_ = username_
        self.ipv4_ = ipv4_
        self.port_ = port_


class Message_GetList(Message):
    def __init__(self, type_, txid_):
        super().__init__(type_, txid_)


class Message_List(Message):
    def __init__(self, type_, txid_, peers_):
        super().__init__(type_, txid_)
        self.peers_ = peers_


class Peer_Record():
    def __init__(self, username_, ipv4_, port_):
        self.username_ = username_
        self.ipv4_ = ipv4_
        self.port_ = port_


class Message_Message(Message):
    def __init__(self, type_, from_, to_, message_):
        super().__init__(type_, txid_)
        self.type_ = type_
        self.from_ = from_
        self.to_ = to_
        self.message_ = message_


class Message_Update(Message):
    def __init__(self, type_, txid_, db_):
        super().__init__(type_, txid_)
        self.db_ = db_


class Db_Record():
    def __init__(self, dotted_decimal_IP_, ushort_port_):
        self.dotted_decimal_IP_ = dotted_decimal_IP_
        self.ushort_port_ = ushort_port_


class Message_Disconnect(Message):
    def __init__(self, type_, txid_):
        super().__init__(type_, txid_)


class Message_Ack(Message):
    def __init__(self, type_, txid_):
        super().__init__(type_, txid_)


class Message_Error(Message):
    def __init__(self, type_, txid_, verbose_):
        super().__init__(type_, txid_)
        self.verbose_ = verbose_
"""
HELLO := {"type":"hello", "txid":<ushort>, "username":"<string>", "ipv4":"<dotted_decimal_IP>", "port": <ushort>}                  
                  
GETLIST := {"type":"getlist", "txid":<ushort>}                  
                  
LIST := {"type":"list", "txid":<ushort>, "peers": {<PEER_RECORD*>}}                  
PEER_RECORD := {"<ushort>":{"username":"<string>", "ipv4":"<dotted_decimal_IP>", "port": <ushort>}}                  
                  
MESSAGE := {"type":"message", "txid":<ushort>, "from":"<string>", "to":"<string>", "message":"<string>"}                  
                  
UPDATE := {"type":"update", "txid":<ushort>, "db": {<DB_RECORD*>}}                  
DB_RECORD := {"<dotted_decimal_IP>,<ushort_port>":{<PEER_RECORD*>}}                  
                  
DISCONNECT := {"type":"disconnect", "txid":<ushort>}                  
                  
ACK := {"type":"ack", "txid":<ushort>}                  
                  
ERROR := {"type":"error", "txid":<ushort>, "verbose": "<string>"}
"""