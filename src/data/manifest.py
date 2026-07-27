from pathlib import Path
import cv2
import yaml
import pandas as pd


class ManifestGenerator:

    def __init__(self, config_path):

        with open(config_path, "r") as f:
            self.config = yaml.safe_load(f)

        self.dataset_root = Path(self.config["dataset_root"])
        self.split = self.config["split"]
        self.calibration_root = Path(self.config["calibration_root"])
        self.output_csv = Path(self.config["manifest_path"])

    def build_manifest(self):

        split_path = self.dataset_root / self.split

        records = []

        scenes = sorted([x for x in split_path.iterdir() if x.is_dir()])

        for scene in scenes:

            scene_name = scene.name

            parts = scene_name.split("-")

            town = parts[0]
            layout = "Overlapping" if "O" in parts else "Non-Overlapping"
            weather = parts[-1]

            calibration_folder = (
                self.calibration_root /
                layout.lower().replace("-", "_") /
                town /
                "camera_info"
            )

            cameras = sorted([x for x in scene.iterdir() if x.is_dir()])

            for camera in cameras:

                video = camera / "out_rgb" / "video.mp4"
                gt = camera / "gt" / "gt.txt"

                camera_number = camera.name.replace("C", "").lstrip("0")
                calibration = calibration_folder / f"camera_{camera_number}.txt"

                cap = cv2.VideoCapture(str(video))

                frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
                fps = cap.get(cv2.CAP_PROP_FPS)
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

                cap.release()

                records.append({

                    "scene": scene_name,
                    "town": town,
                    "layout": layout,
                    "weather": weather,
                    "camera": camera.name,
                    "video_path": str(video),
                    "gt_path": str(gt),
                    "calibration_path": str(calibration),
                    "frame_count": frames,
                    "fps": fps,
                    "width": width,
                    "height": height

                })

        df = pd.DataFrame(records)

        self.output_csv.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(self.output_csv, index=False)

        print("\nManifest Created Successfully")
        print(df.head())