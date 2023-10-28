cmake_minimum_required(VERSION 3.16)
set(CMAKE_CXX_COMPILER "/usr/bin/clang")
set(CMAKE_C_COMPILER "/usr/bin/clang") 
set(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} -std=c++11")
set(GCC_COVERAGE_COMPILE_FLAGS "${GCC_COVERAGE_COMPILE_FLAGS} -undefined dynamic_lookup")
IF(APPLE)
  SET(CMAKE_HOST_SYSTEM_PROCESSOR arm64)
  SET(CMAKE_OSX_ARCHITECTURES "arm64" CACHE STRING "Build architectures for Mac OS X" FORCE)
ENDIF(APPLE)
SET(CMAKE_CXX_FLAGS  "${CMAKE_CXX_FLAGS} ${GCC_COVERAGE_COMPILE_FLAGS}")

project(module)

# Generate python module library
#if(PYBIND_LIB)
    message("=====> GENERATING PYBIND LIBRARY <=====")

    add_definitions(-DPYBIND)

    find_package(PythonLibs)
	set(PYTHON_INCLUDE_DIRS "/Users/koenkeijzer/miniforge3/envs/conda-tst-md/include/")
    include_directories(${PYTHON_INCLUDE_DIRS})
	message(STATUS ${PYTHON_INCLUDE_DIRS})

    add_subdirectory(pybind11 build)
    pybind11_add_module(module bindings.cpp
								ca.cpp
								cell.cpp
								conrec.cpp
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
#endif()
#add_subdirectory(../pybind11 build)
#pybind11_add_module(module binding.cpp testCPM.cpp testdish.cpp)
