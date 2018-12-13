#pragma once

#include <cstdint>
#include <string>
#include <opencv2/core/core.hpp>

class Image {
 public:
  Image(int width, int height);
  ~Image();

  uint32_t& at(int x, int y);
  void set(int x, int y, unsigned char r, unsigned char g, unsigned char b, unsigned char a);
  cv::Mat get_mat();

 private:
  uint32_t* buffer_;
  int width_;
  int height_;
};