import os
import numpy as np
import math

# depth, height, width
configs = [
    ( 64, 128, 128),
    (128, 128, 128),
    (128,  64, 256),
    (128,  32, 128),
    (128, 128,  32),
    ( 32,  32,  32)
]

def make_bucket(depth, height, width, max_mem=64**3):
    ds = 1
    n_voxels = max_mem // ds
    base_size = int(round(n_voxels ** (1/3)))
    dz = min(depth, base_size)
    dy = min(height, n_voxels // (dz * base_size))
    dx = min(width, n_voxels // (dz * dy))
    while dz * dy * dx > n_voxels:
        if dx > 1:
            dx -= 1
        elif dy > 1:
            dy -= 1
        elif dz > 1:
            dz -= 1
    return (dz, dy, dx)

if __name__ == "__main__":
    for config in configs:
        print(make_bucket(*config))


"""

Le ratio du nombre de voxels le long des axes X ou Y versus l'axe Z doit tendre vers 1.0.
Cepenadnt, si ça n'est pas assez pour remplir la mémoire, les tailles en X et Y doivent être augmentées.
On ne va pas se baser sur le ratio physique mais sur le ratio de la grille pour calculer le ratio.
=> Ça peut changer.
Aussi, les buckets doivent être optimisés pour optimiser le nombre d'itérations.
Si on pouvait éviter d'avoir un dernier bucket de 3 pixels, ça serait un plus.

"""