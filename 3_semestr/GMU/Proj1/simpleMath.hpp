/**
* @file simpleMath.hpp
* @author Václav Martinka a Petr Buchal
* @date 29. 12. 2019 (15:42)
* @brief
*/

#ifndef SIMPLE_MATH_HPP
#define SIMPLE_MATH_HPP

#include <limits>
#include <vector>


inline float squared(const float input) {
	return input * input;
}

inline size_t findMin(const std::vector<float> &numbers) {
	size_t index;
	float minVal = std::numeric_limits<float>::max();

	for (size_t i = 0; i < numbers.size(); ++i) {
		if (numbers[i] < minVal) {
			minVal = numbers[i];
			index = i;
		}
	}

	return index;
}


#endif