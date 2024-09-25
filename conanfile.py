import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import copy
from conan.tools.build import can_run


COMPONENT_STUFF_LIB = "stuff"
COMPONENT_STUFF_TOOL = "stufftool"


class StuffConanPkg(ConanFile):

    name = "stuff"
    version = "1.0.0"

    # package_type = "application"
    package_type = "library"
    # package_type = "unknown"

    settings = "os", "compiler", "build_type", "arch"

    options = {"shared": [True, False]}
    default_options = {"shared": False}

    exports_sources = "CMakeLists.txt", "src/*"

    tool_requires = "cmake/[^3]"

    generators = [
        "CMakeDeps",
        "CMakeToolchain",
        "VirtualBuildEnv",
        "VirtualRunEnv",
    ]

    def requirements(self):
        # ZSTD

        # This works OK, but uses old version of zstd - I need to use latest version 1.5.6:
        self.requires('zstd/1.5.5')

        # This doesn't work (conan package version conflict: libtiff requires hardcoded zstd version 1.5.5):
        # ERROR: Version conflict: Conflict between zstd/1.5.5 and zstd/1.5.6 in the graph.
        # Conflict originates from libtiff/4.7.0
        # self.requires('zstd/1.5.6')

        # This doesn't work (conan install is OK, but zstd.h is not found at compile-time):
        # src/lib/stuff/stuff.cpp:3:10: fatal error: 'zstd.h' file not found
        # #include <zstd.h>
        #          ^~~~~~~~
        # self.requires('zstd/1.5.6', override=True)

        # This doesn't work (conan install is OK, but zstd.h is not found at compile-time):
        # src/lib/stuff/stuff.cpp:3:10: fatal error: 'zstd.h' file not found
        # #include <zstd.h>
        #          ^~~~~~~~
        # self.requires('zstd/1.5.6', override=True, headers=True, libs=True)

        # TIFF
        self.requires('libtiff/4.7.0')

    def layout(self):
        cmake_layout(self)

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if can_run(self):
            cmake.test()

    def package(self):
        copy(self,
            pattern="*",
            src=os.path.join(self.source_folder, 'src/lib/stuff/include'),
            dst=os.path.join(self.package_folder, 'include'),
        )
        copy(self,
            pattern="*/stuff_export.h",
            src=os.path.join(self.build_folder),
            dst=os.path.join(self.package_folder, 'include'),
            keep_path=False,
        )
        if self.settings.os == "Windows":
            copy(self,
                pattern="*/stuff.lib",
                src=self.build_folder,
                dst=os.path.join(self.package_folder, 'lib'),
                keep_path=False,
            )
            copy(self,
                pattern="*/stuff.dll",
                src=self.build_folder,
                dst=os.path.join(self.package_folder, 'bin'),
                keep_path=False,
            )
            copy(self,
                pattern="*/stuff.pdb",
                src=self.build_folder,
                dst=os.path.join(self.package_folder, 'bin'),
                keep_path=False,
            )
            copy(self,
                pattern="*/stufftool.exe",
                src=self.build_folder,
                dst=os.path.join(self.package_folder, 'bin'),
                keep_path=False,
            )
            copy(self,
                pattern="*/stufftool.pdb",
                src=self.build_folder,
                dst=os.path.join(self.package_folder, 'bin'),
                keep_path=False,
            )
        else:
            copy(self,
                pattern="*/libstuff.a",
                src=self.build_folder,
                dst=os.path.join(self.package_folder, 'lib'),
                keep_path=False,
            )
            copy(self,
                pattern="*/libstuff.dylib",
                src=self.build_folder,
                dst=os.path.join(self.package_folder, 'lib'),
                keep_path=False,
            )
            copy(self,
                pattern="*/stufftool",
                src=self.build_folder,
                dst=os.path.join(self.package_folder, 'bin'),
                keep_path=False,
            )

    def package_info(self):
        self.cpp_info.components[COMPONENT_STUFF_LIB].libs = [COMPONENT_STUFF_LIB]
        self.cpp_info.components[COMPONENT_STUFF_LIB].includedirs = ['include']
        self.cpp_info.components[COMPONENT_STUFF_LIB].requires = [
            'zstd::zstd',
            'libtiff::libtiff',
        ]

        self.cpp_info.components[COMPONENT_STUFF_TOOL].bindirs = ['bin']
        self.cpp_info.components[COMPONENT_STUFF_TOOL].requires = [COMPONENT_STUFF_LIB]

        self.cpp_info.bindirs = ['bin']

        # self.runenv_info.append_path("PATH", os.path.join(self.package_folder, 'bin'))
