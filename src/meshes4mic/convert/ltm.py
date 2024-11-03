class LTM(object):
    def __init__(self, data_path):
        # Absolute path of the image to be processed.
        self._data_path    = None
        # Regular expression that the filename must respect to be processed.
        self._regex        = None
        # Properties of the image to use for processing.
        self._img_ppts     = None
        # ==> Init
        self._set_data_path(data_path)
        self._fetch_metadata()
    
    def get_image_properties(self):
        return self._img_ppts

    @staticmethod
    def is_valid_datapath(data_path):
        return False, "Not implemented."

    def _fetch_metadata(self):
        raise NotImplementedError("Method not implemented.")

    def _fetch_ome_metadata(self):
        raise NotImplementedError("Method not implemented.")

    def _set_data_path(self, data_path):
        self._data_path = data_path