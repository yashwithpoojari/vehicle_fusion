from copy import deepcopy


class PacketTransmitter:

    def __init__(self):

        self.total_packets_sent = 0

    def transmit(self, packets):

        transmitted_packets = []

        for packet in packets:

            transmitted_packets.append(deepcopy(packet))

            self.total_packets_sent += 1

        return transmitted_packets

    def statistics(self):

        return {

            "packets_sent": self.total_packets_sent

        }