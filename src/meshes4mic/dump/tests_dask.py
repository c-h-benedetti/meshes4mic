import dask.array as da
import tifffile
from tqdm import tqdm
import xml.etree.ElementTree as ET
import numpy as np

filename = "/home/benedetti/Documents/meshes4mic/data/multi-channels.ome.tif"

from concurrent.futures import ThreadPoolExecutor, as_completed
import tifffile
import dask.array as da

def make_random_boxes(shape, n_boxes):
    """
    Produces an array of random bounding boxes.
    It expects a 3D shape (Z, Y, X) and the number of boxes to generate.
    """
    boxes = np.zeros((n_boxes, 6), dtype=np.uint64)
    for b in range(n_boxes):
        z_start = np.random.randint(0, shape[0])
        z_end = np.random.randint(z_start, shape[0]+1)
        y_start = np.random.randint(0, shape[1])
        y_end = np.random.randint(y_start, shape[1]+1)
        x_start = np.random.randint(0, shape[2])
        x_end = np.random.randint(x_start, shape[2]+1)
        boxes[b, :] = z_start, z_end, y_start, y_end, x_start, x_end
    return boxes

def process_chunk(chunk):
    """
    Launch some process over a chunk of data, to measure the running time.
    """
    result = np.median(chunk)
    return result

def measure_run_time(n_iters=10000):
    with tifffile.TiffFile(filename) as tif:
        dask_array = da.from_array(tif.asarray())

    depth, n_channels, height, width = dask_array.shape
    bounding_boxes = make_random_boxes((depth, height, width), n_iters)

    # Boxes properties
    print((depth, n_channels, height, width))
    for i in range(len(bounding_boxes)):
        z1, z2, y1, y2, x1, x2 = bounding_boxes[i]
        ttl = (z2 - z1) * (y2 - y1) * (x2 - x1)
        print(bounding_boxes[i], "->", ttl)

    # Launching the process
    result = []
    for i in tqdm(range(len(bounding_boxes))):
        c = np.random.randint(0, n_channels)
        z1, z2, y1, y2, x1, x2 = bounding_boxes[i]
        ttl = (z2 - z1) * (y2 - y1) * (x2 - x1)
        if ttl == 0:
            continue
        chunk = dask_array[z1:z2, c, y1:y2, x1:x2].compute()
        result.append(float(process_chunk(chunk)))

    print(">>>", result)


def process_image_multi_threads(data_path, n_workers=4, n_iters=10000):
    # Declare the dask array.
    with tifffile.TiffFile(data_path) as tif:
        dask_array = da.from_array(tif.asarray())

    # Prepare the output buffer.
    depth, n_channels, height, width = dask_array.shape
    bounding_boxes = make_random_boxes((depth, height, width), n_iters)
    results = []

    # Create the threads pool.
    with ThreadPoolExecutor(max_workers=n_workers) as executor:
        # Soumettre chaque chunk à un thread
        futures = {
            executor.submit(process_chunk, dask_array[i, j, :, :].compute()): (i, j)
            for i in range(dask_array.shape[0])   # Z
            for j in range(dask_array.shape[1])   # C
        }
        
        # Récupérer les résultats au fur et à mesure
        for future in as_completed(futures):
            chunk_result = future.result()
            results.append(chunk_result)

    print(">>>", results)


if __name__ == "__main__":
    measure_run_time()


"""

∙ Il faut que la taille d'un bucket soit assez grande pour que l'overhead des threads ne soit pas trop grand.
  Même remarque pour l'overhead de Dask.

∙ S'il y a N threads, chaque thread va traiter 1/Nème de chaque chunk.

∙ À chaque tour de boucle, il faut donc attendre que chaque thread ait terminé sa partie et soit passé en mode idle.
  Ce n'est qu'à ce moment-là qu'on peut charger un nouveau chunk.
  On fait ça jusqu'à ce qu'on ait traité tous les chunks.
  Chaque chunk va donc devoir être divisé en N parties égales.

∙ Il va falloir un système de wait solide pour éviter les deadlocks.

∙ Dans le futur, il faudra trouver un algo qui permet de choisir le nombre de threads (entre 1 et max threads) pour minimiser l'overhead.
  Il y aura certainement un gros overhead si les sous-chunks sont trop petits.

"""