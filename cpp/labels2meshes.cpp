#include <cstring>
#include "meshes4mic/labels2meshes.hpp"
#include "meshes4mic/heller_mc.hpp"
#include <iostream>


#include <string>
#include <fstream>

void exportToOBJ(const std::vector<Face>& faces, const std::string& filename) {
    std::ofstream file(filename);
    
    if (!file.is_open()) {
        std::cerr << "Erreur : Impossible d'ouvrir le fichier " << filename << std::endl;
        return;
    }

    // Écriture des sommets (vertices)
    for (const auto& face : faces) {
        file << "v " << face.v1.x << " " << face.v1.y << " " << face.v1.z << "\n";
        file << "v " << face.v2.x << " " << face.v2.y << " " << face.v2.z << "\n";
        file << "v " << face.v3.x << " " << face.v3.y << " " << face.v3.z << "\n";
    }

    // Écriture des faces
    int vertexIndex = 1; // Les indices de sommets commencent à 1 dans les fichiers OBJ
    for (size_t i = 0; i < faces.size(); ++i) {
        file << "f " << vertexIndex << " " << (vertexIndex + 1) << " " << (vertexIndex + 2) << "\n";
        vertexIndex += 3; // Chaque face utilise 3 sommets
    }

    file.close();
    std::cout << "Fichier OBJ exporté avec succès : " << filename << std::endl;
}

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
void NeighborsZYX::set_index(size_t idx) {
    this->nbs[0] = idx;
    this->nbs[1] = idx + this->mc.stride[2];
    this->nbs[2] = idx + this->mc.stride[2] + this->mc.stride[1] * this->mc.shape[2];
    this->nbs[3] = idx + this->mc.stride[1] * this->mc.shape[2];
    this->nbs[4] = idx + this->mc.stride[0] * this->slice;
    this->nbs[5] = idx + this->mc.stride[2] + this->mc.stride[0] * this->slice;
    this->nbs[6] = idx + this->mc.stride[2] + this->mc.stride[1] * this->mc.shape[2] + this->mc.stride[0] * this->slice;
    this->nbs[7] = idx + this->mc.stride[1] * this->mc.shape[2] + this->mc.stride[0] * this->slice;
    this->layout_index();
}

void NeighborsZYX::layout_index() {
    this->layout = 0;
    for (uint8_t i = 0 ; i < 8 ; i++) {
        this->layout |= (this->mc.mask[this->nbs[i]] > 0 ? 1 : 0) << i;
    }
}

MarchingCube::MarchingCube(const uint8_t* m, const std::array<size_t, 3>& dims, const std::array<double, 3>& calib, const std::array<size_t, 3>& strd): 
    mask(m),
    shape(dims),
    calibration(calib),
    stride(strd)
{}

void MarchingCube::run() {
    const size_t depth = this->shape[2], height = this->shape[1], width = this->shape[0];
    NeighborsZYX n(*this);
    size_t idx_z = 0, idx_y = 0, idx = 0;
    std::array<Vec3, 12> v_buffer;

    // The data is padded with the amount of stride on each axis.
    for (size_t z = this->stride[0] ; z < depth - this->stride[0] ; z+=this->stride[0]) {
        idx_z = z * width * height;
        for (size_t y = this->stride[1] ; y < height - this->stride[1] ; y+=this->stride[1]) {
            idx_y = idx_z + y * width;
            for (size_t x = this->stride[2] ; x < width - this->stride[2] ; x+=this->stride[0]) {
                idx = idx_y + x;
                n.set_index(idx);
                this->build_faces(n.layout, z, y, x, v_buffer);
            }
        }
    }
    exportToOBJ(this->faces, "/home/benedetti/tri-soup.obj");
}

void MarchingCube::build_faces(uint8_t layout, size_t z, size_t y, size_t x, std::array<Vec3, 12>& v_buffer) {
    uint16_t edge = edges_array[layout];
    if (edge == 0) { return; }
    for (uint8_t i = 0 ; i < 12 ; i++) {
        v_buffer[i] = (edge & 1<<i) ? Vec3(
            ((float)z+edge_to_shift[i][0]*this->stride[0])*this->calibration[0], 
            ((float)y+edge_to_shift[i][1]*this->stride[1])*this->calibration[1], 
            ((float)x+edge_to_shift[i][2]*this->stride[2])*this->calibration[2]
            ) : Vec3{};
    }
    for (size_t i = 0 ; i < triangles_array[layout][0] ; i++) {
        this->faces.push_back(
            Face(
                v_buffer[triangles_array[layout][1+i*3]],
                v_buffer[triangles_array[layout][1+i*3+1]],
                v_buffer[triangles_array[layout][1+i*3+2]]
            )
        );
    }
}