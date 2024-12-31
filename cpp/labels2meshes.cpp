#include "meshes4mic/labels2meshes.hpp"
#include "meshes4mic/heller_mc.hpp"
#include <cstring>
#include <iostream>
#include <utility>
#include <vector>
#include <algorithm>
#include <array>

#include <string>
#include <fstream>


int other_function(int a, int b) {
    return a + b;
}

NeighborsZYX::NeighborsZYX(const MarchingCube& m): mc(m) {
    // Preprocessed multiplication height*width.
    this->slice = this->mc.shape[1] * this->mc.shape[1];
}

/*
    0: x, y, z
    1: x+1, y, z
    2: x+1, y+1, z
    3: x, y+1, z
    4: x, y, z+1
    5: x+1, y, z+1
    6: x+1, y+1, z+1
    7: x, y+1, z+1
*/
uint8_t NeighborsZYX::get_layout(size_t idx) {
    this->nbs[0] = idx;
    this->nbs[1] = idx + this->mc.stride[2];
    this->nbs[2] = idx + this->mc.stride[2] + this->mc.stride[1] * this->mc.shape[2];
    this->nbs[3] = idx + this->mc.stride[1] * this->mc.shape[2];
    this->nbs[4] = idx + this->mc.stride[0] * this->slice;
    this->nbs[5] = idx + this->mc.stride[2] + this->mc.stride[0] * this->slice;
    this->nbs[6] = idx + this->mc.stride[2] + this->mc.stride[1] * this->mc.shape[2] + this->mc.stride[0] * this->slice;
    this->nbs[7] = idx + this->mc.stride[1] * this->mc.shape[2] + this->mc.stride[0] * this->slice;
    return this->layout_index();
}

uint8_t NeighborsZYX::layout_index() {
    uint8_t layout = 0;
    for (uint8_t i = 0 ; i < 8 ; i++) {
        layout |= (this->mc.mask[this->nbs[i]] > 0 ? 1 : 0) << i;
    }
    return layout;
}

MarchingCube::MarchingCube(const uint8_t* m, const std::array<size_t, 3>& dims, const std::array<double, 3>& calib, const std::array<size_t, 3>& strd): 
    mask(m),
    shape(dims),
    calibration(calib),
    stride(strd)
{}

void export_to_obj(const std::string& filename, const std::vector<Vec3>& vertices, const std::vector<Face>& faces) {
    std::ofstream obj_file(filename);

    if (!obj_file.is_open()) {
        std::cerr << "Error: Unable to open file \"" << filename << "\" for writing." << std::endl;
        return;
    }

    // Write vertices
    for (const auto& vertex : vertices) {
        obj_file << "v " << vertex.x << " " << vertex.y << " " << vertex.z << "\n";
    }

    // Write faces
    for (const auto& face : faces) {
        obj_file << "f " << (face.v1 + 1) << " " << (face.v2 + 1) << " " << (face.v3 + 1) << "\n";
    }

    obj_file.close();
    std::cout << "Mesh exported to \"" << filename << "\" successfully." << std::endl;
}

void MarchingCube::run() {
    const size_t depth = this->shape[2], height = this->shape[1], width = this->shape[0];
    NeighborsZYX n(*this);
    size_t idx_z = 0, idx_y = 0, idx = 0;
    // Allocated memory for the vertices that we create at each iteration.
    std::array<Vec3, 12> v_buffer;
    // Allocated memory for the indices of the vertices that we create at each iteration.
    std::array<size_t, 12> i_buffer;
    // Indices of vertices created at the previous slice (reseted when we change of Z).
    std::vector<std::pair<bool, size_t>> slice_buffer(3*2*height*width, std::make_pair(false, 0));
    // std::fill(slice_buffer.begin(), slice_buffer.end(), std::make_pair(false, 0));

    // The data is padded with the amount of stride on each axis.
    for (size_t z = this->stride[0] ; z < depth - this->stride[0] ; z+=this->stride[0]) {
        idx_z = z * width * height;
        for (size_t y = this->stride[1] ; y < height - this->stride[1] ; y+=this->stride[1]) {
            idx_y = idx_z + y * width;
            for (size_t x = this->stride[2] ; x < width - this->stride[2] ; x+=this->stride[2]) {
                idx = idx_y + x;
                this->build_faces(n.get_layout(idx), Vec3(z, y, x), v_buffer, i_buffer, slice_buffer);
            }
        }
        std::copy(slice_buffer.begin() + 2 * height * width, slice_buffer.begin() + 3 * height * width, slice_buffer.begin());
        std::fill(slice_buffer.begin() + height * width, slice_buffer.end(), std::make_pair(false, 0));
    }
    export_to_obj("/home/benedetti/tri-soup.obj", this->vertices, this->faces);
}

void MarchingCube::build_faces(uint8_t layout, Vec3 v, std::array<Vec3, 12>& v_buffer, std::array<size_t, 12>& i_buffer, std::vector<std::pair<bool, size_t>>& slice_buffer) {
    const size_t height = this->shape[1], width = this->shape[0];
    uint16_t edge = edges_array[layout];
    size_t v_id = 0;
    Vec3 vtx;
    if (edge == 0) { return; }
    for (uint8_t i = 0 ; i < 12 ; i++) {
        vtx = Vec3(
            (v.z + edge_to_shift[i][0] * this->stride[0]) * this->calibration[0], 
            (v.y + edge_to_shift[i][1] * this->stride[1]) * this->calibration[1], 
            (v.x + edge_to_shift[i][2] * this->stride[2]) * this->calibration[2]
        );
        v_id = static_cast<size_t>(2.0 * edge_to_shift[i][0]) * height * width + 
               static_cast<size_t>(((v.y + edge_to_shift[i][1] * this->stride[1]) - 0.5) * 2.0) * width + 
               static_cast<size_t>(v.x + edge_to_shift[i][2] * this->stride[2]);
        if (!slice_buffer[v_id].first) { // The vertex doesn't exists.
            
            this->vertices.push_back(vtx);
            slice_buffer[v_id] = {true, this->vertices.size() - 1};
        }
        i_buffer[i] = slice_buffer[v_id].second;
    }
    for (size_t i = 0 ; i < triangles_array[layout][0] ; i++) {
        this->faces.push_back(
            Face(
                i_buffer[triangles_array[layout][1+i*3]],
                i_buffer[triangles_array[layout][1+i*3+1]],
                i_buffer[triangles_array[layout][1+i*3+2]]
            )
        );
    }
}


/*

void MarchingCube::build_faces(uint8_t layout, Vec3 v, std::array<Vec3, 12>& v_buffer, std::array<size_t, 12>& i_buffer, std::vector<std::pair<bool, size_t>>& slice_buffer) {
    const size_t height = this->shape[1], width = this->shape[0];
    uint16_t edge = edges_array[layout];
    size_t v_id = 0;
    Vec3 vtx;
    if (edge == 0) { return; }
    for (uint8_t i = 0 ; i < 12 ; i++) {
        // if ((edge & (1 << i)) == 0) { continue; } // Edge not intersected => no vertex to create.
        v_id = static_cast<size_t>(2.0 * edge_to_shift[i][0]) * height * width + 
               static_cast<size_t>(v.y + edge_to_shift[i][1] * this->stride[1]) * width + 
               static_cast<size_t>(v.x + edge_to_shift[i][2] * this->stride[2]);
        if (!slice_buffer[v_id].first) { // The vertex doesn't exists.
            vtx = Vec3(
                (v.z + edge_to_shift[i][0] * this->stride[0]) * this->calibration[0], 
                (v.y + edge_to_shift[i][1] * this->stride[1]) * this->calibration[1], 
                (v.x + edge_to_shift[i][2] * this->stride[2]) * this->calibration[2]
            );
            this->vertices.push_back(vtx);
            slice_buffer[v_id] = {true, this->vertices.size() - 1};
        }
        i_buffer[i] = slice_buffer[v_id].second;
    }
    for (size_t i = 0 ; i < triangles_array[layout][0] ; i++) {
        this->faces.push_back(
            Face(
                i_buffer[triangles_array[layout][1+i*3]],
                i_buffer[triangles_array[layout][1+i*3+1]],
                i_buffer[triangles_array[layout][1+i*3+2]]
            )
        );
    }
}

*/