############################################################################################
#  This piece of code is used to generate the marching-cube LUTs (Paul BOURKE's version).  #
#  --> https://paulbourke.net/geometry/polygonise/                                         #
#  We start from the basic cases and edit them (rotations and symetry) to build others.    #
#  The execution of this code results in the creation of a ".hpp" file.                    #
#  The tables are constexpr in them.                                                       # 
#  See the file "data/edge-cases.blend" for the indices of vertices and edges.             #
#  --- By: Clément H. BENEDETTI                                                            #
############################################################################################

import os

"""
Tables describing the new index of each vertex after a rotation around the X, Y or Z axis.
The tables are accessed with the indices of original vertices. (== _V_R_X[old_index] --> index_after_rotation).
Only one rotation direction is implemented, it takes 4 iterations to cancel a move.
These arrays will allow to make the different versions of the "intersected edges" table.
The "edge rotation" arrays behave of the exact same way, and so do the "symetry" ones.
"""
_VERTEX_ROTATION_X = [
    4,
    5,
    1,
    0,
    7,
    6,
    2,
    3
]

_EDGE_ROTATION_X = [
    4,
    9,
    0,
    8,
    6,
    10,
    2,
    11,
    7,
    5,
    1,
    3
]

_VERTEX_ROTATION_Y = [
    4,
    0,
    3,
    7,
    5,
    1,
    2,
    6
]

_EDGE_ROTATION_Y = [
    8,
    3,
    11,
    7,
    9,
    1,
    10,
    5,
    4,
    0,
    2,
    6
]

_VERTEX_ROTATION_Z = [
    1,
    2,
    3,
    0,
    5,
    6,
    7,
    4
]

_EDGE_ROTATION_Z = [
    1,
    2,
    3,
    0,
    5,
    6,
    7,
    4,
    9,
    10,
    11,
    8
]

_VERTEX_SYMETRY_X = [
    1,
    0,
    3,
    2,
    5,
    4,
    7,
    6
]

_EDGE_SYMETRY_X = [
    0,
    3,
    2,
    1,
    4,
    7,
    6,
    5,
    9,
    8,
    11,
    10
]

_VERTEX_SYMETRY_Y = [
    3,
    2,
    1,
    0,
    7,
    6,
    5,
    4
]

_EDGE_SYMETRY_Y = [
    2,
    1,
    0,
    3,
    6,
    5,
    4,
    7,
    11,
    10,
    9,
    8
]

_VERTEX_SYMETRY_Z = [
    4,
    5,
    6,
    7,
    0,
    1,
    2,
    3
]

_EDGE_SYMETRY_Z = [
    4,
    5,
    6,
    7,
    0,
    1,
    2,
    3,
    8,
    9,
    10,
    11
]

# {(tuple of vertices in the volume): [(3 indices of intersected edges forming a triangle)]}
_VERTICES_TO_TRIANGLES = {
    ()          : [],
    (0,)        : [(0, 3, 8)],
    (0, 4)      : [(0, 3, 4), (3, 4, 7)],
    (0, 7)      : [(0, 8, 3), (6, 7, 11)],
    (0, 6)      : [(5, 6, 10), (0, 8, 3)],
    (0, 3, 4)   : [(0, 2, 4), (2, 4, 7), (2, 7, 11)],
    (0, 3, 5)   : [(0, 2, 8), (8, 11, 2), (4, 5, 9)],
    (1, 3, 4)   : [(2, 3, 11), (0, 1, 9), (4, 7, 8)],
    (0, 1, 3, 4): [(1, 2, 9), (2, 4, 9), (2, 11, 4), (11, 7, 4)],
    (0, 1, 3, 6): [(1, 2, 11), (1, 11, 9), (8, 9, 11), (5, 6, 10)],
    (0, 3, 5, 6): [(4, 6, 10), (4, 10, 9), (0, 2, 8), (2, 8, 11)],
    (1, 3, 4, 6): [(5, 6, 10), (0, 1, 9), (2, 3, 11), (4, 7, 8)],
    (0, 1, 2, 3): [(8, 9, 10), (8, 10, 11)],
    (1, 2, 3, 5): [(3, 10, 11), (3, 4, 10), (0, 3, 4), (4, 5, 10)]
}

def complementary_vertices():
    """
    Triangles for 0 positive vertex == triangles for 8 positive vertices,
    Triangles for 1 positive vertex == triangles for 7 positive vertices,
    ...
    Uses the '_VERTICES_TO_TRIANGLES' dictionary that contains triangles up to 4 positive vertices,
    and build the cases for 5, 6, 7 and 8 positive vertices.
    Only the normals should point in opposite directions.
    """
    all_set = set(range(8))
    full_set = _VERTICES_TO_TRIANGLES.copy()
    for vertices, triangles in _VERTICES_TO_TRIANGLES.items():
        negative = all_set - set(vertices)
        full_set[tuple(negative)] = triangles.copy()
    return full_set

def transform_tuple(t, T, n_iters):
    t2 = t
    for _ in range(n_iters):
        t2 = tuple([T[i] for i in t2])
    return t2

def transform_vertex(t, T, n_iters=0):
    return transform_tuple(t, T, n_iters)

def transform_triangles(ts, T, n_iters=0):
    return [transform_tuple(t, T, n_iters) for t in ts]

def ints_to_bits(buffer):
    layout = 0
    for b in buffer:
        layout |= (1<<b)
    return layout

def complete_triangles_set():
    combis_verbose = dict()
    for vertices, triangles in complementary_vertices().items():
        v = vertices
        e = triangles.copy()
        for rx in range(4):
            for ry in range(4):
                for rz in range(4):
                    for sx in range(2):
                        for sy in range(2):
                            for sz in range(2):
                                v = transform_vertex(v, _VERTEX_ROTATION_X, rx)
                                v = transform_vertex(v, _VERTEX_ROTATION_Y, ry)
                                v = transform_vertex(v, _VERTEX_ROTATION_Z, rz)
                                v = transform_vertex(v, _VERTEX_SYMETRY_X, sx)
                                v = transform_vertex(v, _VERTEX_SYMETRY_Y, sy)
                                v = transform_vertex(v, _VERTEX_SYMETRY_Z, sz)

                                e = transform_triangles(e, _EDGE_ROTATION_X, rx)
                                e = transform_triangles(e, _EDGE_ROTATION_Y, ry)
                                e = transform_triangles(e, _EDGE_ROTATION_Z, rz)
                                e = transform_triangles(e, _EDGE_SYMETRY_X, sx)
                                e = transform_triangles(e, _EDGE_SYMETRY_Y, sy)
                                e = transform_triangles(e, _EDGE_SYMETRY_Z, sz)

                                key = tuple(set(v))
                                if key in combis_verbose:
                                    continue
                                combis_verbose[key] = e
    return combis_verbose

def flatten(xss):
    return [x for xs in xss for x in xs]

def create_edges_table(all_triangles):
    lines = ["" for _ in range(256)]
    for vertices, triangles_list in all_triangles.items():
        v = set(vertices)
        e = set(flatten(triangles_list))
        rank = ints_to_bits(v)
        bits = reversed(['1' if i in e else '0' for i in range(16)])
        literal = "    0b" + "".join(bits)
        lines[rank] = literal
    return lines

def edges_table_as_c_array(edges_array):
    return "constexpr uint16_t edges_array[256] = {\n" + ",\n".join(edges_array) + "\n};"

def create_triangles_table(all_triangles):
    """
    The first number corresponds to the number of triangles on this line.
    """
    lines = ["" for _ in range(256)]
    for vertices, triangles_list in all_triangles.items():
        v = set(vertices)
        e = flatten(triangles_list)
        e += [0 for _ in range(15-len(e))]
        rank = ints_to_bits(v)
        indices = [len(triangles_list)] + e
        lines[rank] = indices
    return lines

def triangles_table_as_c_array(triangles_array):
    litteral = "constexpr uint16_t triangles_array[256][16] = {\n"
    blocks = []
    for line in triangles_array:
        blocks.append("    {" + ", ".join([str(l) for l in line]) + "}")
    litteral += ",\n".join(blocks)
    litteral += "\n};"
    return litteral

if __name__ == "__main__":
    destination = os.path.abspath(__file__)
    for _ in range(4):
        destination = os.path.dirname(destination)
    destination = os.path.join(destination, "include", "meshes4mic", "heller_mc.hpp")
    
    all_triangles = complete_triangles_set()

    edges_array  = create_edges_table(all_triangles)
    edges_array  = edges_table_as_c_array(edges_array)

    triangles_list = create_triangles_table(all_triangles)
    triangles_list = triangles_table_as_c_array(triangles_list)

    with open(destination, 'w') as f:
        f.write("#ifndef HELLER_BOURKE_HPP_INCLUDED\n")
        f.write("#define HELLER_BOURKE_HPP_INCLUDED\n")
        f.write("\n")
        f.write("// This file was automatically generated using the 'helper/gen_heller_mc_table.py' script.\n")
        f.write("\n")
        f.write(edges_array)
        f.write("\n\n")
        f.write(triangles_list)
        f.write("\n")
        f.write("#endif //HELLER_BOURKE_HPP_INCLUDED")

# TESTS:
# - [X] Test that in vertices transfo, each index between 0 and 7 is present exactly once.
# - [X] Test that in edges transfo, each index between 0 and 11 is present exactly once.
# - [X] Test that 4 rotations lead back to the initial state.
# - [X] Test that 2 symetries lead back to the initial state.
# - [X] In '_VERTICES_TO_TRIANGLES', vertices indices appear only once.
# - [X] In '_VERTICES_TO_TRIANGLES', edges indices appear only once per tuple.
# - [X] '_VERTICES_TO_TRIANGLES' contains tuple of length up to 4 and point to tuples of length 3.
# - [ ] Test that in the 'complete_triangles_set', there are 256 items.

# TO DO:
# - [ ] Add the table of normals per triangle.
# - [ ] Pouvoir output un ".hpp" à partir de ce fichier.

def test_vertices_content():
    elements = [_VERTEX_ROTATION_X, _VERTEX_ROTATION_Y, _VERTEX_ROTATION_Z,
                _VERTEX_SYMETRY_X , _VERTEX_SYMETRY_Y , _VERTEX_SYMETRY_Z]
    for e in elements:
        target = set(range(8))
        source = set(e)
        assert source == target

def test_edges_content():
    elements = [_EDGE_ROTATION_X, _EDGE_ROTATION_Y, _EDGE_ROTATION_Z,
                _EDGE_SYMETRY_X , _EDGE_SYMETRY_Y , _EDGE_SYMETRY_Z]
    for e in elements:
        target = set(range(12))
        source = set(e)
        assert source == target

def test_4_rotations():
    elements = [_VERTEX_ROTATION_X, _VERTEX_ROTATION_Y, _VERTEX_ROTATION_Z,
                _EDGE_ROTATION_X  , _EDGE_ROTATION_Y  , _EDGE_ROTATION_Z]
    for e in elements:
        target = tuple(range(len(e)))
        source = transform_tuple(target, e, 4)
        assert target == source

def test_2_symetries():
    elements = [_VERTEX_SYMETRY_X, _VERTEX_SYMETRY_Y, _VERTEX_SYMETRY_Z,
                _EDGE_SYMETRY_X  , _EDGE_SYMETRY_Y  , _EDGE_SYMETRY_Z]
    for e in elements:
        target = tuple(range(len(e)))
        source = transform_tuple(target, e, 2)
        assert target == source

def test_unique_indices():
    for vertices in _VERTICES_TO_TRIANGLES.keys():
        s1 = len(vertices)
        s2 = len(set(vertices))
        assert s2 <= 4
        assert s1 == s2
        if s1 > 0:
            assert min(vertices) >= 0
            assert max(vertices) <= 7
    
    for t_list in _VERTICES_TO_TRIANGLES.values():
        for triangle in t_list:
            s1 = len(triangle)
            s2 = len(set(triangle))
            assert s1 == s2
            assert s2 == 3
            if s1 > 0:
                assert min(triangle) >= 0
                assert max(triangle) <= 11

def test_n_combinations():
    all_combis = complete_triangles_set()
    assert len(all_combis) == 256