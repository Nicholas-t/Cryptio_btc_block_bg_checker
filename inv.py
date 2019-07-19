# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:15:28 2019

@author: Admin
"""

from complete import *
from main import *

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