# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:10:57 2019

@author: Admin
"""




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
    if not locator_hashes.index(genesis_hash):
        locator_hashes.append(genesis_hash)

    return BlockLocator(hashes=locator_hashes, version=VERSION)

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
    
def request_blocks(sock):
    items = [InventoryItem(2, int_to_bytes(hash_, 32)) 
             for hash_ in header_hashes]
    getdata = GetData(items=items)
    packet = Packet(getdata.command, getdata.to_bytes())
    sock.send(packet.to_bytes())
