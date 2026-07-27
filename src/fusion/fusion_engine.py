from collections import defaultdict


class EdgeServer:

    def __init__(self):

        # frame_id -> packets
        self.buffer = defaultdict(list)

    def receive(self, packets):

        if not packets:
            return

        frame_id = packets[0].frame_id

        self.buffer[frame_id].extend(packets)

    def get_frame_packets(self, frame_id):

        return self.buffer.get(frame_id, [])

    def clear_frame(self, frame_id):

        if frame_id in self.buffer:
            del self.buffer[frame_id]

    def summary(self):

        print("\n==============================")
        print("Edge Server")
        print("==============================")

        for frame_id, packets in self.buffer.items():

            print(
                f"Frame {frame_id} : {len(packets)} packets"
            )