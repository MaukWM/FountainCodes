import numpy as np
import random

class Receiver:

    def __init__(self, source_size, error_rate, fast_mode=True):
        self.source_size = source_size

        self.result_message = [None] * source_size

        self.received_packets = []
        self.to_decode = []

        self.total_received = 0

        self.error_rate = error_rate

        #TODO: Implement fast mode cause it's slow for more than 20 packets lmao
        # self.fast_mode = fast_mode

        # print(self.result_message)

    # package comes as [(value, [index1, index2, index4, ...)]
    def receive(self, packet):
        self.total_received += 1

        if random.uniform(0, 1) < self.error_rate:
            return

        # Check and remove existing connections before adding packet
        for connection_id in packet.connections:
            if self.result_message[connection_id] is not None:
                packet.value -= self.result_message[connection_id]
                packet.connections = np.delete(packet.connections, np.where(packet.connections == connection_id))

        # if self.fast_mode:
        #     self.to_decode.append(packet)
        # else:
        self.received_packets.append(packet)

    def decode_packet(self):
        # Check if there is a connection with degree 1
        for packet in self.received_packets:
            if len(packet.connections) == 1:
                self.result_message[packet.connections[0]] = packet.value

                # if self.fast_mode:
                #     # Remove each packet with this connection
                #     self.to_decode = [pckt for pckt in self.to_decode if not (len(pckt.connections) == 1 and pckt.connections[0] == packet.connections[0])]
                #     self.to_decode.remove(packet)
                #     return True
                # else:
                    # Better: remove each connection from each packet
                self.remove_connection(packet.connections[0], packet.value)
                    # return True

        # Return false if nothing could be decoded
        return False

    def remove_connection(self, connection_id, value):
        for packet in self.received_packets:
            if connection_id in packet.connections:
                packet.value -= value
                packet.connections = np.delete(packet.connections, np.where(packet.connections == connection_id))



