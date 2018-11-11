cmake_minimum_required(VERSION 2.8)
project(a3-ece650)

set (CMAKE_CXX_FLAGS "-std=c++11 -Wall ${CMAKE_CXX_FLAGS}")
set(CMAKE_INSTALL_PREFIX ${CMAKE_BINARY_DIR}/run)

add_executable(a2-ece650 a2-ece650.cpp edge.cpp edge.hpp graph.cpp graph.hpp parser.cpp parser.hpp)
add_executable(a3-ece650 a3-ece650.cpp)
add_executable(rgen rgen.cpp)

install(PROGRAMS a1ece650.py edge1.py vertex1.py graph1.py parser.py DESTINATION bin)
install(TARGETS a2-ece650 a3-ece650 rgen RUNTIME DESTINATION bin)