class ImageAttributes(object):
    def __init__(self):
        # Distance between two samples along the X axis (a.k.a "pixel width").
        self.x_interval = None
        # Distance between two samples along the Y axis (a.k.a "pixel height").
        self.y_interval = None
        # Distance between two samples along the Z axis (a.k.a "pixel depth").
        self.z_interval = None
        # Physical unit of the X axis.
        self.x_unit = None
        # Physical unit of the Y axis.
        self.y_unit = None
        # Physical unit of the Z axis.
        self.z_unit = None
        # Time interval between two frames.
        self.time_interval = None
        # Physical unit of the time axis.
        self.time_unit = None
        # Number of channels in the image.
        self.n_channels = 1
        # Number of frames in the image.
        self.n_frames = 1
        # Width of the image, in number of voxels.
        self.width = 1
        # Height of the image, in number of voxels.
        self.height = 1
        # Depth of the image, in number of voxels.
        self.depth = 1
        # Axes of the image (TZCYX).
        self.axes = None
        # Data type of the value of each voxel.
        self.dtype = None
        self._parse_attributes()
    
    def __str__(self) -> str:
        return f"X interval: {self.x_interval} {self.x_unit}\nY interval: {self.y_interval} {self.y_unit}\nZ interval: {self.z_interval} {self.z_unit}\nTime interval: {self.time_interval} {self.time_unit}\nNumber of channels: {self.n_channels}\nNumber of frames: {self.n_frames}\nWidth: {self.width}\nHeight: {self.height}\nDepth: {self.depth}\nAxes: {self.axes}\nData type: {self.dtype}"
    
    def anisotropy_factor(self):
        """
        Computes the anisotropy factor of the image.
        """
        if self.is_2d():
            return 1.0
        return max(self.x_interval, self.y_interval, self.z_interval) / min(self.x_interval, self.y_interval, self.z_interval)

    def is_isotropic(self):
        """
        Checks whether the image has isotropic voxels.
        """
        return max(self.x_interval, self.y_interval, self.z_interval) - min(self.x_interval, self.y_interval, self.z_interval) < 1e-6

    def is_2d(self):
        """
        Checks whether the image is 2D.
        """
        return self.depth == 1
    
    def is_3d(self):
        """
        Checks whether the image is 3D.
        """
        return self.depth > 1
    
    def is_calibrated(self):
        # Any image has at least these two dimensions.
        if (self.x_interval is None) or (self.y_interval is None) or (self.x_unit is None) or (self.y_unit is None):
            return False
        # If the image is 3D, we also check the Z axis.
        if self.is_3d() and ((self.z_interval is None) or (self.z_unit is None)):
            return False
        # If the image has multiple frames, we also check the time axis.
        if (self.n_frames > 1) and ((self.time_interval is None) or (self.time_unit is None)):
            return False
        return True

    def _axis_to_attr(self):
        """
        Creates a dictionary that maps each axis to its corresponding attribute.
        """
        return {
            "X": self.width,
            "Y": self.height,
            "Z": self.depth,
            "C": self.n_channels,
            "T": self.n_frames
        }

    def global_shape(self):
        """
        Builds a tuple representing the shape of the image.
        The order of the axes is the same as the one in the 'axes' attribute.
        """
        a2a = self._axis_to_attr()
        shape = []
        for item in self.axes:
            shape.append(a2a[item])
        return tuple(shape)

    def _parse_attributes(self):
        raise NotImplementedError("Method not implemented.")