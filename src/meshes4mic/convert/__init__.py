from meshes4mic.convert.labels2meshes import LabelsToMeshes
from m4mcore import test_fx

if __name__ == "__main__":
    filename = "/home/benedetti/Documents/meshes4mic/data/multi-channels.ome.tif"
    ltm      = LabelsToMeshes(filename, verbose=True)
    print(test_fx(3, 4))