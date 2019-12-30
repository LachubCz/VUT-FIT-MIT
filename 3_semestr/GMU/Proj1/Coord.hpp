/**
* @file Coord.hpp
* @author Václav Martinka a Petr Buchal
* @date 29. 12. 2019 (15:41)
* @brief
*/

#ifndef COORD_HPP
#define COORD_HPP

#include <vector>

typedef struct {
	float x, y, z;
} Coord;


inline float distanceCoords(const Coord a, const Coord b) {
	return sqrt(squared(a.x - b.x) + squared(a.y - b.y) + squared(a.z - b.z));
}

//inline float distanceCoords(const float *x1, const float *y1, const float *z1, const float *x2, const float *y2, const float *z2, const size_t index) {
//	return sqrt(squared(x1[index] - x2[index]) + squared(y1[index] - y2[index]) + squared(z1[index] - z2[index]));
//}

//inline float distanceCoords(const float x1, const float y1, const float z1, const float *x2, const float *y2, const float *z2, const size_t index) {
//	return sqrt(squared(x1 - x2[index]) + squared(y1 - y2[index]) + squared(z1 - z2[index]));
//}

inline float distanceCoords(const Coord a, const float *x, const float *y, const float *z, const size_t index) {
	return distanceCoords({a.x, a.y, a.z}, {x[index], y[index], z[index]});
}

inline float distanceCoords(const Coord a, const std::vector<float> &x, const std::vector<float> &y, const std::vector<float> &z, const size_t index) {
	return distanceCoords({a.x, a.y, a.z}, {x[index], y[index], z[index]});
}



#endif