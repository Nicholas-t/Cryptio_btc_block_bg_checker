from bitcoin_block_bg_checker.main import block_search, recent_hash
from time import time


block_hash = recent_hash()

print(block_hash)

#550067 blocks

block_hash = '000000000000000000161a4d8d05f96dda16d23262a3540c39c4365b38f1c1f8'

now1 = time()

txn = block_search(("164.132.229.117", 8333),
				block_hash,
                target_unspent_tx=["013580abb1c034ade232da56e743299dca7e1372a44a95ea37b8673baf266198"])

now2 = time()

print('Scan took {} seconds'.format((now2-now1)))

#takes 35 seconds if not trans is detected
"""
benefit:
    - scalable
possible bugs:
    - stopping too early because inv is sent more times than us handling transaction packets
     but fear not because if ti runs every 10 minutes it will be fine
"""