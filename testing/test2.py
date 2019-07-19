# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 13:32:45 2019

@author: Admin
"""
import binascii
import codecs
from complete import*
import hashlib

def double_sha256(b):
    first_round = hashlib.sha256(b).digest()
    second_round = hashlib.sha256(first_round).digest()
    return second_round

def flip_byte_order(string):
	flipped = "".join(reversed([string[i:i+2] for i in range(0, len(string), 2)]))
	return codecs.encode(flipped,"utf-8")


version=2
TxIn = 'f76ace860fc71b84be5c6cc86ef3c12e004f9388dbd65239f34e6f247f707435'

index = 1
scriptsig = b'\x16\x00\x147\xc1\xaabx$\xf5\xa2/\xa4h\x1e6@\xa8(j(\x92\x0b'

sequence = 4294967294

amount= 114701706
pk_script = b'\xa9\x14QE\xde\xd7\xc0m\xbd\xd3\x88r\xd04\x017\xa4\x9b\xd5Ja\xd1\x87'
amount2 = 82355680
pk_script2 =b'\xa9\x14i\xf3t\x83\x87\xf0v\x94\x13\xaen#\xfc&\x99\x98Y\xd2\xfaJ\x87'
nlocktime = 550066

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
raw+= binascii.hexlify(int_to_bytes(nlocktime,4))

print(raw)

"predicted hash 'a523bf6e837ee4e1d637f2c8368a07fe1013dc574c4a2a27871d851e580fc9f3'"
#https://btc.com/79a15c90704a77e3aa2f204556b0450c3502b5bd02a9e567c0a34b08fb59102f#in_0
"""

actual raw:
02000000
00 #segwit This could be the reason why?
0101
3574707f246f4ef33952d6db88934f002ec1f36ec86c5cbe841bc70f86ce6af701
0000001716001437c1aa627824f5a22fa4681e3640a8286a28920bfeffffff028a35d6060000000017a9
145145ded7c06dbdd38872d0340137a49bd54a61d187e0a5e8040000000017a91469f3748387f0769413
ae6e23fc26999859d2fa4a8702473044022050458003472ee22403843ea8b13f797a5663c69c08f53389b
6f929dbac26496a0220276e96ba2dde0cd82d788734886cc1ecd9973540daeddf7bd89a1f9eb01b
0cc3012102ee0c16e301c8cc0974315ef8796597b5932fece144da136b93c5ba318ad0a7e5b2640800


actual hash 79a15c90704a77e3aa2f204556b0450c3502b5bd02a9e567c0a34b08fb59102f

https://btc.com/79a15c90704a77e3aa2f204556b0450c3502b5bd02a9e567c0a34b08fb59102f#in_0

"""

print(codecs.encode(double_sha256(binascii.unhexlify(raw))[::-1], "hex_codec"))

"""02000000
0001 #segwit This could be the reason why?

01

3574707f246f4ef33952d6db88934f002ec1
f36ec86c5cbe841bc70f86ce6af7010000001716001437c1
aa627824f5a22fa4681e3640a8286a28920bfeffffff028a
35d6060000000017a9145145ded7c06dbdd38872d0340137
a49bd54a61d187e0a5e8040000000017a91469f3748387f
0769413ae6e23fc26999859d2fa4a87

02473044022050458003472ee22403843ea8b13f797a5663c69c08f53389b
6f929dbac26496a0220276e96ba2dde0cd82d788734886cc1ecd9973540daeddf7bd89a1f9eb01b
0cc3012102ee0c16e301c8cc0974315ef8796597b5932fece144da136b93c5ba318ad0a7e5b2640800"""

"""0200000001

3574707f246f4ef33952d6db88934f002ec1
f36ec86c5cbe841bc70f86ce6af7010000001716001437c1
aa627824f5a22fa4681e3640a8286a28920bfffffffe038a
35d6060000000017a9145145ded7c06dbdd38872d0340137
a49bd54a61d187e0a5e8040000000017a91469f3748387f
0769413ae6e23fc26999859d2fa4a87

b2640800"""
