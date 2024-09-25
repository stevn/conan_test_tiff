cmake_minimum_required(VERSION 3.26)

project(stufftestpkg_prj)

include(CTest)

find_package(stuff REQUIRED CONFIG)

add_executable(stufftestpkg)
target_sources(stufftestpkg PRIVATE stufftestpkg.cpp)
target_link_libraries(stufftestpkg PRIVATE stuff::stuff)
add_test(
	NAME stufftestpkg
	COMMAND $<TARGET_FILE:stufftestpkg>
)
