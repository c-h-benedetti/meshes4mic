import tifffile
import numpy as np

def padded_shape(img, pad_size):
    return tuple(np.array(img.shape) + 2 * pad_size)

if __name__ == "__main__":
    filename = "/home/benedetti/Documents/meshes4mic/data/3d-stack.tif"
    imIn = tifffile.imread(filename)
    print(imIn.shape)
    pad_size = (1, 2, 2)
    imOut = np.pad(imIn, ((1, 1), (2, 2), (2, 2)), mode='constant', constant_values=0)
    print(imOut.shape)
    tifffile.imwrite("/home/benedetti/Documents/meshes4mic/data/3d-stack-padded.tif", imOut)