from pathlib import Path
import cv2
import yaml


class DatasetInventory:

    def __init__(self, config_path):

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.dataset_root = Path(self.config["dataset_root"])
        self.split = self.config["split"]
        self.scene = self.config["scene"]
        self.cameras = self.config["cameras"]

    def scan_scene(self):

        scene_path = self.dataset_root / self.split / self.scene

        print("=" * 60)
        print(f"Scene : {self.scene}")
        print("=" * 60)

        for camera in self.cameras:

            video_folder = scene_path / camera / "out_rgb"

            video_files = list(video_folder.glob("*.mp4"))

            if len(video_files) == 0:
                print(f"{camera} : Video not found")
                continue

            video = video_files[0]

            cap = cv2.VideoCapture(str(video))

            frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

            cap.release()

            print(f"\nCamera : {camera}")
            print(f"Video   : {video.name}")
            print(f"Frames  : {frame_count}")
            print(f"FPS     : {fps}")
            print(f"Size    : {width} x {height}")