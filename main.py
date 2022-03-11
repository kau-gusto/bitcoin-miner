from threading import Thread
from functools import lru_cache
from hashlib import sha256
import time
import sys


def strToSha256(text: str):
    return sha256(text.encode()).hexdigest()


class Miner(Thread):

    def __init__(self, num_block: int, transation: str, previous_hash: str,
                 n0: int):
        Thread.__init__(self)
        self.num_block = num_block
        self.transation = transation
        self.previous_hash = previous_hash
        self.n0 = n0
        self.new_hash = None

    def hash(self, nonce):
        text = \
            str(self.num_block) + self.transation + \
            self.previous_hash + str(nonce)
        new_hash = strToSha256(text)
        if new_hash.startswith("0" * self.n0):
            self.new_hash = new_hash

    def run(self):
        after = time.time()
        nonce = 0
        while True:
            self.hash(nonce)
            if(self.new_hash != None):
                break
            nonce += 1

        print(f"{self.new_hash=}, {nonce=} in {(time.time() - after)}s")


if __name__ == "__main__":
    args = len(sys.argv)
    num_block = 716186 if args <= 1 else int(sys.argv[1])
    transation = "a=>b, b=>c, c=>d" if args <= 2 else sys.argv[2]
    previous_hash = "000000000000000000062a46328d6747614570cb4ceb2daf9cfe2a0295cc2137" if args <= 3 else sys.argv[
        3]
    n0 = 4 if args <= 4 else int(sys.argv[4])

    Miner(num_block, transation, previous_hash, n0).start()
