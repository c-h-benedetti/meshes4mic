# Meshes4Mic

## List of features

### Mask/labels-map ↦ meshes

Allows to transform a binary mask or a labels-map of any arbitrary size, isotropic or not, into a set of meshes. In the case of a labels-map, each individual label has its own buffer and so, their own mesh. Otherwise, everything is connected. Dask is used in this function, which allows to use labeled map of any size, even things that wouldn't fit your memory. Images can be presented either in a monolithic TIFF, a collection of TIFF of in OME-ZAR (NGFF). We handle multi-channels and multi-timepoints stacks. The result is a parent folder (for the image) containing a sub-folder for each frame, itseld containing a sub-folder for each channel. Each of these folders contains a PLY file for each label contained within the image.

In the following example, our image is named `my-experiment.tif` and has 3 channels and 5 timepoints. Each folder `📁 T000I` represents a timepoint, each `📁 C000J` represents a channel and each `🕸️ L000000K.ply` represents a mesh over the label with the value `K`.

```
┌─ 📁 my-experiment-tif
│     ├─ 📁 T0001
│     │     ├─ 📁 C0001
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0002
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0003
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     ├─ 📁 T0002
│     │     ├─ 📁 C0001
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0002
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0003
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     ├─ 📁 T0003
│     │     ├─ 📁 C0001
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0002
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0003
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     ├─ 📁 T0004
│     │     ├─ 📁 C0001
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0002
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0003
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     ├─ 📁 T0005
│     │     ├─ 📁 C0001
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0002
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
│     │     ├─ 📁 C0003
│     │     │     ├─ 🕸️ L0000001.ply
│     │     │     ├─ 🕸️ L0000002.ply
│     │     │     ├─ 🕸️ L0000003.ply
│     │     │     └─ 🕸️ ...
```