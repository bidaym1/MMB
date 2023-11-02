cmake_minimum_required(VERSION 3.16)

SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}")

project(module)

add_definitions(-DPYBIND)



find_package(PythonLibs)



   
find_package(pybind11 REQUIRED)
pybind11_add_module(module bindings.cpp
  ca.cpp
  cell.cpp
  conrec_pytst.cpp
  crash.cpp
  dish.cpp
  hull.cpp
  info.cpp
  misc.cpp
  output.cpp
  parameter.cpp
  parse.cpp
  pde.cpp
  random.cpp
  warning.cpp
)
target_include_directories(module PUBLIC .)

