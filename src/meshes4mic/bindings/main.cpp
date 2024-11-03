#include <pybind11/pybind11.h>

int test_fx(int a, int b) { return a+b; }

PYBIND11_MODULE(m4mcore, m) {
    m.doc() = "Python bindings for meshes4mic";
    m.def("test_fx", &test_fx,
        pybind11::arg("First int argument"),
        pybind11::arg("Second int argument"),
        "A function exposed from C++ to process the sum of two integers."
    );
}

