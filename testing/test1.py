# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 11:50:50 2019

@author: Admin
"""

import binascii
import codecs
from complete import*
import hashlib


def flip_byte_order(string):
	flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
	return codecs.encode(flipped,"utf-8")

def double_sha256(b):
    first_round = hashlib.sha256(b).digest()
    second_round = hashlib.sha256(first_round).digest()
    return second_round


version=2
TxIn = '9c4f789a3e7ba2446ffd64f7a645a8f1e45fa5c7a3b57b65edd38562c54c61cf'

index = 1
scriptsig = b"H0E\x02!\x00\xfe\xc2[\xd7'\xe3[^>B\x8csj;\xd2\x8f\xf3\x7f\xdb\x1al\xd34\xd2\x0bt\xc2Z\xa7pm9\x02 )\xc9,t\x8f\xb6\x0e\x85NB\xfe1\xfc\x1e\xd8\t\xb9\xf0\x98\x98\x03_\x19\x8e\xb5\xffD3\xf2;\\\x07\x01!\x02)qy!\x89\xeb+v\xb61XQ\x9aywb\xcdb/xRT\x9f\t\xa9\xca.W\x9bK\xa8\xae" 

sequence = 4294967295
 
amount= 8558538810
pk_script = b'v\xa9\x14\xf0\xd9\x9f\xb6.\x97\x1a^+\xa3\xdeB\x95\xa5\x95\xf5u\xf6\xd9G\x88\xac'
amount2 = 30399000
pk_script2 =b'v\xa9\x14\xa5\x12\x82\xb0\xe9\x1fAP\xde\x91\xc43\x16\xba\n\x15X\x93\xe1\xb4\x88\xac'
amount3 = 300000000
pk_script3 = b'v\xa9\x14\xe6\x80S*Bh$i\xe0\x9b\x03\x1a(\\&\x939p#|\x88\xac'
nlocktime= 0

#https://btc.com/54e37639bfca256a1afd3fb884c0eb67b9f0f1031fad32d2cdf87e2471bd391b#in_0

raw = b''
raw+= binascii.hexlify(int_to_bytes(version,4))
raw+= binascii.hexlify(int_to_bytes(1,1))
raw+= flip_byte_order(TxIn)
raw+= binascii.hexlify(int_to_bytes(1,4))
raw+= codecs.encode('{0:x}'.format(len(scriptsig)),"utf-8")
raw+= binascii.hexlify(scriptsig)
raw+= codecs.encode('{0:x}'.format(sequence),"utf-8")
raw+= binascii.hexlify(int_to_bytes(3,1))
raw+= binascii.hexlify(int_to_bytes(amount,8))
raw+= codecs.encode('{0:x}'.format(len(pk_script)),"utf-8")
raw+= binascii.hexlify(pk_script)
raw+= binascii.hexlify(int_to_bytes(amount2,8))
raw+= codecs.encode('{0:x}'.format(len(pk_script2)),"utf-8")
raw+= binascii.hexlify(pk_script2)
raw+= binascii.hexlify(int_to_bytes(amount3,8))
raw+= codecs.encode('{0:x}'.format(len(pk_script3)),"utf-8")
raw+= binascii.hexlify(pk_script3)
raw+= binascii.hexlify(int_to_bytes(nlocktime,4))




print(raw)


"""
actual raw:
    
02000000
01
cf614cc56285d3ed657bb5a3c7a55fe4f1a845a6f764fd6f44a2
7b3e9a784f9c
01000000
6b
483045022100fec25bd727e35b5e3e428c736a3bd28
ff37fdb1a6cd334d20b74c25aa7706d39022029c92c748fb60e854e42fe31fc1e
d809b9f09898035f198eb5ff4433f23b5c070121022971792189eb2b76b631585
19a797762cd622f7852549f09a9ca2e579b4ba8ae

ffffffff

03

3af020fe01000000
19
76a914f0d99fb62e971a5e2ba3de4295a595f575f6d94788ac

18dacf0100000000
19
76a914a51282b0e91f4150de91c43316ba0a155893e1b488ac

00a3e11100000000
19
76a914e680532a42682469e09b031a285c26933970237c88ac
00000000

actual hash : 54e37639bfca256a1afd3fb884c0eb67b9f0f1031fad32d2cdf87e2471bd391b"""
print(codecs.encode(double_sha256(binascii.unhexlify(raw))[::-1], "hex_codec"))
#print(double_sha256(codecs.decode(raw, "hex")))
#print(codecs.encode(double_sha256(codecs.encode(raw,"hex")))[::-1],"hex")

#print(hashlib.sha256(b"iusgad").digest())