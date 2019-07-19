# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:15:29 2019

@author: Admin
"""
from complete import *
from main import *

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