cmake_minimum_required(VERSION 3.22)

project(M4M)

# Définit le standard C++ utilisé
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Options pour le compilateur (exemple : ajouter des warnings)
set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Werror")

# Chemins vers les fichiers source
set(SRC_DIR ${CMAKE_SOURCE_DIR}/cpp)
set(INCLUDE_DIR ${CMAKE_SOURCE_DIR}/include)
set(TEST_DIR ${CMAKE_SOURCE_DIR}/cpp/tests)

# Ajout des fichiers sources
set(SRC_FILES
    ${TEST_DIR}/main.cpp
    ${SRC_DIR}/labels2meshes.cpp
)

# Définir l'exécutable principal (si nécessaire)
add_executable(M4M ${SRC_FILES})
target_include_directories(M4M PUBLIC ${INCLUDE_DIR})

# Lien avec les bibliothèques Google Test
find_package(GTest REQUIRED)
target_link_libraries(M4M GTest::GTest GTest::Main pthread)