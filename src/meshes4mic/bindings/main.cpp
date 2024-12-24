#include <pybind11/pybind11.h>
#include <pybind11/numpy.h>
#include <memory>
#include <stdexcept>
#include <cstddef>
#include <cstdint>
#include "meshes4mic/labels2meshes.hpp"

namespace py = pybind11;

int test_fx(int a, int b) { return a+b; }

std::shared_ptr<MarchingCube> create_marching_cubes(py::array_t<uint8_t> m,
                                                    py::tuple dims,
                                                    py::tuple calib,
                                                    py::tuple strd) {
    // 1. Vérifier que les arguments ne sont pas None
    if (m.is_none()) {
        throw std::runtime_error("Le tableau 'm' ne doit pas être None.");
    }
    if (dims.is_none()) {
        throw std::runtime_error("Le tuple 'dims' ne doit pas être None.");
    }
    if (calib.is_none()) {
        throw std::runtime_error("Le tuple 'calib' ne doit pas être None.");
    }
    if (strd.is_none()) {
        throw std::runtime_error("Le tuple 'strd' ne doit pas être None.");
    }

    // 2. Vérifier que 'm' est un tableau NumPy 3D de type uint8
    if (m.ndim() != 3) {
        throw std::runtime_error("Le tableau 'm' doit avoir exactement 3 dimensions.");
    }

    // 3. Vérifier que le tableau 'm' est contiguë en mémoire C (row-major)
    if (!(m.flags() & py::array::c_style)) {
        throw std::runtime_error("Le tableau 'm' n'est pas contiguë en mémoire C (row-major).");
    }

    // 4. Vérifier que les tuples ont exactement 3 éléments
    if (dims.size() != 3) {
        throw std::runtime_error("Le tuple 'dims' doit contenir exactement 3 éléments.");
    }
    if (calib.size() != 3) {
        throw std::runtime_error("Le tuple 'calib' doit contenir exactement 3 éléments.");
    }
    if (strd.size() != 3) {
        throw std::runtime_error("Le tuple 'strd' doit contenir exactement 3 éléments.");
    }

    // 5. Extraire et valider les valeurs des tuples
    std::array<size_t, 3> dims_values;
    std::array<double, 3> calib_values;
    std::array<size_t, 3> strd_values;

    for (size_t i = 0; i < 3; ++i) {
        // Extraction et vérification des dimensions
        size_t dim = dims[i].cast<size_t>();
        double calib_val = calib[i].cast<double>();
        size_t strd_val = strd[i].cast<size_t>();

        // Vérifier que les valeurs sont positives et non nulles
        if (dim <= 0) {
            throw std::runtime_error("Tous les éléments de 'dims' doivent être positifs et non nuls.");
        }
        if (calib_val <= 0.0f) {
            throw std::runtime_error("Tous les éléments de 'calib' doivent être positifs et non nuls.");
        }
        if (strd_val <= 0) {
            throw std::runtime_error("Tous les éléments de 'strd' doivent être positifs et non nuls.");
        }

        dims_values[i]  = dim;
        calib_values[i] = calib_val;
        strd_values[i]  = strd_val;
    }

    // 6. Extraire les pointeurs vers les données du tableau 'm'
    py::buffer_info m_info = m.request();
    const uint8_t* m_ptr = static_cast<const uint8_t*>(m_info.ptr);

    // 7. Créer l'instance C++ de MarchingCube
    MarchingCube* mc = new MarchingCube(m_ptr, dims_values, calib_values, strd_values);

    // 8. Retourner un shared_ptr avec un délégué qui maintient les références aux objets Python
    return std::shared_ptr<MarchingCube>(mc, [m, dims, calib, strd](MarchingCube* ptr) {
        delete ptr;
        // Les objets m, dims, calib, strd sont capturés par valeur et restent vivants
    });
}

PYBIND11_MODULE(m4mcore, m) {
    m.doc() = "Python bindings for meshes4mic";
    
    // -------------------------------------------------------------------------------

    py::module_ surfaces = m.def_submodule("surfaces", "All the classes and functions used to convert label maps into meshes.");

    py::class_<MarchingCube, std::shared_ptr<MarchingCube>>(surfaces, "MarchingCube")
        .def(py::init(&create_marching_cubes), py::arg("mask"), py::arg("shape"), py::arg("calibration"), py::arg("stride"))
        .def("run", &MarchingCube::run);

    // -------------------------------------------------------------------------------

    py::module_ distances = m.def_submodule("distances", "Distance transform methods.");

    distances.def("test_fx", &test_fx,
        py::arg("arg1"),
        py::arg("arg2"),
        "A function exposed from C++ to process the sum of two integers."
    );

    // -------------------------------------------------------------------------------

    py::module_ flux = m.def_submodule("flux", "Flux processing methods.");

    flux.def("other_function", &other_function,
        py::arg("arg1"),
        py::arg("arg2"),
        "A function exposed from C++ to process the sum of two integers."
    );
}

