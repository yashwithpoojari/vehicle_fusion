from dataclasses import dataclass


@dataclass
class DetectionPacket:

    frame_id: int

    camera_id: str

    vehicle_class: str

    confidence: float

    bbox: list


class PacketBuilder:

    def build(self, frame_id, camera_id, detections):

        packets = []

        for detection in detections:

            packets.append(

                DetectionPacket(

                    frame_id=frame_id,

                    camera_id=camera_id,

                    vehicle_class=detection["class"],

                    confidence=detection["confidence"],

                    bbox=detection["bbox"]

                )

            )

        return packets