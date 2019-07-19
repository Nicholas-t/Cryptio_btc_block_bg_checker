# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 10:57:21 2019

@author: Admin
"""

from complete import *
from handshake import handshake
from blockchain import blockexplorer as blk
import binascii
import codecs


VERSION = 70015

def double_sha256(b):
    first_round = hashlib.sha256(b).digest()
    second_round = hashlib.sha256(first_round).digest()
    return second_round

def flip_byte_order(string):
	flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
	return codecs.encode(flipped,"utf-8")


class GetHeadersMessage:

    command = b"getheaders"

    def __init__(self, locator, hashstop=0):
        self.locator = locator
        self.hashstop = hashstop

    def to_bytes(self):
        msg = self.locator.to_bytes()
        msg += int_to_bytes(self.hashstop, 32)
        return msg
    
class BlockLocator:
    def __init__(self, hashes, version):
        self.hashes = hashes
        self.version = version

    def to_bytes(self):
        msg = int_to_bytes(self.version, 4)
        msg += int_to_var_int(len(self.hashes))
        for hash_ in self.hashes:
            msg += int_to_bytes(hash_, 32)
        return msg
    


def construct_block_locator(all_hashes):
    locator_hashes = []
    height = len(all_hashes) - 1
    step = 1

    while height >= 0:
        # every iteration adds header at `height` and decrements `step`
        header = all_hashes[height]
        locator_hashes.append(header)
        height -= step
        
        # `step` starts doubling after the 11th hash
        if len(locator_hashes) > 10:
            step *= 2
    
    # make sure we have the genesis hash
    if not locator_hashes.index(block):
        locator_hashes.append(block)

    return BlockLocator(hashes=locator_hashes, version=VERSION)

def send_getheaders(sock):
    locator = construct_block_locator(header_hashes)
    getheaders = GetHeadersMessage(locator)
    packet = Packet(getheaders.command, getheaders.to_bytes())
    sock.send(packet.to_bytes())
    
class HeadersMessage:

    command = b"headers"

    def __init__(self, count, headers):
        self.count = count
        self.headers = headers

    @classmethod
    def from_bytes(cls, b):
        s = io.BytesIO(b)
        count = read_var_int(s)
        headers = []
        for _ in range(count):
            header = BlockHeader.from_stream(s)
            headers.append(header)
        return cls(count, headers)

    def __repr__(self):
        return f"<HeadersMessage #{len(self.headers)}>"
    




    
class BlockHeader:
    def __init__(
        self, version, prev_block, merkle_root, timestamp, bits, nonce, txn_count
    ):
        self.version = version
        self.prev_block = prev_block
        self.merkle_root = merkle_root
        self.timestamp = timestamp
        self.bits = bits
        self.nonce = nonce
        self.txn_count = txn_count

    @classmethod
    def from_stream(cls, s):
        version = read_int(s, 4)
        prev_block = read_int(s, 32)
        merkle_root = read_int(s, 32)
        timestamp = read_int(s, 4)
        bits = s.read(4)
        nonce = s.read(4)
        txn_count = read_var_int(s)
        return cls(version, prev_block, merkle_root, timestamp, bits, nonce, txn_count)

    def to_bytes(self):
        result = int_to_bytes(self.version, 4)
        result += int_to_bytes(self.prev_block, 32)
        result += int_to_bytes(self.merkle_root, 32)
        result += int_to_bytes(self.timestamp, 4)
        result += self.bits
        result += self.nonce
        return result

    def hash(self):
        s = self.to_bytes()
        sha = double_sha256(s)
        return sha[::-1]  # little endian

    def pow(self):
        s = self.to_bytes()
        sha = double_sha256(s)
        return bytes_to_int(sha)

    def target(self):
        # last byte is exponent
        exponent = self.bits[-1]
        # the first three bytes are the coefficient in little endian
        coefficient = bytes_to_int(self.bits[:-1])
        # the formula is:
        # coefficient * 2**(8*(exponent-3))
        return coefficient * 2 ** (8 * (exponent - 3))

    def check_pow(self):
        return self.pow() < self.target()

    def pretty(self):
        hx = hex(self.pow())[2:]  # remove "0x" prefix
        sigfigs = len(hx)
        padding = "0" * (64 - sigfigs)
        return padding + hx

    def __str__(self):
        headers = ["BlockHeader", ""]
        attrs = [
            "version",
            "prev_block",
            "merkle_root",
            "timestamp",
            "bits",
            "nonce",
            "txn_count",
        ]
        rows = [[attr, fmt(getattr(self, attr))] for attr in attrs]
        rows = [["hash", self.pretty()]] + rows
#         import pdb; pdb.set_trace()
        return tabulate(rows, headers, tablefmt="grid")
    
    
def save_header_hashes(block_headers):
    for header in block_headers:
        # we add it to the header_hashes if prev_block is our current tip
        if header.prev_block == header_hashes[-1]:
            header_hashes.append(header.pow())
        else:
            raise RuntimeError("received out-of-order block")
            



class Block(BlockHeader):
    def __init__(
        self, version, prev_block, merkle_root, timestamp, bits, nonce, txn_count, txns
    ):
        super().__init__(
            version, prev_block, merkle_root, timestamp, bits, nonce, txn_count
        )
        self.txns = txns

    @classmethod
    def from_stream(cls, s):
        version = read_int(s, 4)
        prev_block = read_int(s, 32)
        merkle_root = read_int(s, 32)
        timestamp = read_int(s, 4)
        bits = s.read(4)
        nonce = s.read(4)
        txn_count = read_var_int(s)
        txns = [Tx.from_stream(s) for _ in range(txn_count)]
        return cls(
            version, prev_block, merkle_root, timestamp, bits, nonce, txn_count, txns
        )

    def __repr__(self):
        return f"<Block {self.pretty()} >"
    
class InventoryItem:
    def __init__(self, type_, hash_):
        self.type = type_
        self.hash = hash_

    @classmethod
    def from_stream(cls, s):
        type_ = bytes_to_int(s.read(4))
        hash_ = s.read(32)
        return cls(type_, hash_)

    def to_bytes(self):
        msg = b""
        msg += int_to_bytes(self.type, 4)
        msg += self.hash
        return msg

    def __repr__(self):
        return f"<InvItem {inv_map[self.type]} {self.hash}>"


class GetData:
    command = b"getdata"

    def __init__(self, items=None):
        if items is None:
            self.items = []
        else:
            self.items = items

    def to_bytes(self):
        msg = int_to_var_int(len(self.items))
        for item in self.items:
            msg += item.to_bytes()
        return msg

    def __repr__(self):
        return f"<Getdata {repr(self.inv)}>"
    
def request_blocks(sock):
    items = [InventoryItem(2, int_to_bytes(hash_, 32)) 
             for hash_ in header_hashes]
    getdata = GetData(items=items)
    packet = Packet(getdata.command, getdata.to_bytes())
    sock.send(packet.to_bytes())
    
def handle_headers_packet(packet, sock):
    headers_message = HeadersMessage.from_bytes(packet.payload)
    block_headers = headers_message.headers
    print(f"{len(block_headers)} new headers")
    save_header_hashes(block_headers)
    print(f"We now have {len(header_hashes)} headers")
    request_blocks(sock)
    
def handle_block_packet(packet, sock):
    block = Block.from_stream(io.BytesIO(packet.payload))
    for txn in block.txns[:30]:
        print(txn)
    
def handle_packet(packet, sock):
    command_to_handler = {
        b"headers": handle_headers_packet,
        b"block": handle_block_packet,
    }
    handler = command_to_handler.get(packet.command)
    if handler:
        print(f'handling "{packet.command}"')
        handler(packet, sock)
    else:
        print(f'discarding "{packet.command}"')

class Tx:
    def __init__(self, version, tx_ins, tx_outs, locktime, segwit_flag = -1 , witness = -1, testnet=False):
        self.version = version
        self.tx_ins = tx_ins
        self.tx_outs = tx_outs
        self.locktime = locktime
		self.segwit_flag = segwit_flag #i added this
		self.witness = witness
        self.testnet = testnet

        
    def get_raw(self):
        raw = b''
        raw+= binascii.hexlify(int_to_bytes(self.version,4))
		if self.segwit_flag -= -1:
			raw += binascii.hexlify(int_to_bytes(self.segwit_flag,2))
        raw+= binascii.hexlify(int_to_bytes(len(self.tx_ins),4))
        for t in self.tx_ins:
            raw+= t.get_raw()
        raw+= binascii.hexlify(int_to_bytes(len(self.tx_outs),4))
        for t in self.tx_outs:
            raw+= t.get_raw()
		if self.witness != -1:
			raw+= binascii.hexlify(int_to_bytes(len(self.witness),4))
			for w in self.witness:
				raw+= w.get_raw()
        raw+= binascii.hexlify(int_to_bytes(self.locktime,4))
        return raw
    
    def get_hash(self):
        try:
            return codecs.encode(double_sha256(binascii.unhexlify(self.get_raw()))[::-1], "hex_codec")
        except:
            return "Failed to calculate hash"
    @classmethod
    def from_stream(cls, s):
        """Takes a byte stream and from_streams the transaction at the start
        return a Tx object
        """
        # s.read(n) will return n bytes
        # version has 4 bytes, little-endian, interpret as int
        version = bytes_to_int(s.read(4))
        # num_inputs is a varint, use read_var_int(s)
		seg = s.read(1)
		if bytes_to_int(seg) == 0: #FIX ME
			seg += s.read(1)
			num_inputs = read_var_int(s)
		else:
			seg = -1
			num_inputs = seg
        # each input needs parsing
        inputs = []
        for _ in range(num_inputs):
            inputs.append(TxIn.from_stream(s))
        # num_outputs is a varint, use read_var_int(s)
        num_outputs = read_var_int(s)
        # each output needs parsing
        outputs = []
        for _ in range(num_outputs):
            outputs.append(TxOut.from_stream(s))
		if seg != -1:
			wit = []
			num_wit = read_var_int(s)
			for _ in range (num_wit):
				wit.append(Witness.from_stream(s))
			# locktime is 4 bytes, little-endian
			locktime = bytes_to_int(s.read(4))
			# return an instance of the class (cls(...))
			return cls(version, inputs, outputs, locktime, segwit_flag = seg , witness = wit)
		else:
			locktime = bytes_to_int(s.read(4))
			return cls(version, inputs, outputs, locktime)

    def __repr__(self):
        try :
            t = blk.get_tx(self.get_hash())
            print(t.address, " successfully found")
            exit()
        except:
            return "<Tx{} \n version: {}\n ntx_ins: {} \n tx_outs: {} \n nlocktime: {} \n>".format(
                    self.get_hash(),
                self.version,
                ",".join([repr(t) for t in self.tx_ins]),
                ",".join([repr(t) for t in self.tx_outs]),
                self.locktime )

class Witness: #class i made
    def __init__(self,  script):
        self.script= script  # TODO from_stream it

    def get_raw(self):#FIX ME
        raw = b''
        raw+= codecs.encode('{0:x}'.format(len(self.script)),"utf-8")
        raw+= binascii.hexlify(self.script)
        return raw
    
    def __repr__(self):
        return "<Witness {}>".format(self.script)

    @classmethod
    def from_stream(cls, s):
        """Takes a byte stream and from_streams the tx_output at the start
        return a TxOut object
        """
        script_length = read_var_int(s)
        script = s.read(script_length)
        # return an instance of the class (cls(...))
        return cls(script)


class TxIn:
    def __init__(self, prev_tx, prev_index, script_sig, sequence):
        self.prev_tx = prev_tx.hex()
        self.prev_index = prev_index
        self.script_sig = script_sig  # TODO from_stream it
        self.sequence = sequence
        
    def get_raw(self):
        raw= b''
        raw+= flip_byte_order(self.prev_tx)
        raw+= binascii.hexlify(int_to_bytes(self.prev_index,4))
        raw+= codecs.encode('{0:x}'.format(len(self.script_sig)),"utf-8")
        raw+= binascii.hexlify(self.script_sig)
        raw+= codecs.encode('{0:x}'.format(self.sequence),"utf-8")
        return raw


    def __repr__(self):
        return "<TxIn {}\n:index {} \nscriptsig {} \n sequence {}>\n".format(self.prev_tx, 
                      self.prev_index,
                      self.script_sig,
                      self.sequence)

    @classmethod
    def from_stream(cls, s):
        """Takes a byte stream and from_streams the tx_input at the start
        return a TxIn object
        """
        # s.read(n) will return n bytes
        # prev_tx is 32 bytes, little endian
        prev_tx = s.read(32)[::-1]
        # prev_index is 4 bytes, little endian, interpret as int
        prev_index = bytes_to_int(s.read(4))
        # script_sig is a variable field (length followed by the data)
        # get the length by using read_var_int(s)
        script_sig_length = read_var_int(s)
        script_sig = s.read(script_sig_length)
        # sequence is 4 bytes, little-endian, interpret as int
        sequence = bytes_to_int(s.read(4))
        # return an instance of the class (cls(...))
        return cls(prev_tx, prev_index, script_sig, sequence)


class TxOut:
    def __init__(self, amount, script_pubkey):
        self.amount = amount
        self.script_pubkey = script_pubkey  # TODO from_stream it

    def get_raw(self):
        raw = b''
        raw+= binascii.hexlify(int_to_bytes(self.amount,8))
        raw+= codecs.encode('{0:x}'.format(len(self.script_pubkey)),"utf-8")
        raw+= binascii.hexlify(self.script_pubkey)
        return raw
    
    def __repr__(self):
        return "<TxOut {}:{}>".format(self.amount, self.script_pubkey)

    @classmethod
    def from_stream(cls, s):
        """Takes a byte stream and from_streams the tx_output at the start
        return a TxOut object
        """
        # s.read(n) will return n bytes
        # amount is 8 bytes, little endian, interpret as int
        amount = bytes_to_int(s.read(8))
        # script_pubkey is a variable field (length followed by the data)
        # get the length by using read_var_int(s)
        script_pubkey_length = read_var_int(s)
        script_pubkey = s.read(script_pubkey_length)
        # return an instance of the class (cls(...))
        return cls(amount, script_pubkey)




        
def initial_block_download():
    address = ("37.187.107.95", 8333)
    sock = handshake(address, log=False)
    # comment this line out and we don't get any headers
    send_getheaders(sock)
    i = 0
    while True:
        i+=1
        packet = Packet.from_socket(sock)
        handle_packet(packet, sock)
    
    
block = int("000000000000000000161a4d8d05f96dda16d23262a3540c39c4365b38f1c1f8", 16) #bloc 550067
header_hashes = [block]

initial_block_download()
