#include <stdio.h>
#include "common.h"
#include "cpu.h"

/***************************************************************************
 Hlavni program zajistuje generovani vstupnich pixelu a volani funkce pro
 jejich zpracovani.
***************************************************************************/
int main(int argc, char *argv[]){

   int         r, c, f;
   t_pixel_sw  pix_input, pix_output;
   int         pix_output_vld;

   for (f = 0; f < FRAMES; f++) {
      for (r = 0; r < FRAME_ROWS; r++) {
         for (c = 0; c < FRAME_COLS; c++) {
            pix_input = gen_pixel();
            pixel_processing(pix_input, &pix_output, &pix_output_vld);
         }
      }
   }

   return 0;
}

