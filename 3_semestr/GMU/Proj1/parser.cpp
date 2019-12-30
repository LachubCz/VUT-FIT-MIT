/**
 * @file parser.cpp
 * @author Václav Martinka a Petr Buchal
 * @date 29. 12. 2019 (15:42)
 * @brief
 */


#include <cstdlib>
#include <cstdio>
#include <iostream>
#include <fstream>
#include <vector>


#include "Spheres.hpp"


using namespace std;

Spheres parse( char* filename ) {
	Spheres spheres;

	ifstream input(filename);

	if (!input) {
		printf("Invalid file!\n");
		return spheres;
	}


	float x, y, z, radius;
	while (input >> x >> y >> z >> radius)
	{
		spheres.add(x, y, z, radius);
	}

	
	float sumX = 0;
	float sumY = 0;
	float sumZ = 0;
	float sumRadius = 0;

	for (size_t i = 0; i < spheres.count(); ++i) {
		Sphere sphere = spheres.get( i );

		sumX += sphere.x * sphere.radius;
		sumY += sphere.y * sphere.radius;
		sumZ += sphere.z * sphere.radius;
		sumRadius += sphere.radius;
	}

	return spheres;
}