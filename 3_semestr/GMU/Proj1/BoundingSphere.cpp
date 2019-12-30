/**
* @file BoundingSphere.cpp
* @author Václav Martinka a Petr Buchal
* @date 29. 12. 2019 (15:42)
* @brief
*/


#include <limits>
#include <algorithm>

#include "BoundingSphere.hpp"


using namespace std;


void BoundingSphere::getBoundingBlock(Coord &from, Coord &to) {
	if (validBoundingBlock) {
		from = boundingBlockFrom;
		to = boundingBlockTo;
	}
	else {
		from.x = from.y = from.z = numeric_limits<float>::max();
		to.x = to.y = to.z = numeric_limits<float>::min();

		for ( size_t i = 0; i < _spheres->count() ; i++ ) {
			from.x = min( from.x, _spheres->getSpheresX()[i] - _spheres->getSpheresRadius()[i] );
			from.y = min( from.y, _spheres->getSpheresY()[i] - _spheres->getSpheresRadius()[i] );
			from.z = min( from.z, _spheres->getSpheresZ()[i] - _spheres->getSpheresRadius()[i] );

			to.x = max( to.x, _spheres->getSpheresX()[i] + _spheres->getSpheresRadius()[i] );
			to.y = max( to.y, _spheres->getSpheresY()[i] + _spheres->getSpheresRadius()[i] );
			to.z = max( to.z, _spheres->getSpheresZ()[i] + _spheres->getSpheresRadius()[i] );
		}

		boundingBlockFrom = from;
		boundingBlockTo = to;
		validBoundingBlock = true;
	}
}

Sphere BoundingSphere::getBoundingSphere() {
	Coord from, to;
	getBoundingBlock(from, to);
	Sphere prevSphere, newSphere = {numeric_limits<float>::max(),numeric_limits<float>::max(),numeric_limits<float>::max(),numeric_limits<float>::max()};

	while (distanceSpheresCenters(prevSphere, newSphere) > DISTANCE_LIMIT) {
		prevSphere = newSphere;
		newSphere = getBoundingSphereOneStep(from, to);
	}

	return newSphere;
}


Sphere BoundingSphere::getBoundingSphereOneStep(Coord &from, Coord &to) {
	float stepX = (to.x - from.x) / 2;
	float stepY = (to.y - from.y) / 2;
	float stepZ = (to.z - from.z) / 2;

	Spheres results;

	for (size_t x = 0; x < 2; x++) {
		for (size_t y = 0; y < 2; y++) {
			for (size_t z = 0; z < 2; z++) {
				Coord tmpCoord = {
					from.x + x * stepX + stepX / 2,
					from.y + y * stepY + stepY / 2,
					from.z + z * stepZ + stepZ / 2
				};
				results.add(tmpCoord, findBoundingSphereRadiusAt(tmpCoord));
			}
		}
	}

	Sphere resultSphere = {0,0,0,numeric_limits<float>::max()};
	for (size_t i = 0; i < results.count(); ++i) {
		if (resultSphere.radius > results.getSpheresRadius()[i]) {
			resultSphere = results.get(i);
		}
	}

	from.x = resultSphere.x - stepX / 2;
	from.y = resultSphere.y - stepY / 2;
	from.z = resultSphere.z - stepZ / 2;
    
	to.x = resultSphere.x + stepX / 2;
	to.y = resultSphere.y + stepY / 2;
	to.z = resultSphere.z + stepZ / 2;

	return resultSphere;
}


float BoundingSphere::findBoundingSphereRadiusAt(Coord coord) {
	float radius = 0;
	for (size_t i = 0; i < _spheres->count(); ++i) {
		radius = max(radius, _spheres->distance(i, coord) + _spheres->getSpheresRadius()[i]);
	}

	return radius;
}
