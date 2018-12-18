#include <ac_int.h>
#include "video_buf.h"

/***************************************************************************
 Funkce video_buf realizuje Video buffer pro pixely pred tim, nez budou 
 zobrazeny na obrazovce. Interni obrazek je generova z rozlisenim 320x240
 pixelu a zobrazuje se na obrazovku s dvojnasobnym rozlisenim 640x480. Kazdy
 vstupni pixel se proto rozkopiruje na 4 vystupni pixely. Tato komponenta
 zajistuje bufferovani a rozkopirovavani techto vstupnich pixelu.

 Vstupy:
   in_data        vstupni pixel
   in_data_vld    informace o platnosti vstupniho pixelu
   vga_row        cislo radku pro VGA display
   vga_col        cislo sloupce pro VGA display
 Vystupy:
   out_data       vystupni pixel
   vga_enable     aktivace VGA kontroleru
   gen_pause      siglnal pro pozastaveni generatoru pixelu
***************************************************************************/
#pragma hls_design top

void video_buf(t_pixel &in_data, bool &in_data_vld, 
   ac_int<10,false> vga_row, ac_int<10,false> vga_col, 
   t_pixel &out_data, bool &vga_enable, bool &gen_pause){

   static t_pixel buffer[BUFFER_ROWS][BUFFER_COLS];
   static bool dummy = ac::init_array<AC_VAL_DC>((t_pixel*)buffer,BUFFER_ROWS*BUFFER_COLS); 

   static ac_int<2,false> row_in = 0;
   static ac_int<10, false>  col_in = 0;
   static bool vga_enable_int = false;
   ac_int<2,false> row_diff = 0;

   // Aktivace VGA kontroleru - po nacteni prvnich dvou radku
   if(row_in == 2)
      vga_enable_int = true;

   // Precteni vystupniho pixelu pro VGA
   out_data = buffer[vga_row.slc<2>(1)][vga_col.slc<9>(1)];
   vga_enable = vga_enable_int;

   // Pozastaveni generatoru pixelu
   if (row_in >= vga_row.slc<2>(1))
      row_diff = row_in - vga_row.slc<2>(1); 
   else
      row_diff = BUFFER_ROWS - vga_row.slc<2>(1) + row_in; 

   gen_pause = (row_diff == 3);

   // Zpracovani vstupniho pixelu
   if (in_data_vld) {
      // Ulozeni vstupniho pixelu do bufferu      
      buffer[row_in][col_in] = in_data;

      // Aktualizace ukazovatka
      if (col_in == BUFFER_COLS-1) {
         col_in = 0;
         row_in++;
      }
      else
         col_in++;
   } 
}

