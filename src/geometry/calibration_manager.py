from src.geometry.calibration import CameraCalibration


class CalibrationManager:

    def __init__(self, manifest):

        self.manifest = manifest
        self.calibrations = {}

    def load(self):

        for _, row in self.manifest.iterrows():

            camera = row["camera"]

            calibration_file = row["calibration_path"]

            self.calibrations[camera] = CameraCalibration(
                calibration_file
            )

    def get(self, camera):

        return self.calibrations[camera]

    def summary(self):

        print("\n==============================")
        print("Loaded Calibrations")
        print("==============================")

        for camera in self.calibrations:

            print(camera)