from ltm import LTM
import re
import os

class MultiTiffToMeshes(LTM):
    def __init__(self, data_path):
        super().__init__(data_path)
    
    @staticmethod
    def is_valid_datapath(data_path):
        regex = re.compile(r"^(.+)([sScCtTfF][0-9]{1,3}\-?){1,3}(\.tiff?)$")
        if not os.path.isdir(data_path):
            return False, "The image path is not a file."
        content = os.listdir(data_path)
        for file_name in content:
            if not regex.match(file_name):
                return False, "The file name does not match the regular expression."
        return True, "Valid TIFF file."