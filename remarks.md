## Marching-cube

- Dans le générateur, mettre directement les tuples avec les triangles plutôt que les indices de edges.
- La liste d'indices de edges (pour construire l'index 12 bits) peut être retrouvée depuis la liste de triangles.
- Écire des tests pour voir si le résultat produit est correct.
  - Chaque array de transformation doit avoir exactement une fois chaque index.
  - L'array de sortie doit avoir 256 slots et pas de doublons.
- Comment sont connectés les triangles produits, on ne veut pas de triangle soup. (Half-efges?)
  On doit pouvoir retrouver les indices des vertices déjà créés, sans créer un buffer de la taille de l'input si possible.
- Chaque version du marching cube pourra avoir son générateur Python (si possible).
- Comment orienter les normales selon les faces ? Faut-il les preprocess aussi?
- Ajouter des paramètres pour output un HPP.
- Est-ce qu'il serait plus rapide de générer la triangles soup et de la ranger après ?
- Changer le type du tableau "intersected edges":
  ([], [])  -->  {(): [(), (), ()]}
  Tuple des indices de vertices vers liste de triangles.

#### Milestones:

- [X] Implémenter le marching-cube qui output une triangles-soup à partir d'un masque binaire qui entre en RAM.
      Cette méthode utilise le triangles-set de base (Heller, Bourke).

- [ ] Modifier l'implémentation pour créer un vrai mesh plutôt qu'une triangles-soup.
      Utiliser des half-edges ou une autre structure.

- [ ] Pouvoir faire des meshes par dessus des labels plutôt que de simples masques.

- [ ] Pouvoir faire des meshes sur des label-maps qui ne fit pas en RAM.

- [ ] Ajouter des tables de vertices plus élaborées.

## TO-DO

- [ ] Vérifier que rien ne manque dans le `pyproject.toml`.
- [ ] Est-ce qu'il serait possible de faire un projet sans `setup.py` avec PyBind11 ?
- [ ] Marquer les classes virtuelles, les fonctions constantes, les méthodes et classes purement virtuelles ...
- [ ] Les attributs pourraient en fait être des méthodes décorées avec `@property`.
- [ ] Les unités devraient être check et converties plutôt qu'utilisées sous forme de string (avec `Pint`).
- [ ] Est-ce qu'il vaut mieux stocker les axes comme un tuple de string ou comme un string ?
- [ ] Ne peut-on pas faire quelque chose de plus propre pour le `__str__` ?
- [ ] Migrer de `os.path.*` à `pathlib.Path`.
- [ ] En plus du TIF et du ZAR, quels seraient les autres formats (open) à gérer ?
- [ ] Il est vraiment temps de commencer à écrire les unit tests.
- [ ] Est-ce qu'avoir des attributs `tmp_*` est la façon la plus propre d'implémenter ?
- [ ] Check si toutes les clés sont toujours là.
- [ ] Que faire si les valeurs rencontrées dans les fichiers sont corrompues ?
- [ ] Retourner l'objet `ImageProperties` sans garde-fou pourrait être à éviter.
- [ ] Il faudrait au moins vérifier un flag connu dans le fichier plutôt que juste l'extension.
- [ ] Opti la méthode `get_bucket_size` pour voir si elle a des cas dégénérés.
- [ ] Ré-implémenter `get_bucket_size` pour que chaque zone tombe exactement une fois dans du non-overlap.
- [ ] Est-ce que tout TIF a une `series[0]` et un `ome_metadata` ?
- [ ] Comment convertir une image en OME-ZARR ? Est-ce que faire une appli JS en ligne qui remplace Bio-formats serait intéressante 
- [ ] Écrire une description du fonctionnement technique pour ne pas ré-apprendre dans qqs mois.
- [ ] Faut-il mettre quelque chose de particulier dans les `__init__` ?
- [ ] ChatGPT proposait beaucoup plus d'instructions que ce qui a été conservé, qu'était-ce ?
- [ ] Vaut-il mieux écrire la doc' dans les `*.pyi` ou dans le code C ?


## Implémentation

- Il est possible de remplacer dask qu'on utilise en fait très peu par une combinaison de tifffile et de zar, voir `zar_store_and_tif.py`.

- Dans un premier temps, on va faire un marching-cube mono-channel et mono-frame avec une implémentation instinctive.
  Pas de multi-threading ni rien, pas même de buckets, on va expérimenter sur une image qui entre totalement en RAM pour pouvoir l'avoir entièrement.
  Le binding Python ne sera là que pour pouvoir utiliser tifffile.

- La classe de meshing doit être complètement isolée de la notion de multi-threading.
  On lui donne simplement le bucket d'entrée et l'endroit où la sortie doit être écrite.

- Liste de workflows dans lesquels le `mesher` doit pouvoir s'intégrer:
    - On implémente une random-forest.
      On a donc de tous petits buckets pour pouvoir stocker toutes les features à toutes les résolutions requises.
      Le `mesher` doit alors pouvoir consommer les buckets d'output de cet algo et construire le mesh à la volée.
      Peut-être qu'il va même falloir ajouter la possibilité d'insérer des filtres entre les étapes pour virer les pixels isolés.
      Dans ce cas, on peut avoir la moitié des threads dédiés à l'exécution de la random-forest et le reste pour le meshing.
      Ça ferait du double-buffering, un des buffers est entrain d'être consommé pendant que l'autre se fait remplir.

    - Quand on veut simplement ouvrir une image en tant que mesh, tous les threads doivent être consacrés au meshing.