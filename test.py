from bitcoin_block_bg_checker.main import block_search, recent_hash
from time import time


block_hash = recent_hash()

print(block_hash)
block_hash = '0000000000000000001e5d0d4568626b416ddccb6089e34d4173dafcc34eaa4f'
now1 = time()

txn = block_search(("164.132.229.117", 8333),
				block_hash,
                target_unspent_tx=["0424202c1da7cee9a0e2befd40a3ba43507baa8c10e78842a6c73feb5e96d4d5"])

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