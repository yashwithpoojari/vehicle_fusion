import numpy as np


class WorldProjector:

    def __init__(self, calibration):

        self.calibration = calibration

        self.K = calibration.intrinsic

        self.E = calibration.extrinsic

        self.position = calibration.position

    def bbox_to_world(self, bbox):

        """
        Convert a detection bounding box into an approximate
        world coordinate.

        Current version:
        Uses the bottom-center of the bounding box together
        with the camera position.

        Returns:
            {
                "image_point": (u, v),
                "world_point": (x, y, z)
            }
        """

        x1, y1, x2, y2 = bbox

        # Bottom center of bounding box
        u = (x1 + x2) / 2.0
        v = y2

        # Camera position
        cam_x, cam_y, cam_z = self.position

        # Simple placeholder projection.
        # This will be replaced by geometric projection
        # in the next stage.
        world_x = cam_x + (u - self.K[0, 2]) / 100.0
        world_y = cam_y + (v - self.K[1, 2]) / 100.0
        world_z = 0.0

        return {

            "image_point": (u, v),

            "world_point": (
                float(world_x),
                float(world_y),
                float(world_z)
            )

        }