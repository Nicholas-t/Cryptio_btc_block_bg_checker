from bitcoin_block_bg_checker.main import block_search, recent_hash
from time import time


block_hash = recent_hash()

print(block_hash)

now1 = time()

txn = block_search(("91.121.170.214", 8333),
				block_hash,
                target_unspent_tx="82e63e889759bccc0561d771c657fb0e451bd3b750d5735535f8c770891c1a46")

now2 = time()

print('Scan took {} seconds'.format((now2-now1)))