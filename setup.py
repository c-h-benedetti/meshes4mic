from setuptools import setup, Extension
from pybind11.setup_helpers import Pybind11Extension, build_ext
from setuptools import find_packages

ext_modules = [
    Pybind11Extension("m4mcore", [
            "cpp/labels2meshes.cpp",
            "src/meshes4mic/bindings/main.cpp"
        ],
        include_dirs=["include"]
    ),
]

setup(
    name="m4mcore",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    packages=find_packages(),
    package_data={
        'm4mcore': ['py.typed', 'stubs/**/*.pyi'],
    },
    include_package_data=True,
)
