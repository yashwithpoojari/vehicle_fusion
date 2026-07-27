from src.geometry.calibration import CameraCalibration

calibration = CameraCalibration(
    r"C:\Users\Yashwith Poojari\Documents\internship\vehicle_fusion\data\raw\synthehicle\calibration\overlapping\Town01\camera_info\camera_1.txt"
)

calibration.summary()