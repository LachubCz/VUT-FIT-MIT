cmake_minimum_required (VERSION 2.6)
project (raytracer)
set(CMAKE_CXX_FLAGS "-std=c++11 -O3")
find_package( OpenCV REQUIRED )
add_executable(raytracer src/image.cpp
					     src/input_format.cpp
					     src/main.cpp
					     src/scene.cpp
					     src/scene_base.cpp
					     src/quadric.cpp
					     src/v3.cpp)
target_link_libraries(raytracer LINK_PUBLIC ${OpenCV_LIBS})
