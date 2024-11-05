from abc import ABC, abstractmethod

class ImageProperties(ABC):
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

    def is_2d_isotropic(self):
        """
        Checks if the sampling interval is the same along the X and Y axes.

        Returns:
            bool: True if the image is 2D-isotropic, False otherwise.
        """
        return abs(self.x_interval - self.y_interval) < 1e-6
    
    def is_3d_isotropic(self):
        """
        Checks if the sampling interval is the same along the X, Y and Z axes.

        Returns:
            bool: True if the image is 3D-isotropic, False otherwise.
        """
        if not self.is_3d():
            raise ValueError("The image is 2D, the Z axis cannot be considered.")
        return self.is_2d_isotropic() and abs(self.x_interval - self.z_interval) < 1e-6

    def anisotropy_ratio(self, axes='XZ'):
        """
        Computes the anisotropy ratio between two spatial axes (X, Y and Z).
        The order of the division (numerator/denominator) is the order of the axes in the 'axes' parameter.
        Ex: 'XZ' -> X / Z
        The Z axis cannot be considered for 2D images.
        The case of the axes is not important ('x' == 'X').

        Args:
            axes (str): a two-character string representing the axes to compare (ex: 'XZ').
        
        Returns:
            float: the anisotropy ratio.
        """
        axes = axes.upper()
        if self.is_2d() and ('Z' in axes):
            raise ValueError("The image is 2D, the Z axis cannot be considered.")
        if not all(c in {'X', 'Y', 'Z'} for c in axes):
            raise ValueError("Invalid axis. Must be a combination of 'X', 'Y' and 'Z'.")
        if len(axes) != 2:
            raise ValueError("Invalid axis. Must be a combination of two axes.")
        values = self._axis_to_attr()
        return values[axes[0]] / values[axes[1]]

    def is_2d(self):
        """
        Checks whether the image is spatially 2D.
        Time and channel axes are not considered here.
        A multi-channel image with a time axis is still considered 2D if it has no depth.

        Returns:
            bool: True if the image is 2D, False otherwise.
        """
        return self.depth == 1
    
    def is_3d(self):
        """
        Checks whether the image is spatially 3D.
        Time and channel axes are not considered here.
        A multi-channel image with a time axis is still considered 3D if it has depth.

        Returns:
            bool: True if the image is 3D, False otherwise.
        """
        return self.depth > 1
    
    def is_calibrated(self, exclude_time=False):
        """
        Verifies if the image has all the necessary attributes to be considered calibrated.
        A calibrated image has a known sampling interval and unit for each spatial axis.
        A fully calibrated image also has a known sampling interval and unit for the time axis.

        Args:
            exclude_time (bool): whether to exclude the time axis from the verification.

        Returns:
            bool: True if the image is calibrated, False otherwise.
        """
        # Any image has at least these two dimensions.
        if (self.x_interval is None) or (self.y_interval is None) or (self.x_unit is None) or (self.y_unit is None):
            return False
        # If the image is 3D, we also check the Z axis.
        if self.is_3d() and ((self.z_interval is None) or (self.z_unit is None)):
            return False
        # If the image has multiple frames, we also check the time axis.
        if (not exclude_time) and (self.n_frames > 1) and ((self.time_interval is None) or (self.time_unit is None)):
            return False
        return True

    def _axis_to_attr(self):
        """
        Creates a dictionary that maps each axis to its corresponding attribute.

        Returns:
            dict: the mapping between axes and attributes.
        """
        return {
            "X": self.width,
            "Y": self.height,
            "Z": self.depth,
            "C": self.n_channels,
            "T": self.n_frames
        }

    def astuple(self, values_dict):
        """
        Assembles a dictionary of values into a tuple following the axes order for this image.
        Ex: values_dict = {'X': 128, 'Y': 128, 'Z': 64} and self.axes = ('Y', 'Z', 'X') -> (128, 64, 128)

        Args:
            values_dict: dictionary containing the values to be assembled.
        
        Returns:
            tuple: the assembled values
        """
        basis = [1 for _ in range(len(self.axes))]
        for i, ax in enumerate(self.axes):
            basis[i] = values_dict.get(ax, 1)
        return tuple(basis)

    def global_shape(self):
        """
        Builds a tuple representing the shape of the image.
        The order of the axes is the same as the one in self.axes.

        Returns:
            tuple: the shape of the image.
        """
        a2a = self._axis_to_attr()
        shape = []
        for item in self.axes:
            shape.append(a2a[item])
        return tuple(shape)

    @abstractmethod
    def _parse_attributes(self):
        """
        Responsible for extracting the attributes from the image's metadata.
        This method should be implemented in a subclass.
        """
        pass
