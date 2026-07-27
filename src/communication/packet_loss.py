import random


class PacketLossSimulator:

    def __init__(self, loss_rate=0.0):

        self.loss_rate = loss_rate

        self.total_packets = 0

        self.dropped_packets = 0

    def apply(self, packets):

        remaining = []

        for packet in packets:

            self.total_packets += 1

            if random.random() < self.loss_rate:

                self.dropped_packets += 1

                continue

            remaining.append(packet)

        return remaining

    def statistics(self):

        return {

            "total_packets": self.total_packets,

            "dropped_packets": self.dropped_packets,

            "received_packets":
                self.total_packets - self.dropped_packets

        }