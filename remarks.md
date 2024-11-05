## Remarks

| Locatation      |                                                                                                                                 |
| --------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| TOML            | Vérifier que rien ne manque dans le `pyproject.toml`.                                                                           |
| UML             | Marquer les classes virtuelles, les fonctions constantes, les méthodes et classes purement virtuelles ...                       |
| ImageProperties | Les attributs pourraient en fait être des méthodes décorées avec `@property`.                                                   |
| ImageProperties | Les unités devraient être check et converties plutôt qu'utilisées sous forme de string (avec `Pint`).                           |
| ImageProperties | Est-ce qu'il vaut mieux stocker les axes comme un tuple de string ou comme un string ?                                          |
| ImageProperties | Ne peut-on pas faire quelque chose de plus propre pour le `__str__` ?                                                           |
| All             | Migrer de `os.path.*` à `pathlib.Path`.                                                                                         |
| All             | En plus du TIF et du ZAR, quels seraient les autres formats (open) à gérer ?                                                    |
| All             | Il est vraiment temps de commencer à écrire les unit tests.                                                                     |
| TiffProperties  | Est-ce qu'avoir des attributs `tmp_*` est la façon la plus propre d'implémenter ?                                               |
| TiffProperties  | Check si toutes les clés sont toujours là.                                                                                      |
| TiffProperties  | Que faire si les valeurs rencontrées dans les fichiers sont corrompues ?                                                        |
| LTM_Worker      | Retourner l'objet `ImageProperties` sans garde-fou pourrait être à éviter.                                                      |
| LTM_Worker      | Il faudrait au moins vérifier un flag connu dans le fichier plutôt que juste l'extension.                                       |
| LTM_Worker      | Opti la méthode `get_bucket_size` pour voir si elle a des cas dégénérés.                                                        |
| LTM_Worker      | Ré-implémenter `get_bucket_size` pour que chaque zone tombe exactement une fois dans du non-overlap.                            |
| TiffToMeshes    | Est-ce que tout TIF a une `series[0]` et un `ome_metadata` ?                                                                    |
| ZarrToMeshes    | Comment convertir une image en OME-ZARR ? Est-ce que faire une appli JS en ligne qui remplace Bio-formats serait intéressante ? |
| All             | Écrire une description du fonctionnement technique pour ne pas ré-apprendre dans qqs mois.                                      |
| __init__        | Faut-il mettre quelque chose de particulier dans les `__init__` ?                                                               |
| setup.py        | ChatGPT proposait beaucoup plus d'instructions que ce qui a été conservé, qu'était-ce ?                                         |
| *.pyi           | Vaut-il mieux écrire la doc' dans les `*.pyi` ou dans le code C ?                                                               |
