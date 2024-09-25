add_executable(stufftool)
target_sources(stufftool PRIVATE stufftool.cpp)
target_link_libraries(stufftool PRIVATE stuff)
add_test(
	NAME stufftool
	COMMAND $<TARGET_FILE:stufftool>
)
