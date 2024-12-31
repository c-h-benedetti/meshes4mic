from meshes4mic.convert.labels2meshes import LabelsToMeshes
from m4mcore.distances import test_fx
from m4mcore.flux import other_function
from m4mcore.surfaces import MarchingCube
import numpy as np
import tifffile

if __name__ == "__main__":
    data_path = "/home/benedetti/Documents/meshes4mic/data/basic_mask.tif"
    # mask = np.zeros((2048, 2048, 1024), dtype=np.uint8)
    mask = tifffile.imread(data_path)
    stride = (1, 1, 1) # ZYX
    padded_img = np.pad(
        mask, 
        (
            (stride[0], stride[0]), 
            (stride[1], stride[1]), 
            (stride[2], stride[2])), 
        mode='constant', 
        constant_values=0
    )
    print(padded_img.shape)
    mc = MarchingCube(padded_img, padded_img.shape, (0.3333, 0.3333, 0.3333), stride)
    mc.run()