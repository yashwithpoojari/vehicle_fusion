from src.data.inventory import DatasetInventory
from src.data.manifest import ManifestGenerator
from src.data.synchronizer import VideoSynchronizer
from src.detection.yolo_agent import YOLOAgent
from src.detection.packet_builder import PacketBuilder


def main():

    inventory = DatasetInventory("configs/dataset.yaml")
    inventory.scan_scene()

    manifest = ManifestGenerator("configs/dataset.yaml")
    manifest.build_manifest()

    synchronizer = VideoSynchronizer(
        "data/manifests/dataset_manifest.csv",
        ["C01", "C02", "C03"]
    )

    frames = synchronizer.read_frame(0)

    agent = YOLOAgent()

    builder = PacketBuilder()

    frame_id = 0

    for camera, frame in frames.items():

        detections = agent.detect(frame)

        print(f"\n{camera}")

        packets = builder.build(
            frame_id,
            camera,
            detections
        )

        print(f"\n{camera}")

        print(f"vehicle packets: {len(packets)}")

        for packet in packets:

            print(packet)

    synchronizer.release()


if __name__ == "__main__":
    main()