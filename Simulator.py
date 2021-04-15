import time

import numpy as np

from Distributions import Uniform, OneShot, IdealSoliton, RobustSoliton
from Receiver import Receiver
from Sender import Sender

import matplotlib.pyplot as plt

class Simulator:

    def __init__(self, source_size, distribution, error_rate):
        self.source_size = source_size
        self.error_rate = error_rate

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
        self.receiver.receive(packet)

    def decode(self):
        return self.receiver.decode_packet()

    def simulate(self):
        self.sender = Sender(self.source_size, self.distribution)
        self.receiver = Receiver(self.source_size, self.error_rate)

        while None in self.receiver.result_message:
            self.send_packet()
            self.decode()
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
    source_size = 100
    error_rate = 0
    sim_amount = 500

    sim_uniform = Simulator(source_size, 'uniform', error_rate)
    sim_uniform.run_simulations(sim_amount)

    sim_oneshot = Simulator(source_size, 'one_shot', error_rate)
    sim_oneshot.run_simulations(sim_amount)

    sim_idealsoliton = Simulator(source_size, 'ideal_soliton', error_rate)
    sim_idealsoliton.run_simulations(sim_amount)

    sim_robustsoliton = Simulator(source_size, 'robust_soliton', error_rate)
    sim_robustsoliton.run_simulations(sim_amount)
