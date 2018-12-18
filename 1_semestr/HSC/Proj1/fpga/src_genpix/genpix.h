#ifndef __GENPIX__
#define __GENPIX__

#include <ac_int.h>

typedef ac_int<3,false> t_pixel;
typedef ac_int<9,false> t_pix_pos;

void genpix(bool &pause, bool &req, t_pixel &pixel, bool &pixel_vld);

#endif
