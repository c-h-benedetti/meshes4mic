from meshes4mic.convert.ltm_worker import LTM_Worker
from meshes4mic.convert.tiff_properties import TiffProperties
import tifffile
import xml.etree.ElementTree as ET
import os
import re
import dask.array as da

class TiffToMeshes(LTM_Worker):
    def __init__(self, data_path):
        super().__init__(data_path)

    def _fetch_metadata(self):
        with tifffile.TiffFile(self._data_path) as tif:
            ome_xml = ET.fromstring(tif.ome_metadata)
            tif_metadata = tif.series[0]
            self._img_ppts = TiffProperties(ome_xml, tif_metadata)

    @staticmethod
    def is_valid_datapath(data_path):
        regex = re.compile(r"^(.+)(\.ome\.tiff?)$")
        if not os.path.isfile(data_path):
            return False, "The image path is not a file."
        file_name = os.path.basename(data_path)
        if not regex.match(file_name):
            return False, "The file name does not match the regular expression."
        return True, "Valid TIFF file."
    
    def to_meshes(self, output_path, sampling_rate, n_threads):
        chunk_size = self.get_chunk_size(self._max_memory)
        with tifffile.TiffFile(self._data_path) as tif:
            dask_array = da.from_array(tif.asarray(), chunks=chunk_size)


"""

Fonctionnement:
===============

- Lancer le pool de threads.
- Charger un chunk de données dans la mémoire.
- Les threads vont consommer la data.
- Une fois que tous les threads ont fini de consommer la data, on peut charger un nouveau chunk.
- Il va falloir un système de wait solide pour éviter les deadlocks.
- Il va falloir croiser ça avec Dask.

"""