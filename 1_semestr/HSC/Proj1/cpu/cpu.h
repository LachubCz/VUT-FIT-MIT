#ifndef CPU_H
#define CPU_H

typedef unsigned char t_pixel_sw;

t_pixel_sw gen_pixel();
void pixel_processing(t_pixel_sw data_in, t_pixel_sw *data_out, int *data_out_vld);

#endif
