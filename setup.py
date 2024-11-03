from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension("m4mcore", [
            "src/meshes4mic/bindings/main.cpp"
        ],
        include_dirs=["include"]
    ),
]

setup(
    name="m4mcore",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext}
)