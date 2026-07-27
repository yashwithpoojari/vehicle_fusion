import pandas as pd
from src.geometry.calibration_manager import CalibrationManager
from src.data.inventory import DatasetInventory
from src.data.manifest import ManifestGenerator
from src.data.synchronizer import VideoSynchronizer

from src.detection.yolo_agent import YOLOAgent
from src.detection.packet_builder import PacketBuilder

from src.communication.transmitter import PacketTransmitter
from src.communication.packet_loss import PacketLossSimulator
from src.communication.receiver import PacketReceiver

from src.geometry.projection import WorldProjector

from src.fusion.fusion_engine import EdgeServer

import yaml


CONFIG_PATH = "configs/dataset.yaml"


def main():

    # -----------------------------------------
    # Read configuration
    # -----------------------------------------
    with open(CONFIG_PATH, "r") as f:
        config = yaml.safe_load(f)

    cameras = config["cameras"]
    manifest_path = config["manifest_path"]

    # -----------------------------------------
    # Module 1 : Dataset Inventory
    # -----------------------------------------
    inventory = DatasetInventory(CONFIG_PATH)
    inventory.scan_scene()

    # -----------------------------------------
    # Module 2 : Manifest Generation
    # -----------------------------------------
    manifest = ManifestGenerator(CONFIG_PATH)
    manifest.build_manifest()

    # -----------------------------------------
    # Module 6 : Camera Calibration
    # -----------------------------------------

    manifest_df = pd.read_csv(manifest_path)

    calibration_manager = CalibrationManager(manifest_df)

    calibration_manager.load()

    calibration_manager.summary()

    # -----------------------------------------
    # Create one projector for each camera
    # -----------------------------------------

    projectors = {}

    for camera in cameras:

        calibration = calibration_manager.get(camera)

        projectors[camera] = WorldProjector(calibration)

    # -----------------------------------------
    # Module 3 : Video Synchronization
    # -----------------------------------------
    synchronizer = VideoSynchronizer(
        manifest_path,
        cameras
    )

    # -----------------------------------------
    # Module 4 : YOLO Detection
    # -----------------------------------------
    detector = YOLOAgent()

    builder = PacketBuilder()

    # -----------------------------------------
    # Module 5 : Communication Layer
    # -----------------------------------------
    transmitter = PacketTransmitter()

    packet_loss = PacketLossSimulator(loss_rate=0.0)

    receiver = PacketReceiver()

    edge_server = EdgeServer()

    # -----------------------------------------
    # Process first synchronized frame
    # -----------------------------------------
    frame_id = 0

    frames = synchronizer.read_frame(frame_id)

    if frames is None:
        print("Unable to read synchronized frame.")
        return

    for camera, frame in frames.items():

        print(f"\n{camera}")

        detections = detector.detect(frame)

        packets = builder.build(
            frame_id,
            camera,
            detections
        )

        packets = transmitter.transmit(packets)

        packets = packet_loss.apply(packets)

        receiver.receive(packets)

        edge_server.receive(packets)

        print(f"Packets Sent : {len(packets)}")

        for packet in packets:
            print(packet)

            projection = projectors[camera].bbox_to_world(packet.bbox)

            print(
                "World Point :",
                projection["world_point"]
            )

    synchronizer.release()

    # -----------------------------------------
    # Communication Summary
    # -----------------------------------------
    print("\n========================================")
    print("Communication Summary")
    print("========================================")

    print(transmitter.statistics())
    print(packet_loss.statistics())
    print(f"Edge Server Queue : {len(receiver.get_packets())} packets")
    edge_server.summary()
    

if __name__ == "__main__":
    main()