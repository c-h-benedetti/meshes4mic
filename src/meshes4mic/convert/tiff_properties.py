from meshes4mic.convert.image_properties import ImageProperties
import numpy as np

class TiffProperties(ImageProperties):
    def __init__(self, ome_xml, tif_metadata):
        self._tmp_ome_xml      = ome_xml
        self._tmp_tif_metadata = tif_metadata
        super().__init__()
        
    def _parse_attributes(self):
        self._parse_tif_data()
        self._parse_ome_data()
        del self._tmp_ome_xml
        del self._tmp_tif_metadata
    
    def _parse_ome_data(self):
        pixels_info = self._tmp_ome_xml.find(".//{*}Pixels")
        self.x_interval = float(pixels_info.attrib["PhysicalSizeX"])
        self.y_interval = float(pixels_info.attrib["PhysicalSizeY"])
        self.z_interval = float(pixels_info.attrib["PhysicalSizeZ"])
        self.x_unit = pixels_info.attrib["PhysicalSizeXUnit"]
        self.y_unit = pixels_info.attrib["PhysicalSizeYUnit"]
        self.z_unit = pixels_info.attrib["PhysicalSizeZUnit"]
        self.time_interval = float(pixels_info.attrib["TimeIncrement"])
        self.time_unit = pixels_info.attrib["TimeIncrementUnit"]
        n_c = int(pixels_info.attrib["SizeC"])
        n_t = int(pixels_info.attrib["SizeT"])
        n_x = int(pixels_info.attrib["SizeX"])
        n_y = int(pixels_info.attrib["SizeY"])
        n_z = int(pixels_info.attrib["SizeZ"])
        pairs = [("X", n_x), ("Y", n_y), ("Z", n_z), ("C", n_c), ("T", n_t)]
        self._check_consistency(pairs)

    def _check_consistency(self, pairs):
        a2a = self._axis_to_attr()
        for axis, value in pairs:
            tgt_val = a2a.get(axis, None)
            if tgt_val is None:
                continue
            if tgt_val != value:
                raise ValueError(f"Inconsistent value for axis {axis}: {tgt_val} != {value}")

    def _decapsulate_shape(self, shape, axes):
        if len(shape) != len(axes):
            raise ValueError("Inconsistent shape and axes.")
        for axis, value in zip(axes, shape):
            if axis == "X":
                self.width = int(value)
            elif axis == "Y":
                self.height = int(value)
            elif axis == "Z":
                self.depth = int(value)
            elif axis == "C":
                self.n_channels = int(value)
            elif axis == "T":
                self.n_frames = int(value)

    def _parse_tif_data(self):
        self.dtype = np.dtype(self._tmp_tif_metadata.dtype).type
        self.axes = self._tmp_tif_metadata.axes
        self._decapsulate_shape(self._tmp_tif_metadata.shape, self.axes)