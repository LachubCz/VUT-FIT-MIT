#ifndef COMMON_H
#define COMMON_H

#define FRAME_COLS      320
#define FRAME_ROWS      240
#define FRAMES          501
#define PIXELS          8 
#define MAX_PIXEL       (PIXELS-1)
#define MIN_PIXEL       0
#define PIXEL_WIDTH     3

/* Vypocet parametru generatoru na zaklade loginu */
#define LOGIN           "xbucha02"
#define NUM1            (LOGIN[0]+LOGIN[1]+LOGIN[2]+LOGIN[3]) % 4 
#define NUM2            (LOGIN[4]+LOGIN[5]+LOGIN[6]+LOGIN[7]) % 16
#define IMG_SIZE        img_size[NUM1]
#define NOISE_INTERVAL  prime_num[NUM2]

/* Vypocet hranic pro pozici baze objektu */
#define BASE_FST_COL    0
#define BASE_LST_COL    FRAME_COLS-IMG_SIZE
#define BASE_FST_ROW    0
#define BASE_LST_ROW    FRAME_ROWS-IMG_SIZE

extern const int img_size[4];
extern const int prime_num[16];

#endif
