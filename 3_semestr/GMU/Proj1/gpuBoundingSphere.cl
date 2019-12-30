/**
 * @file gpuBoundingSphere.cl
 * @author Václav Martinka a Petr Buchal
 * @date 28. 12. 2019 (15:44)
 * @brief
 */

inline float squared(const float x) {
	return x * x;
}


inline float dist(const float x1, const float x2, const float y1, const float y2, const float z1, const float z2) {
	return sqrt(squared(x1 - x2) + squared(y1 - y2) + squared(z1 -z2));
}


__kernel void boundingSphere(
	__global const float *xData,  __global const float *yData,  __global const float *zData,  __global const float *radiusData,
	__global const float *xCoord, __global const float *yCoord, __global const float *zCoord,
	__global float* result, const int spheresCount, const int dimensionsCount
) {
	int id = (int)get_global_id(0);


	if (id < dimensionsCount) {
		// Najdu nejmensi mozny polomer
		float radius = 0;

		// Projdu vsechny koule a spocitam jejich vzdalenost
		for (size_t i = 0; i < spheresCount; ++i) {
			radius = max(radius, dist(xData[i], xCoord[id], yData[i], yCoord[id], zData[i], zCoord[id]) + radiusData[i]);
		}

		result[id] = radius;
	}
}
