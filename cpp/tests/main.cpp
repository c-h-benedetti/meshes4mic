#include <iostream>
#include <gtest/gtest.h>
#include <random>

#include "meshes4mic/labels2meshes.hpp"

size_t calcul(size_t height, size_t width, size_t z, size_t y, size_t x) {
    return z * height * width + y * width + x;
}

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

int random_within_range(int min, int max) {
    static std::mt19937 generator(std::random_device{}());
    std::uniform_int_distribution<int> distribution(min, max);
    return distribution(generator);
}

TEST(ImageBrowsingTest, Correct1DIndex) {
    // Différentes configurations de tailles d'image
    std::vector<std::tuple<size_t, size_t, size_t>> dimensions = {
        {128, 128, 128},
        {256, 256, 256},
        {512, 512, 512},
        {1024, 1024, 1024}
    };

    // Strides à tester
    std::vector<std::tuple<size_t, size_t, size_t>> strides = {
        {1, 1, 1},
        {2, 3, 5},
        {4, 4, 4}
    };

    for (const auto& dim : dimensions) {
        for (const auto& stride : strides) {
            size_t depth = std::get<0>(dim);
            size_t height = std::get<1>(dim);
            size_t width = std::get<2>(dim);
            for (size_t k = 0 ; k < 100 ; k++) {
                size_t s_z = std::get<0>(stride);
                size_t s_y = std::get<1>(stride);
                size_t s_x = std::get<2>(stride);

                // Générer des positions aléatoires dans l'image
                size_t z = random_within_range(s_z, depth - s_z);
                size_t y = random_within_range(s_y, height - s_y);
                size_t x = random_within_range(s_x, width - s_x);

                // Initialiser les objets
                MarchingCube mc = MarchingCube(nullptr, {depth, height, width}, {1.0f, 1.0f, 1.0f}, {s_z, s_y, s_x});
                NeighborsZYX n(mc);

                size_t idx = calcul(height, width, z, y, x);
                n.get_layout(idx);

                // Vérifications
                EXPECT_EQ(n.get_buffer()[0], idx);
                EXPECT_EQ(n.get_buffer()[1], calcul(height, width, z, y, x + s_x));
                EXPECT_EQ(n.get_buffer()[2], calcul(height, width, z, y + s_y, x + s_x));
                EXPECT_EQ(n.get_buffer()[3], calcul(height, width, z, y + s_y, x));
                EXPECT_EQ(n.get_buffer()[4], calcul(height, width, z + s_z, y, x));
                EXPECT_EQ(n.get_buffer()[5], calcul(height, width, z + s_z, y, x + s_x));
                EXPECT_EQ(n.get_buffer()[6], calcul(height, width, z + s_z, y + s_y, x + s_x));
                EXPECT_EQ(n.get_buffer()[7], calcul(height, width, z + s_z, y + s_y, x));
            }
        }
    }
}

int main(int argc, char* argv[]) {
    ::testing::InitGoogleTest(&argc, argv);
    return RUN_ALL_TESTS();
}