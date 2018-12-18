#include <ac_int.h>
#include "../../cpu/common.h"
#include "genpix.h"

#ifndef CCS_DUT_SYSC
#ifndef CCS_DUT_RTL
const int img_size[4] = {8,16,32,64};
const int prime_num[16] = {919, 929, 937, 941, 947, 953, 967, 971, \
                           977, 983, 991, 997, 1009, 1013, 1019, 1021};
#endif
#endif

/***************************************************************************
 Procedura update_base_pos zajistuje aktualizaci bazove pozice, ktera posouva
 objekt po obrazovce
***************************************************************************/
void update_base_pos(t_pix_pos &base_r, t_pix_pos &base_c) {

   static ac_int<2,true> inc_r = 1, inc_c = 1;

   if (base_r == BASE_LST_ROW) {
         inc_r = -1;
   }
   else if (base_r == BASE_FST_ROW) {
         inc_r = 1;
   }

   if (base_c == BASE_LST_COL) {
         inc_c = -1;
   }
   else if (base_c == BASE_FST_COL) {
         inc_c = 1;
   }

   base_r += inc_r;
   base_c += inc_c;
}

/***************************************************************************
 Procedura genpix realizuje generator pixelu
 Vstupy:
   pause       pozadavek na pozastaveni generatoru
   req         pozadavek na novy pixel
 Vystupy:
   pixel       vystupni pixel
   pixel_vld   informace o platnosti vystupniho pixelu
***************************************************************************/
#pragma hls_design top

void genpix(bool &pause, bool &req, t_pixel &pixel, bool &pixel_vld){

   static t_pix_pos           r=0, c=0;
   static t_pix_pos           base_r=100, base_c=100;
   static ac_int<10,false>    noise_cnt = 0;
   static ac_int<6,false>     frame_cnt = 0;
   static bool                init = true;
   ac_int<4,false>            diff_aux;
   t_pixel                    pixel_int, noise_pix;
   t_pix_pos                  diff_r, diff_c; 
   t_pixel                    diff;

   // vypocet rozdilu aktualni pozice vuci bazove pozici
   diff_r = r - base_r;
   diff_c = c - base_c;
   diff = (diff_r > diff_c) ? diff_r.slc<3>(NUM1) : diff_c.slc<3>(NUM1);
   diff = ~diff;
   diff_aux = diff + frame_cnt.slc<3>(3);
   diff = (diff_aux > MAX_PIXEL) ? (t_pixel)MAX_PIXEL : diff_aux.slc<3>(0);

   // vykresli pixel pokud je v blizkosti bazovych souradnic
   if ((diff_c < IMG_SIZE) && (diff_r < IMG_SIZE))
      pixel_int = diff;
   else
      pixel_int = MIN_PIXEL;

   noise_pix = (noise_cnt == NOISE_INTERVAL-1) ? (t_pixel)MAX_PIXEL : (t_pixel)MIN_PIXEL;
   pixel_int |= noise_pix;

   if (req || init) {
      // aktualizace aktualnich souradnic
      if (c == FRAME_COLS-1) {
         c = 0;
         if (r == FRAME_ROWS-1) {
            r = 0;
            // na konci smiku - aktualizace bazovych souradnic
            update_base_pos(base_r, base_c);
            frame_cnt++;
         }
         else
            r++;
      }
      else
         c++;

      // citac sumu
      noise_cnt = (noise_cnt == NOISE_INTERVAL-1) ? (ac_int<10,false>)0 : (ac_int<10,false>)(noise_cnt+1);

      pixel = pixel_int;
   }

   pixel_vld = (!pause);
   init = false;
}

