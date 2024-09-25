cmake_minimum_required(VERSION 3.26)

set(CMAKE_CXX_VISIBILITY_PRESET hidden)
set(CMAKE_VISIBILITY_INLINES_HIDDEN 1)

project(stuff_prj)

include(CTest)
include(GenerateExportHeader)

find_package(zstd REQUIRED CONFIG)
find_package(TIFF REQUIRED CONFIG)

add_subdirectory(src/lib/stuff)
add_subdirectory(src/app/stufftool)
