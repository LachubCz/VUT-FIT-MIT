#ifndef __VIDEOBUF__
#define __VIDEOBUF__

#include <ac_int.h>

#define BUFFER_COLS   320
#define BUFFER_ROWS   4

typedef ac_int<3,false> t_pixel;

void video_buf(t_pixel &in_data, bool &in_data_vld, 
   ac_int<10,false> vga_row, ac_int<10,false> vga_col, 
   t_pixel &out_data, bool &vga_enable, bool &gen_pause);

#endif
