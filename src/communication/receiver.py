class PacketReceiver:

    def __init__(self):

        self.received_packets = []

    def receive(self, packets):

        self.received_packets.extend(packets)

    def get_packets(self):

        return self.received_packets

    def clear(self):

        self.received_packets = []