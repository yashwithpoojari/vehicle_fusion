import cv2
import pandas as pd


class VideoSynchronizer:

    def __init__(self, manifest_path, cameras):

        self.manifest = pd.read_csv(manifest_path)

        self.cameras = cameras

        self.captures = {}

        self.frame_count = None

        self.open_videos()

    def open_videos(self):

        for camera in self.cameras:

            row = self.manifest[self.manifest["camera"] == camera].iloc[0]

            cap = cv2.VideoCapture(row["video_path"])

            self.captures[camera] = cap

            frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

            if self.frame_count is None:
                self.frame_count = frames
            else:
                self.frame_count = min(self.frame_count, frames)

    def read_frame(self, frame_number):

        synchronized_frames = {}

        for camera, cap in self.captures.items():

            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

            success, frame = cap.read()

            if not success:
                return None

            synchronized_frames[camera] = frame

        return synchronized_frames

    def release(self):

        for cap in self.captures.values():
            cap.release()