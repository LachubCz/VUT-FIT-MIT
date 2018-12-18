#include "video_buf.h"

#include <iostream>
using namespace std;
#include "mc_scverify.h"

#define FRAME_ROWS   480
#define FRAME_COLS   640

CCS_MAIN(int argv, char *argc){
   t_pixel pix_in = 0, pix_out;
   bool pix_in_vld = true, vga_enable=false, vga_enable_prev=false, gen_pause=false;
   int vga_r=0, vga_c=0;

   for(int r=0; r<FRAME_ROWS; r++) {
      for(int c=0; c<FRAME_COLS; c++) {
         pix_in_vld = !gen_pause;
         CCS_DESIGN(video_buf)(pix_in, pix_in_vld, vga_r, vga_c, pix_out, vga_enable, gen_pause);
         cout << "("<< r << "," << c << ": " << pix_in << "/" << vga_enable << " - " << vga_r << "," << vga_c << ": " << pix_out << "/" << gen_pause << ") ";
         if (!gen_pause)
            pix_in++;

         // Aktualizace radku a sloupce VGA rozhrani
         if (vga_enable_prev) {
            if(vga_c == FRAME_COLS-1) {
               vga_c=0;
               vga_r = (vga_r == FRAME_ROWS-1) ? 0 : vga_r+1;
            }
            else
               vga_c++;
         }
         vga_enable_prev = vga_enable;
      }
      cout << endl;
   }

   
   CCS_RETURN(0);
}
 
