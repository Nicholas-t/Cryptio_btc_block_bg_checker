# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:10:56 2019

@author: Admin
"""



class GetHeadersMessage:

    command = b"getheaders"

    def __init__(self, locator, hashstop=0):
        self.locator = locator
        self.hashstop = hashstop

    def to_bytes(self):
        msg = self.locator.to_bytes()
        msg += int_to_bytes(self.hashstop, 32)
        return msg
    
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
    

    
def save_header_hashes(block_headers):
    for header in block_headers:
        # we add it to the header_hashes if prev_block is our current tip
        if header.prev_block == header_hashes[-1]:
            header_hashes.append(header.pow())
        else:
            raise RuntimeError("received out-of-order block")
            

