from ltm import LTM
from tiff_attributes import TiffAttributes
import tifffile
import xml.etree.ElementTree as ET
import os
import re

class TiffToMeshes(LTM):
    def __init__(self, data_path):
        super().__init__(data_path)

    def _fetch_metadata(self):
        with tifffile.TiffFile(self._data_path) as tif:
            ome_xml = ET.fromstring(tif.ome_metadata)
            tif_metadata = tif.series[0]
            self._img_ppts = TiffAttributes(ome_xml, tif_metadata)

    @staticmethod
    def is_valid_datapath(data_path):
        regex = re.compile(r"^(.+)(\.ome\.tiff?)$")
        if not os.path.isfile(data_path):
            return False, "The image path is not a file."
        file_name = os.path.basename(data_path)
        if not regex.match(file_name):
            return False, "The file name does not match the regular expression."
        return True, "Valid TIFF file."