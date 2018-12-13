#pragma once

#include "scene_base.h"

class Quadric : public SceneObject {
 public:
  Quadric(V3 origin_coord, V3 param_vec, int quadric_type, Material* material, float bounding_box_range);
  Intersection intersect(Ray ray);
  void change_type(int new_type);
  void change_param_vec_(V3 new_param_vec_);
  void change_material(Material *new_material);
  void change_bounding_box_range(double new_range);

 private:
  void count_eq_type1(Ray ray, int e1, int e2, float *ax, float *bx, float *cx);
  void count_eq_type2(Ray ray, int e1, int e2, int e3, float *ax, float *bx, float *cx);
  V3 count_norm_type1(float hit_x, float hit_y, float hit_z, float a, float b, float c, float e1, float e2);
  V3 count_norm_type2(float hit_x, float hit_y, float a, float b, float e);
  V3 count_norm_type3(float hit_x, float hit_y, float a, float b, float e);
  bool check_bounding_box(V3 p);

  V3 origin_coord_;
  V3 param_vec_;
  int quadric_type_;
  float bounding_box_range_;
};