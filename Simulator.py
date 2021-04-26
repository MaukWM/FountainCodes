import time

import numpy as np

from Distributions import Uniform, OneShot, IdealSoliton, RobustSoliton
from Receiver import Receiver
from Sender import Sender

import matplotlib.pyplot as plt

class Simulator:

    def __init__(self, source_size, distribution, error_rate, fast_mode=True):
        self.source_size = source_size
        self.error_rate = error_rate
        self.fast_mode = fast_mode

        self.packet_len_1_sent = False

        if distribution == 'uniform':
            self.distribution = Uniform(source_size)

        elif distribution == 'one_shot':
            self.distribution = OneShot(source_size)

        elif distribution == 'ideal_soliton':
            self.distribution = IdealSoliton(source_size)

        elif distribution == 'robust_soliton':
            self.distribution = RobustSoliton(source_size, 0.1, error_rate)

        else:
            raise Exception("No distribution provided")

        self.sender = None
        self.receiver = None

    def send_packet(self):
        packet = self.sender.create_packet()
        self.packet_len_1_sent = len(packet.connections) == 1
        return self.receiver.receive(packet)

    def decode(self, pckt1_sent=False):
        return self.receiver.decode_packet(pckt1_sent=pckt1_sent)

    def simulate(self):
        self.sender = Sender(self.source_size, self.distribution)
        self.receiver = Receiver(self.source_size, self.error_rate, fast_mode=self.fast_mode)

        successful_decode = False
        successful_send = False

        while not self.receiver.decoded:
            # Send a packet and attempt to decode if it is received
            if not successful_decode:
                successful_send = self.send_packet()
            if successful_send:
                successful_decode = self.decode(pckt1_sent=self.packet_len_1_sent)
                self.packet_len_1_sent = False
        # print(self.receiver.result_message)
        # print(self.receiver.total_received)
        return self.receiver.total_received

    def run_simulations(self, amount):
        print("=== Running {} {} simulations ===".format(amount, self.distribution.name()))

        start = time.time()

        total_packets_received = []

        for i in range(amount):
            total_packets_received.append(self.simulate())

        plt.hist(total_packets_received, density=True, bins=50)

        plt.xlabel("Total amount of packets received")
        # TODO: ylabel?

        plt.show()

        print("Mean: {:.2f}".format(np.mean(total_packets_received)))
        print("Standard deviation: {:.2f}".format(np.std(total_packets_received)))
        print("Efficiency: {}".format(self.source_size / np.average(total_packets_received)))
        print("Total time: {:.2f} seconds".format(time.time() - start))
        print()


if __name__ == "__main__":
    source_size = 75
    error_rate = 0.9
    sim_amount = 10

    # sim_uniform = Simulator(source_size, 'uniform', error_rate, fast_mode=False)
    # sim_uniform.run_simulations(sim_amount)

    sim_uniform_fast = Simulator(source_size, 'uniform', error_rate, fast_mode=True)
    sim_uniform_fast.run_simulations(sim_amount)

    # sim_oneshot = Simulator(source_size, 'one_shot', error_rate)
    # sim_oneshot.run_simulations(sim_amount)
    #
    # sim_idealsoliton = Simulator(source_size, 'ideal_soliton', error_rate)
    # sim_idealsoliton.run_simulations(sim_amount)
    #
    # sim_robustsoliton = Simulator(source_size, 'robust_soliton', error_rate)
    # sim_robustsoliton.run_simulations(sim_amount)
