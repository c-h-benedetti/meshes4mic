from abc import ABC, abstractmethod
import numpy as np

class LTM_Worker(ABC):
    def __init__(self, data_path):
        # Absolute path of the image to be processed.
        self._data_path    = None
        # Regular expression that the filename must respect to be processed.
        self._regex        = None
        # Properties of the image to use for processing.
        self._img_ppts     = None
        # Threads used for processing.
        self._threads      = None
        self._set_data_path(data_path)
        self._fetch_metadata()

    def get_image_properties(self):
        """ Returns an ImageAttributes instance with the properties of the image. """
        return self._img_ppts

    @staticmethod
    @abstractmethod
    def is_valid_datapath(data_path):
        """ Checks the extension of the file to determine if this specialized class can process it. """
        pass

    @abstractmethod
    def _fetch_metadata(self):
        """ Probes the file/folder to extract the metadata of the image. """
        pass

    def _set_data_path(self, data_path):
        self._data_path = data_path
    
    def get_bucket_size(self, max_ram):
        ds = np.dtype(self._img_ppts.dtype).itemsize # size of a voxel in bytes.
        n_voxels = max_ram // ds
        base_size = int(round(n_voxels ** (1/3)))
        dz = min(self._img_ppts.depth, base_size)
        dy = min(self._img_ppts.height, n_voxels // (dz * base_size))
        dx = min(self._img_ppts.width, n_voxels // (dz * dy))
        while dz * dy * dx > n_voxels:
            if dx > 1:
                dx -= 1
            elif dy > 1:
                dy -= 1
            elif dz > 1:
                dz -= 1
        return self._img_ppts.astuple({'Z': dz, 'Y': dy, 'X': dx})
    
    @abstractmethod
    def to_meshes(self, output_path, sampling_rate, n_threads):
        pass