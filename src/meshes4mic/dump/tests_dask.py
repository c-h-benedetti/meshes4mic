import os
import dask.array as da
import tifffile
import re
import psutil
import xml.etree.ElementTree as ET


def dump():
    # Utilisation de tifffile pour lire les métadonnées et la structure du fichier
    with tifffile.TiffFile(filename) as tif:
        # Créer un Dask Array à partir de chaque page du TIFF (fonctionne pour des stacks 3D ou multi-pages)
        dask_array = da.from_array(tif.asarray(), chunks='auto')  # chunks peut aussi être spécifié manuellement

    # Afficher quelques informations
    print(dask_array.shape)
    print(dask_array.dtype)

    # Utiliser le Dask Array pour traitement
    # Exemple: calculer la moyenne de chaque frame (paresseusement, pour ne pas tout charger en mémoire)
    mean_per_frame = dask_array.mean(axis=(1, 2))  # pour une image 3D

    # Exécuter les calculs avec .compute()
    result = mean_per_frame.compute()
    print(result)
