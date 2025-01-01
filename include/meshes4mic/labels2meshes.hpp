#ifndef LABELS_2_MESHES_HPP_INCLUDED
#define LABELS_2_MESHES_HPP_INCLUDED

#include <cstddef>
#include <cstdint>
#include <vector>
#include <array>

int other_function(int a, int b);

constexpr float edge_to_shift[12][3] = {
    {0.0, 0.0, 0.5},
    {0.0, 0.5, 1.0},
    {0.0, 1.0, 0.5},
    {0.0, 0.5, 0.0},
    {1.0, 0.0, 0.5},
    {1.0, 0.5, 1.0},
    {1.0, 1.0, 0.5},
    {1.0, 0.5, 0.0},
    {0.5, 0.0, 0.0},
    {0.5, 0.0, 1.0},
    {0.5, 1.0, 1.0},
    {0.5, 1.0, 0.0}
};

struct Vec3 {
    float x, y, z;
    Vec3() = default;
    Vec3(float _z, float _y, float _x): x(_x), y(_y), z(_z) {}
    Vec3(const Vec3&) = default;
};

struct Face {
    size_t v1, v2, v3;
    Face() = default;
    Face(size_t _v1, size_t _v2, size_t _v3): v1(_v1), v2(_v2), v3(_v3) {}
};

class MarchingCube;

/*
    x, y, z
    x+1, y, z
    x+1, y+1, z
    x, y+1, z
    x, y, z+1
    x+1, y, z+1
    x+1, y+1, z+1
    x, y+1, z+1
*/
class NeighborsZYX {
    /**
     * Processes the indices of a voxel's neighbors when the voxels grid is stored in a 1D array.
     */
    const MarchingCube& mc;
    size_t nbs[8] = {0};
    size_t slice = 0;

private:

    uint8_t layout_index();

public:

    NeighborsZYX() = default;
    NeighborsZYX(const MarchingCube& mc);

    uint8_t get_layout(size_t idx);
};

class MarchingCube {
    /// Binary mask containing the shapes
    const uint8_t* mask;
    /// Dimensions of the mask, including the padding/overlap
    const std::array<size_t, 3> shape;
    /// Physical calibration of a pixel.
    const std::array<double, 3> calibration;
    /// Stride on each axis.
    const std::array<size_t, 3> stride;
    /// List of faces of the mesh (triangles soup).
    std::vector<Face> faces;
    /// List of vertices of the mesh.
    std::vector<Vec3> vertices;

private:

    void build_faces(uint8_t layout, Vec3 v, std::array<size_t, 12>& i_buffer, std::vector<std::pair<bool, size_t>>& slice_buffer);

public:

    /**
     * @brief Construct a new Marching Cubes object.
     * 
     * @param m The binary mask containing the shapes.
     * @param dims The dimensions of the mask, including the padding/overlap.
     * @param calib Physical calibration of a pixel.
     * @param strd Stride on each axis.
     */
    MarchingCube(const uint8_t* m, const std::array<size_t, 3>& dims, const std::array<double, 3>& calib, const std::array<size_t, 3>& strd);

    void run();

    friend class NeighborsZYX;
};

#endif //LABELS_2_MESHES_HPP_INCLUDED
