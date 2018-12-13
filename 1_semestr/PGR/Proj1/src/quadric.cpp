#include <stdlib.h>
#include "quadric.h"
#include "stdio.h"

Quadric::Quadric(V3 origin_coord, V3 param_vec, int quadric_type, Material* material, float bounding_box_range)
    : origin_coord_(origin_coord), param_vec_(param_vec), quadric_type_(quadric_type), bounding_box_range_(bounding_box_range) {
  material_ = material;
}
   
Intersection Quadric::intersect(Ray ray) {
  float ax, bx, cx, D;

  // Select type of quadric and count a, b, c
  switch (quadric_type_) {
      case 1:
        count_eq_type1(ray, 1, 1, &ax, &bx, &cx);
        break;
      case 2:
        count_eq_type2(ray, 1, -1, 0, &ax, &bx, &cx);
        break;
      case 3:
        count_eq_type2(ray, -1, -1, 0, &ax, &bx, &cx);
        break;
      case 4:
        count_eq_type1(ray, -1, 1, &ax, &bx, &cx);
        break;
      case 5:
        count_eq_type1(ray, -1, -1, &ax, &bx, &cx);
        break;
      case 6:
        count_eq_type1(ray, -1, 0, &ax, &bx, &cx);
        break;
      case 7:
        count_eq_type2(ray, 1, 0, 1, &ax, &bx, &cx);
        break;
      case 8:
        count_eq_type2(ray, -1, 0, 1, &ax, &bx, &cx);
        break;
      default:
        printf("Warning: You chose invalid type of quadric. Defaulting to ellipsoid.\n");
        count_eq_type1(ray, 1, 1, &ax, &bx, &cx);
        break;
  }
  
  // Count intersection
  Intersection intersection;
  intersection.happened_ = false;
  D = bx * bx - ax * cx * 4;
  if (D > 0) {
    float sD = sqrt(D);
    float t1 = (-bx + sD) / (2 * ax);
    float t2 = (-bx - sD) / (2 * ax);

    // Choose correct t
    float t = t1 < t2 ? t1 : t2;
    if (t <= 0 || !check_bounding_box(ray.origin_coord_ + ray.direction_unit_vec_ * t)) {
      t = t == t1 ? t2 : t1;
    }

    if (t > 0) {
      V3 hitpoint = ray.origin_coord_ + ray.direction_unit_vec_ * t;
      if (check_bounding_box(hitpoint)) {
        
        // Select type of quadric and count normal if it is needed 
        V3 normal = V3(1, 1, 1);
        if (material_->kDiffuse > 0) {
          switch (quadric_type_) {
              case 1:
                normal = count_norm_type1(hitpoint.x(), hitpoint.y(), hitpoint.z(), param_vec_.x(), param_vec_.y(), param_vec_.z(), 1, 1);
                break;
              case 2:
                normal = count_norm_type2(hitpoint.x(), hitpoint.y(), param_vec_.x(), param_vec_.y(), 1);
                break;
              case 3:
                normal = count_norm_type2(hitpoint.x(), hitpoint.y(), param_vec_.x(), param_vec_.y(), -1);
                break;
              case 4:
                normal = count_norm_type1(hitpoint.x(), hitpoint.y(), hitpoint.z(), param_vec_.x(), param_vec_.y(), param_vec_.z(), -1, 1);
                break;
              case 5:
                normal = count_norm_type1(hitpoint.x(), hitpoint.y(), hitpoint.z(), param_vec_.x(), param_vec_.y(), param_vec_.z(), -1, -1);
                break;
              case 6:
                normal = count_norm_type1(hitpoint.x(), hitpoint.y(), hitpoint.z(), param_vec_.x(), param_vec_.y(), param_vec_.z(), -1, 0);
                break;
              case 7:
                normal = count_norm_type3(hitpoint.x(), hitpoint.y(), param_vec_.x(), param_vec_.y(), 1);
                break;
              case 8:
                normal = count_norm_type3(hitpoint.x(), hitpoint.y(), param_vec_.x(), param_vec_.y(), -1);
                break;
              default:
                normal = count_norm_type1(hitpoint.x(), hitpoint.y(), hitpoint.z(), param_vec_.x(), param_vec_.y(), param_vec_.z(), 1, 1);
                break;
          }
        }
        intersection.happened_ = true;
        intersection.contact_coord_ = hitpoint;
        intersection.normal_unit_vec_ = normal.unit();
      }
    }

  }

  return intersection;
}

void Quadric::count_eq_type1(Ray ray, int e1, int e2, float *ax, float *bx, float *cx) {
  float a2, b2, c2, ab2, ac2, bc2;
  // Count useful variables
  a2 = param_vec_.x() * param_vec_.x();
  b2 = param_vec_.y() * param_vec_.y();
  c2 = param_vec_.z() * param_vec_.z();
  ab2 = a2 * b2;
  ac2 = a2 * c2;
  bc2 = b2 * c2;

  // Count parameters
  *ax = ray.direction_unit_vec_.x() * ray.direction_unit_vec_.x() * bc2 + \
        ray.direction_unit_vec_.y() * ray.direction_unit_vec_.y() * ac2 + \
        ray.direction_unit_vec_.z() * ray.direction_unit_vec_.z() * ab2 * e1;
  *bx = ((ray.origin_coord_.x() - origin_coord_.x()) * ray.direction_unit_vec_.x() * bc2  + \
         (ray.origin_coord_.y() - origin_coord_.y()) * ray.direction_unit_vec_.y() * ac2  + \
         (ray.origin_coord_.z() - origin_coord_.z()) * ray.direction_unit_vec_.z() * ab2 * e1) * 2;
  *cx = (ray.origin_coord_.x() * ray.origin_coord_.x() + origin_coord_.x() * origin_coord_.x() - 2 * ray.origin_coord_.x() * origin_coord_.x()) * bc2 + \
        (ray.origin_coord_.y() * ray.origin_coord_.y() + origin_coord_.y() * origin_coord_.y() - 2 * ray.origin_coord_.y() * origin_coord_.y()) * ac2 + \
        (ray.origin_coord_.z() * ray.origin_coord_.z() + origin_coord_.z() * origin_coord_.z() - 2 * ray.origin_coord_.z() * origin_coord_.z()) * ab2 * e1 - ab2 * c2 * e2;
}

void Quadric::count_eq_type2(Ray ray, int e1, int e2, int e3, float *ax, float *bx, float *cx) {
  float a2, b2, ab2;
  // Count useful variables
  a2 = param_vec_.x() * param_vec_.x();
  b2 = param_vec_.y() * param_vec_.y();
  ab2 = a2 * b2;

  // Count parameters
  *ax = ray.direction_unit_vec_.x() * ray.direction_unit_vec_.x() * b2 + \
        ray.direction_unit_vec_.y() * ray.direction_unit_vec_.y() * a2 * e1;
  *bx = (ray.origin_coord_.x() - origin_coord_.x()) * ray.direction_unit_vec_.x() * b2 * 2 + \
        (ray.origin_coord_.y() - origin_coord_.y()) * ray.direction_unit_vec_.y() * a2 * 2 * e1 + \
        ray.direction_unit_vec_.z() * ab2 * e2;
  *cx = (ray.origin_coord_.x() * ray.origin_coord_.x() + origin_coord_.x() * origin_coord_.x() - 2 * ray.origin_coord_.x() * origin_coord_.x()) * b2 + \
        (ray.origin_coord_.y() * ray.origin_coord_.y() + origin_coord_.y() * origin_coord_.y() - 2 * ray.origin_coord_.y() * origin_coord_.y()) * a2 * e1 + \
        (ray.origin_coord_.z() - origin_coord_.z()) * ab2 * e2 - ab2 * e3;
}

V3 Quadric::count_norm_type1(float hit_x, float hit_y, float hit_z, float a, float b, float c, float e1, float e2) {
  float r = sqrt(abs(e1 * e2 - (e1 * hit_x * hit_x / (a * a)) - (e1 * hit_y * hit_y / (b * b))));
  V3 result = V3(1, 0, ((-e1) * c * hit_x) / (a * a * r)).cross(V3(0, 1, ((-e1) * c * hit_y) / (b * b * r)));
  float e3 = hit_z < 0 ? -1 : 1;
  return V3(result.x(), result.y(), e3 * result.z());
}

V3 Quadric::count_norm_type2(float hit_x, float hit_y, float a, float b, float e) {
  return V3(1, 0, 2 * hit_x / (a * a)).cross(V3(0, 1, (e * 2) * hit_y / (b * b)));
}

V3 Quadric::count_norm_type3(float hit_x, float hit_y, float a, float b, float e) {
  float r = sqrt(abs(e - e * hit_x * hit_x / (a * a)));
  V3 result = V3((-e) * b * hit_x / (a * a * r), -1, 0);
  float e2 = hit_y < 0 ? -1 : 1;
  return V3(e2 * result.x(), result.y(), result.z());
}

bool Quadric::check_bounding_box(V3 p) {
  return p.x() > -bounding_box_range_ && p.x() < bounding_box_range_ && \
         p.y() > -bounding_box_range_ && p.y() < bounding_box_range_ && \
         p.z() > -bounding_box_range_ && p.z() < bounding_box_range_;
}

void Quadric::change_type(int new_type){
  quadric_type_ = new_type;
}

void Quadric::change_param_vec_(V3 new_param_vec_){
  param_vec_ = new_param_vec_;
}

void Quadric::change_material(Material *new_material) {
  material_ = new_material;
}

void Quadric::change_bounding_box_range(double new_range) {
  bounding_box_range_ = new_range;
}