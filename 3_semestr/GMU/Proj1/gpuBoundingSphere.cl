/**
 * @file gpuBoundingSphere.cl
 * @author Václav Martinka a Petr Buchal
 * @date 07. 01. 2020 (21:55)
 * @brief
 */


//#define DISTANCE_LIMIT 0.000001
#define MASTER 0

inline float squared(const float x) {
	return x * x;
}


inline float dist(const float x1, const float x2, const float y1, const float y2, const float z1, const float z2) {
	return sqrt(squared(x1 - x2) + squared(y1 - y2) + squared(z1 -z2));
}


void prepareData(
	float fromX, float fromY, float fromZ,
	float toX, float toY, float toZ,
	float stepX, float stepY, float stepZ,
	__global float *xCoord, __global float *yCoord, __global float *zCoord,
	const int subcubesInLine
) {
	// Prichystam souradnice
	size_t i = 0;
	float tmpX = fromX + stepX / 2;
	for (size_t x = 0; x < subcubesInLine; ++x) {
		float tmpY = fromY + stepY / 2;
			
		for (size_t y = 0; y < subcubesInLine; ++y) {
			float tmpZ = fromZ + stepZ / 2;
				
			for (size_t z = 0; z < subcubesInLine; ++z) {
				xCoord[i] = tmpX;
				yCoord[i] = tmpY;
				zCoord[i] = tmpZ;

				tmpZ += stepZ;
				++i;
			}

			tmpY += stepY;
		}

		tmpX += stepX;
	}
}


void count(
	__global const float *xData, __global const float *yData, __global const float *zData, __global const float *radiusData,
	__global float *xCoord, __global float *yCoord, __global float *zCoord,
	__global float* result, const int spheresCount, const int id
) {
	// Najdu nejmensi mozny polomer
	float radius = 0;

	// Projdu vsechny koule a spocitam jejich vzdalenost
	for (size_t i = 0; i < spheresCount; ++i) {
		radius = max(radius, dist(xData[i], xCoord[id], yData[i], yCoord[id], zData[i], zCoord[id]) + radiusData[i]);
	}

	result[id] = radius;
}


size_t findMin(__global float *numbers, size_t size) {
	size_t index;
	float minVal = FLT_MAX;

	for (size_t i = 0; i < size; ++i) {
		if (numbers[i] < minVal) {
			minVal = numbers[i];
			index = i;
		}
	}

	return index;
}




__kernel void boundingSphere(
	__global const float *xData,  __global const float *yData,  __global const float *zData,  __global const float *radiusData,
	__global float *xCoord, __global float *yCoord, __global float *zCoord,
	float fromX, float fromY, float fromZ, float toX, float toY, float toZ, 
	__global float* result, const int spheresCount, const float distanceLimit, const int subcubesInLine, const int dimensionsCount, __global bool *run
) {
	int id = (int)get_global_id(0);

	float centerX, centerY, centerZ;
	float stepX, stepY, stepZ;
	centerX = centerY = centerZ = FLT_MAX;

	// Povolim vypocet
	if (id == MASTER) {
		*run = true;
	}
	barrier(CLK_GLOBAL_MEM_FENCE);

	// Ochrana proti zamrznuti
	size_t counter = 1000;

	if (id < dimensionsCount) {
		while (*run) {
			--counter;
			// Pripravim data vlaknem 0
			if (id == MASTER) {
				// Vypoctu krok
				stepX = (toX - fromX) / subcubesInLine;
				stepY = (toY - fromY) / subcubesInLine;
				stepZ = (toZ - fromZ) / subcubesInLine;

				prepareData(fromX, fromY, fromZ, toX, toY, toZ, stepX, stepY, stepZ, xCoord, yCoord, zCoord, subcubesInLine);
			}
			barrier(CLK_GLOBAL_MEM_FENCE);

			// Spustim vypocet
			count(xData, yData, zData, radiusData, xCoord, yCoord, zCoord, result, spheresCount, id);
		
			// Najdu nejmensi kouli
			if (id == MASTER) {
				size_t minValIndex = findMin(result, dimensionsCount);

				// Zkontroluji presnost vypoctu
				if (dist(centerX, xCoord[minValIndex], centerY, yCoord[minValIndex], centerZ, zCoord[minValIndex]) < distanceLimit) {
					result[3] = result[minValIndex];
					result[0] = xCoord[minValIndex];
					result[1] = yCoord[minValIndex];
					result[2] = zCoord[minValIndex];
					*run = false;
				}
				else {
					centerX = xCoord[minValIndex];
					centerY = yCoord[minValIndex];
					centerZ = zCoord[minValIndex];

					fromX = toX = centerX - stepX / 2;
					fromY = toY = centerY - stepY / 2;
					fromZ = toZ = centerZ - stepZ / 2;
					toX += stepX;
					toY += stepY;
					toZ += stepZ;
				}
			}

			if (!counter) {
				return;
			}

			barrier(CLK_GLOBAL_MEM_FENCE);
		}
	}
}
