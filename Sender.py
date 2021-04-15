import numpy as np
import random

from Distributions import Uniform
from Packet import Packet


class Sender:

    def __init__(self, source_size, distribution):
        self.source_size = source_size

        self.distribution = distribution

        # TODO: Add error rate

        self.source = np.random.randint(1, source_size, source_size)

        # print(self.source)

    def create_packet(self):
        block_amount = self.distribution.sample_from_dist()

        value = 0
        block_ids = np.random.choice(np.arange(0, self.source_size), replace=False, size=block_amount)

        for block_id in block_ids:
            value += self.source[block_id]

        packet = Packet(value, block_ids)

        return packet

# Sender(20)

