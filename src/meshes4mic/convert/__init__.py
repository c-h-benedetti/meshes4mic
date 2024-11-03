from labels2meshes import LabelsToMesh
from m4mcore import test_fx

if __name__ == "__main__":
    filename = "/home/benedetti/Documents/meshes4mic/data/multi-channels.ome.tif"
    ltm = LabelsToMesh(filename, verbose=True)
    print(help(test_fx))
    print(test_fx(3, 4))