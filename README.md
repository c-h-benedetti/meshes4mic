# Meshes4Mic

A Python package for efficient 3D mesh processing and visualization tailored to microscopy image analysis, bridging the gap between volumetric data and surface representation for biological research.
This package will be the backbone of a Blender addon and a Napari plugin.

## Mask/labels-map ↦ meshes

> Allows to transform a binary mask or a labels-map into a set of meshes.

- Images are read thourgh Dask, so they can be of any arbitrary size.
- Works whether images are isotropic or not.
- In the case of a labels-map, each individual label has its own buffer and so, their own mesh. Otherwise, everything is connected. 
The OME-TIF and OME-ZAR file formats are the only supported formats.
- Multi-channels and multi-timepoints stacks are handled.
- The output is an Alembic (.abc) file.
- Meshes can be optimized given their local curvature to minimize the number of vertices.
