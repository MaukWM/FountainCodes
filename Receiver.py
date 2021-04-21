import numpy as np
import random

class Receiver:

    def __init__(self, source_size, error_rate, fast_mode=True):
        self.source_size = source_size

        self.result_message = [None] * source_size

        self.received_packets = []

        self.total_received = 0

        self.error_rate = error_rate

        self.fast_mode = fast_mode

        self.decoded_amount = 0
        self.decoded = False

        # print(self.result_message)

    # package comes as [(value, [index1, index2, index4, ...)]
    def receive(self, packet):
        self.total_received += 1

        if random.uniform(0, 1) < self.error_rate:
            return False

        # Check and remove existing connections before adding packet
        for connection_id in packet.connections:
            if self.result_message[connection_id] is not None:
                packet.value -= self.result_message[connection_id]
                packet.connections = np.delete(packet.connections, np.where(packet.connections == connection_id))

        self.received_packets.append(packet)

        return True

    def decode_packet(self):
        packet_len_1 = list(filter(lambda pckt: len(pckt.connections) == 1, self.received_packets))

        if len(packet_len_1) == 0:
            return False

        dec_packet = packet_len_1[0]
        self.result_message[dec_packet.connections[0]] = dec_packet.value

        self.remove_connection(dec_packet.connections[0], dec_packet.value)

        self.decoded_amount += 1

        if self.decoded_amount == self.source_size:
            self.decoded = True

        return True

    def remove_connection(self, connection_id, value):
        remaining_packets = []
        for packet in self.received_packets:
            if connection_id in packet.connections:
                packet.value -= value
                packet.connections = np.delete(packet.connections, np.where(packet.connections == connection_id))
            if packet.value > 0:
                remaining_packets.append(packet)
        if self.fast_mode:
            self.received_packets = remaining_packets



