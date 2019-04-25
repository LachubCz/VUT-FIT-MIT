class Message(object):
    def __init__(self, type_, txid_, bytes_):
        if bytes_:
            self.type_ = type_.decode('UTF-8')
            self.txid_ = txid_
        else:
            self.type_ = type_
            self.txid_ = txid_

    def dictionary(self):
        dict_ = {
            str.encode("type") : self.type_,
            str.encode("txid") : self.txid_
        }

        return dict_

class Message_Hello(Message):
    def __init__(self, type_, txid_, username_, ipv4_, port_, bytes_=False):
        super().__init__(type_, txid_, bytes_)
        if bytes_:
            self.username_ = username_.decode('UTF-8')
            self.ipv4_ = ipv4_.decode('UTF-8')
            self.port_ = port_
        else:
            self.username_ = username_
            self.ipv4_ = ipv4_
            self.port_ = port_

    def dictionary(self):
        dict_ = {
            str.encode("type") : self.type_,
            str.encode("txid") : self.txid_,
            str.encode("username") : self.username_,
            str.encode("ipv4") : self.ipv4_,
            str.encode("port") : self.port_
        }

        return dict_

class Message_GetList(Message):
    def __init__(self, type_, txid_, bytes_=False):
        super().__init__(type_, txid_, bytes_)

class Message_List(Message):
    def __init__(self, type_, txid_, peers_, bytes_=False):
        super().__init__(type_, txid_, bytes_)
        self.peers_ = peers_

    def dictionary(self):
        dict_ = {
            str.encode("type") : self.type_,
            str.encode("txid") : self.txid_,
            str.encode("peers") : self.peers_.dictionary()
        }

        return dict_

class Peer_Records():
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def dictionary(self):
        dict_ = dict()
        for i, item in enumerate(self.records):
            temp_ = {
                str.encode("username") : item.username_,
                str.encode("ipv4") : item.ipv4_,
                str.encode("port") : item.port_
            }
            dict_[str.encode(str(i))] = temp_

        return dict_

class Peer_Record():
    def __init__(self, username_, ipv4_, port_, bytes_=False):
        if bytes_:
            self.username_ = username_.decode('UTF-8')
            self.ipv4_ = ipv4_.decode('UTF-8')
            self.port_ = port_
        else:
            self.username_ = username_
            self.ipv4_ = ipv4_
            self.port_ = port_

class Message_Message(Message):
    def __init__(self, type_, txid_, from_, to_, message_, bytes_=False):
        super().__init__(type_, txid_, bytes_)
        if bytes_:
            self.type_ = type_.decode('UTF-8')
            self.from_ = from_.decode('UTF-8')
            self.to_ = to_.decode('UTF-8')
            self.message_ = message_.decode('UTF-8')
        else:
            self.type_ = type_
            self.from_ = from_
            self.to_ = to_
            self.message_ = message_

    def dictionary(self):
        dict_ = {
            str.encode("type") : self.type_,
            str.encode("txid") : self.txid_,
            str.encode("from") : self.from_,
            str.encode("to") : self.to_,
            str.encode("message") : self.message_
        }

        return dict_

class Message_Update(Message):
    def __init__(self, type_, txid_, db_, bytes_=False):
        super().__init__(type_, txid_, bytes_)
        self.db_ = db_

    def dictionary(self):
        dict_ = {
            str.encode("type") : self.type_,
            str.encode("txid") : self.txid_,
            str.encode("db") : self.db_.dictionary()
        }

        return dict_

class Db_Records():
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def dictionary(self):
        dict_ = dict()
        for i, item in enumerate(self.records):
            temp_ = {
                str.encode("username") : item.peers_.dictionary(),
                str.encode("ipv4") : item.peers_.dictionary(),
                str.encode("port") : item.peers_.dictionary()
            }
            dict_[str.encode(item.dotted_decimal_IP_+','+str(item.ushort_port_))] = item.peers_.dictionary()

        return dict_

class Db_Record():
    def __init__(self, dotted_decimal_IP_, ushort_port_, peers_):
        self.dotted_decimal_IP_ = dotted_decimal_IP_
        self.ushort_port_ = ushort_port_
        self.peers_ = peers_

class Message_Disconnect(Message):
    def __init__(self, type_, txid_, bytes_=False):
        super().__init__(type_, txid_, bytes_)

class Message_Ack(Message):
    def __init__(self, type_, txid_, bytes_=False):
        super().__init__(type_, txid_, bytes_)

class Message_Error(Message):
    def __init__(self, type_, txid_, verbose_, bytes_=False):
        super().__init__(type_, txid_, bytes_)
        if bytes_:
            self.verbose_ = verbose_.decode('UTF-8')
        else:
            self.verbose_ = verbose_

    def dictionary(self):
        dict_ = {
            str.encode("type") : self.type_,
            str.encode("txid") : self.txid_,
            str.encode("verbose") : self.verbose_
        }

        return dict_
