/**
 * @file Spheres.hpp
 * @author Václav Martinka a Petr Buchal
 * @date 07. 01. 2020 (21:54)
 * @brief 
 */


#ifndef SPHERES_HPP
#define SPHERES_HPP

#include <vector>
#include <cmath>

#include "simpleMath.hpp"
#include "Coord.hpp"

typedef struct {
	float x, y, z, radius;
} Sphere;



class Spheres {
public:
	Spheres()  {};
	~Spheres() {};

	void add(const float x, const float y, const float z, const float radius) {
		spheresX.push_back(x);
		spheresY.push_back(y);
		spheresZ.push_back(z);
		spheresRadius.push_back(radius);
	}

	void add(const Coord coord, const float radius) {
		add(coord.x, coord.y, coord.z, radius);
	}

	void add(const Sphere sphere) {
		add(sphere.x, sphere.y, sphere.z, sphere.radius);
	}

	
	Sphere get(const size_t index) { return {spheresX.at(index), spheresY.at(index), spheresZ.at(index), spheresRadius.at(index)}; }


	float *getSpheresX() { return spheresX.data(); }
	float *getSpheresY() { return spheresY.data(); }
	float *getSpheresZ() { return spheresZ.data(); }
	float *getSpheresRadius() { return spheresRadius.data(); }
	

	float getX(size_t index) { return spheresX.at(index); }
	float getY(size_t index) { return spheresY.at(index); }
	float getZ(size_t index) { return spheresZ.at(index); }
	float getRadius(size_t index) { return spheresRadius.at(index); }


	size_t count() { return spheresX.size(); }


	float distance(const size_t index, const Coord &coord) {
		return sqrt(squared(coord.x - spheresX[index]) + squared(coord.y - spheresY[index]) + squared(coord.z - spheresZ[index]));
	}


private:
	std::vector<float> spheresX;
	std::vector<float> spheresY;
	std::vector<float> spheresZ;
	std::vector<float> spheresRadius;
	
};


inline float distanceSpheresCenters( const Sphere a, const Sphere b ) {
	return sqrt( squared( a.x - b.x ) + squared( a.y - b.y ) + squared( a.z - b.z ) );
}

inline void printSphere(const Sphere &s) {
	printf("x\ty\tz\tradius\n");
	printf("%.3f\t%.3f\t%.3f\t%.3f\n", s.x, s.y, s.z, s.radius);
}

inline Coord Sphere2Coord(Sphere s) {
	return {s.x, s.y, s.z};
}



#endif