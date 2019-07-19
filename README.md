# Cryptio_btc_block_bg_checker
 
# Background:
With this project, we would like to code a program that tracks an **entity transaction real time data** given their unspent transaction hash 
(i.e. the hash of the last transactions they have). This can have a lot of possible applications, one of them is to be able to track *your own* transaction and see whether it is
already succesfully saved in the global ledger, you can also track peoples transaction if you know who the unspent transaction hash belongs to.
What is ambitious about this project is we would like to do this **without running our own node** and use as least as third party API as possible such as blockchain API, with that being 
said we will eventually use their API for one small part of the project which will be explained later. All communication in the bitcoin protocol uses TCP Protocol.

## Why not run our own node?

There is no doubt that running your own bitcoin node is beneficial if you are a bitcoin player, some might say it is recommended. Unfortunately running your own node comes with 
cost which mainly comes from having to keep the whole bitcoin blockchain stored in your device. And that way is also beneficial for us to learn about the bitcoin Peer2Peer protocol.

## Why not use the existing API for the whole project?

This project is meant to help Cryptio and as a startup that dreams big we will need to think of a scalable method, thus relying a lot on a third party API will put us on a restrictive
disadvantage in the long run.

Outline of steps that we will take:
- *Connecting to a remote node*
- *handshake*
- *get headers message*
- *get block message*
- *handle packets*

Special thanks to justin moon's [repo](https://github.com/justinmoon/bitcoincorps) for having a thorough step by step guide on communicating to a remote node. 
do check it out if you wanna go deeper than what we cover here!


## Dependencies:
	-binsacii
	-blockchain
	-python3 (not tested for python2)
	-other libraries that we use will should be in the python standard package library, if not:
		-hashlib
		-codecs
		-io
		-re
		-socket

# Connecting to a remote node (TO DO)

# Handshake

Best way to think of this _Handshake_ is like in real life it is *socially wise* to handshake someone before a professional meeting and tells them your name, company, etc. except with
the bitcoin network, your peer will not want to talk to you ever if you haven't done the handshake.
The purpose of this handshake ritual is to broadcast your identity to your connected peer.

![alt handshake]("https://github.com/Nicholas-t/Cryptio_btc_block_bg_checker/tree/master/images/handshake.png)

The _Handshake_ done by the following:

	- We send a Version message
	- We receive a Version message
	- We receive a Verack (VERsion ACKnowledgement) message
	- We send a Verack message 

#### ref
	version : <https://en.bitcoin.it/wiki/Protocol_documentation#version>
	verack : <https://en.bitcoin.it/wiki/Protocol_documentation#verack>
	
# Get Headers Message

Every block is represented in the blockchain(*in the node*) as a blockheaders. There is no use for a node to keep the data of all the transaction in each block unless it is in
their interest.

<img align="right" src="https://github.com/Nicholas-t/Cryptio_btc_block_bg_checker/tree/master/images/headers.PNG">

If we take a look at the format of a headers message from the bitcoin protocol, we can see that the actual block it self is crypted in the second part of the headers message,
this means we can get the details of the block, if we can decode it using binary parsing.

# Get Block Message

# Handle Packets

# Practical Tutorial

#Conclusion

Tracking an unspent transaction through only socket connection with a remote node