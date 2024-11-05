from meshes4mic.convert.ltm_worker import LTM_Worker
import os
import re

class ZarrToMeshes(LTM_Worker):
    def __init__(self, data_path):
        super().__init__(data_path)
    
    @staticmethod
    def is_valid_datapath(data_path):
        regex = re.compile(r"^(.+)(\.ome\.zarr?)$")
        if not os.path.isfile(data_path):
            return False, "The image path is not a file."
        file_name = os.path.basename(data_path)
        if not regex.match(file_name):
            return False, "The file name does not match the regular expression."
        return True, "Valid ZARR file."