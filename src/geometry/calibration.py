import json
import numpy as np


class CameraCalibration:

    def __init__(self, calibration_file):

        with open(calibration_file, "r") as f:
            data = json.load(f)

        self.intrinsic = np.array(
            data["intrinsic_matrix"],
            dtype=float
        )

        self.extrinsic = np.array(
            data["extrinsic_matrix"],
            dtype=float
        )

        self.position = np.array([
            data["x"],
            data["y"],
            data["z"]
        ])

        self.pitch = data["pitch"]
        self.yaw = data["yaw"]
        self.roll = data["roll"]

    def summary(self):

        print("\n==============================")
        print("Camera Calibration")
        print("==============================")

        print("\nIntrinsic Matrix")

        print(self.intrinsic)

        print("\nExtrinsic Matrix")

        print(self.extrinsic)

        print("\nPosition")

        print(self.position)

        print(
            f"\nPitch : {self.pitch}"
        )

        print(
            f"Yaw   : {self.yaw}"
        )

        print(
            f"Roll  : {self.roll}"
        )