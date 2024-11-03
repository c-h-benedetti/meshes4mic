import psutil
from utils import verbose_bytes
from tiff2meshes import TiffToMeshes
from mtiff2meshes import MultiTiffToMeshes
from zarr2meshes import ZarrToMeshes

class LabelsToMesh(object):

    candidates = [
        TiffToMeshes, 
        MultiTiffToMeshes, 
        ZarrToMeshes
    ]

    def __init__(self, labels_path, verbose=False, memory_limit=None, threads_limit=None):
        # Absolute path of the image to be processed.
        self._labels_path = None
        # Object that will be used to process the image.
        self._processor = None
        # Whether to print information during the process.
        self.verbose = verbose

        self._set_max_memory(memory_limit)
        self._set_n_thread(threads_limit)
        self._set_data_path(labels_path)
    
    def _set_max_memory(self, max_memory):
        """
        Allows to set manually the maximum amount of memory to use.

        Args:
            max_memory (int): Max number of bytes that we can use. 
                              If None, it will use either 50% of the total memory or 90% of the available memory.
        """
        self.max_memory = max_memory
        if max_memory is None:
            self.max_memory = min(
                int(0.5 * psutil.virtual_memory().total),
                int(0.9 * psutil.virtual_memory().available))
        self._log(f"Max memory: {verbose_bytes(self.max_memory)}")
    
    def _set_n_thread(self, threads_limit):
        """
        Allows to set manually the maximum number of threads to use.

        Args:
            threads_limit (int): Max number of threads to use. 
                                 If None, it will use the number of logical CPUs.
        """
        self.max_threads = threads_limit
        if threads_limit is None:
            self.max_threads = psutil.cpu_count(logical=True)
        self._log(f"Max threads: {self.max_threads}")

    def _log(self, msg):
        """ Prints something if the verbose flag is set to True. """
        if self.verbose:
            print(msg)

    def _set_data_path(self, labels_path):
        """ Tries to find the right candidate to process the image. """
        self._search_processor(labels_path)
        self._log(self._processor.get_image_properties())
    
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