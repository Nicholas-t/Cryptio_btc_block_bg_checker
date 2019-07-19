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

<img align="right" width="100" height="100" src="https://github.com/Nicholas-t/Cryptio_btc_block_bg_checker/tree/master/images/handshake.png">

The _Handshake_ done by the following:

	- We send a Version message
	- We receive a Version message
	- We receive a Verack (VERsion ACKnowledgement) message
	- We send a Verack message 

#### ref :
version : <https://en.bitcoin.it/wiki/Protocol_documentation#version>

verack : <https://en.bitcoin.it/wiki/Protocol_documentation#verack>
	
# Get Headers Message

Every block is represented in the blockchain(*in the node*) as a blockheaders. There is no use for a node to keep the data of all the transaction in each block unless it is in
their interest.

If we take a look at the format of a response to a *get headers message* from the bitcoin protocol, we can see that the actual block it self is crypted in the second part of the headers message,
this means we can get the details of the block, if we can decode it using binary parsing.

#### ref :
getheaders : <https://en.bitcoin.it/wiki/Protocol_documentation#getheaders>

# Get Block Message

In this step we request the details of the *block message* from the *headers message* through our public node. The information that we are most interested in is the transactions that
are included in the block

#### ref :
getblocks : <https://en.bitcoin.it/wiki/Protocol_documentation#getblocks>

# Handle Packets

There are 2 main packets that we will be interested in. I specified only 2 because throughout the communication protocol we will also receive other packets such as *inv* packets, 
*getaddr* packets or a *ping* message which doesnt do us any good.

<img align="right" width="100" height="100" src="https://github.com/Nicholas-t/Cryptio_btc_block_bg_checker/tree/master/images/headers.PNG">

## Handling headers message:

Headers message is the response to a *getheaders* message that we sent, which should contain the information about the block headers we requested.

#### ref :
headers : <https://en.bitcoin.it/wiki/Protocol_documentation#headers>

block headers : <https://en.bitcoin.it/wiki/Protocol_documentation#Block_Headers>


<img align="right" width="100" height="100" src="https://github.com/Nicholas-t/Cryptio_btc_block_bg_checker/tree/master/images/blocks.PNG">

## Handling block message:

A block message is a response to a getblocks message and contains the information about the block. As we can see the information about the 
transactions is in the very last chunk of bytes.

The transaction object contained has a list of inputs and outputs, **now do not get confused!** contrary to our usual notion of inputsan d outputs being the addresses of 
the entity that take part in the transaction, 
that is not the case in the bitcoin protocol , instead input contains the **unspent transaction hash** that the user have that he/she used in this transaction
and output contains the information about the **amount** of the transaction in satoshi, with that being said, technically we can derive the 
address of the recepient and sender of the transaction by studying the script in the output but in our case we will not go as deep. 
so the conclusion is if we managed to decode this message to get the details of the transaction in the block, given an unspent transaction hash, we can scan the block
for when is our unspent transaction hash is used as an input in a transaction and when it does, we can catch it and find details about how much they spent etc.
 
![alt tx](https://github.com/Nicholas-t/Cryptio_btc_block_bg_checker/tree/master/images/tx.PNG) ![alt in_n_out](https://github.com/Nicholas-t/Cryptio_btc_block_bg_checker/tree/master/images/in_n_out.PNG) 
 
# Practical Tutorial (TO DO)

# Conclusion

Tracking an unspent transaction through only socket connection with a remote node