include_directories("../src")

choreonoid_add_executable(vnoid_python_test vnoid_python_test.cpp)

target_link_libraries(vnoid_python_test vnoid_lib)
