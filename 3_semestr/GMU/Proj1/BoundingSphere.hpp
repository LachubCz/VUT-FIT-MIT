/**
 * @file BoundingSphere.hpp
 * @author Václav Martinka a Petr Buchal
 * @date 29. 12. 2019 (15:41)
 * @brief
 */

#ifndef BOUNDING_SPHERE_HPP
#define BOUNDING_SPHERE_HPP

#include "Spheres.hpp"
#include "Coord.hpp"

#define DISTANCE_LIMIT 0.000001



class BoundingSphere {
public:
	BoundingSphere( Spheres &spheres ) { _spheres = &spheres; };
	~BoundingSphere() {};

	void getBoundingBlock(Coord &from, Coord &to);
	Sphere getBoundingSphere();


private:
	Spheres * _spheres;

	float findBoundingSphereRadiusAt(Coord coord);
	Sphere getBoundingSphereOneStep(Coord &from, Coord &to);

	bool validBoundingBlock = false;
	Coord boundingBlockFrom, boundingBlockTo;
};

#endif