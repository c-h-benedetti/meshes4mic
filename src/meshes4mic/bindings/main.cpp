#include <pybind11/pybind11.h>

int test_fx(int a, int b) { return a+b; }

PYBIND11_MODULE(m4mcore, m) {
    m.doc() = "Python bindings for meshes4mic";
    m.def("test_fx", &test_fx,
        pybind11::arg("arg1"),
        pybind11::arg("arg2"),
        "A function exposed from C++ to process the sum of two integers."
    );
}

