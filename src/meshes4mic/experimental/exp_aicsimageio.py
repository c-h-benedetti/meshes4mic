from aicsimageio import AICSImage
import tifffile as tif

def experiment_aicsimageio():
    DATA_ROOT = "/home/benedetti/Documents/meshes4mic/data/calibrated_synthetic/"

    # Load the image
    img = AICSImage("path_to_your_image_file")

    # Access dimensions
    dims = img.dims  # e.g., 'S', 'T', 'C', 'Z', 'Y', 'X'

    # Access physical pixel sizes
    pixel_sizes = img.physical_pixel_sizes  # e.g., {'X': 0.1, 'Y': 0.1, 'Z': 0.3, 'T': 1.0}

    # Number of channels
    num_channels = img.get_dimensions('C')

    # Number of frames (time points)
    num_frames = img.get_dimensions('T')

def experimental_tifffile():
    data_path = "/home/benedetti/Documents/meshes4mic/data/calibrated_synthetic/5d_hyperstack.tif"
    with tif.TiffFile(data_path) as t:
        img = t.asarray()
        print(img.shape)
        dims = img.shape
        print(dims)

if __name__ == "__main__":
    experimental_tifffile()