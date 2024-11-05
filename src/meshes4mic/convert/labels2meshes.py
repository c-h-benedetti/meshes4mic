import psutil
from meshes4mic.convert.utils import verbose_bytes
from meshes4mic.convert.tiff2meshes import TiffToMeshes
from meshes4mic.convert.zarr2meshes import ZarrToMeshes


class LabelsToMeshes(object):

    candidates = [
        TiffToMeshes,
        ZarrToMeshes
    ]

    def __init__(self, labels_path, sampling=1, verbose=False, memory_limit=None, threads_limit=None):
        # Absolute path of the image to be processed.
        self._labels_path = None
        # Object that will be used to process the image.
        self._processor = None
        # Whether to print information during the process.
        self._verbose = verbose
        # Maximum amount of memory to use.
        self._max_memory = None
        # Maximum number of threads to use.
        self._max_threads = None
        # Sampling rate of the voxels grid.
        self.sampling_rate = sampling

        self.max_memory = memory_limit
        self.n_threads  = threads_limit
        self._set_data_path(labels_path)
    
    @property
    def max_memory(self):
        return self._max_memory

    @max_memory.setter
    def max_memory(self, max_memory):
        """
        Allows to set manually the maximum amount of memory to use.

        Args:
            max_memory (int): Max number of bytes that we can use. 
                              If None, it will use either 50% of the total memory or 90% of the available memory.
        """
        self._max_memory = max_memory
        if max_memory is None:
            self._max_memory = min(
                int(0.5 * psutil.virtual_memory().total),
                int(0.9 * psutil.virtual_memory().available))
        self._log(f"Max memory: {verbose_bytes(self._max_memory)}")
    
    @property
    def n_threads(self):
        return self._max_threads

    @n_threads.setter
    def n_threads(self, threads_limit):
        """
        Allows to set manually the maximum number of threads to use.

        Args:
            threads_limit (int): Max number of threads to use. 
                                 If None, it will use the number of logical CPUs.
        """
        self._max_threads = threads_limit
        if threads_limit is None:
            self._max_threads = psutil.cpu_count(logical=True)
        self._log(f"Max threads: {self._max_threads}")

    def _log(self, msg):
        """ Prints something if the verbose flag is set to True. """
        if self._verbose:
            print(msg)

    def _set_data_path(self, labels_path):
        """ Tries to find the right candidate to process the image. """
        self._search_processor(labels_path)
        self._log(self._processor.get_image_properties())
        self._log(self._processor.process_buckets(self.sampling_rate, self._max_memory))
    
    def _search_processor(self, labels_path):
        """
        Browses the whell of candidates (LabelsToMesh.candidates) to find the right one to process the image.
        The file extension is used to determine which candidate is the right one.

        Args:
            labels_path (str): Absolute path of the image to be processed.

        Raises:
            ValueError: If no candidate is found to process the image.
        """
        for c in self.candidates:
            valid, msg = c.is_valid_datapath(labels_path)
            self._log(f"Checking {c.__name__} validity: {msg}")
            if valid:
                self._labels_path = labels_path
                self._processor   = c(labels_path)
                return
        raise ValueError("Didn't find a valid candidate given the file extension.")
    
    def labels2meshes(self, output_path):
        """
        Converts the labels into meshes.

        Args:
            output_path (str): Absolute path of the folder where the meshes will be saved.
        """
        self._processor.labels2meshes(output_path, self.sampling_rate, self._max_threads)