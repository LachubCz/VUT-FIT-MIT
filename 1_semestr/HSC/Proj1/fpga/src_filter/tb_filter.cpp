#include "filter.h"
#include "addr_space.h"
#include "../cpu/common.h"

#include <iostream>
using namespace std;
#include "mc_scverify.h"
#include "../cpu/cpu.h"

extern int otsu(int *hist, int n);

/***************************************************************************
 Hlavni program Testbench souboru. Zajistuje generovani vstupnich pixelu,
 volani puvodniho (referencniho) kodu a modifikovaneho kodu a porovnani
 jejich vystupu.
***************************************************************************/
CCS_MAIN(int argv, char *argc){
   t_pixel pix_in_hw, pix_out_hw = 0;
   t_pixel_sw pix_in_sw, pix_out_sw = 0;
   int pix_out_sw_vld;
   bool valid = true, non_valid = false;
   t_mcu_data mcu_data[MCU_SIZE];
   int new_frame, prev_frame=0, threshold;
   int histogram[PIXELS];

   // Inicializace sdilene pameti
   for(int i=0;i<MCU_SIZE;i++)
      mcu_data[i] = 0;
   mcu_data[FPGA_MCU_READY] = 1;

   // Cekani na synchronizaci FPGA - MCU
   while(mcu_data[FPGA_MCU_READY]!=2)
      CCS_DESIGN(filter)(pix_in_hw, non_valid, pix_out_hw, mcu_data); 

   // Test filtrace pixelu
   for(int f=0;f<FRAMES;f++){
      for(int r=0;r<FRAME_ROWS;r++){
         for(int c=0;c<FRAME_COLS;c++){
            /* Generovani vstupniho pixelu */
            pix_in_sw = gen_pixel();
            pix_in_hw = (t_pixel)pix_in_sw;
            /* Volani puvodniho (referencniho) kodu */
            pixel_processing(pix_in_sw, &pix_out_sw, &pix_out_sw_vld); 
            /* Volani modifikovaneho kodu */
            CCS_DESIGN(filter)(pix_in_hw, valid, pix_out_hw, mcu_data); 

            /* Porovnani vysledku referencniho vs. modifikovaneho kodu */
            if(pix_out_sw_vld && (pix_out_hw != pix_out_sw)) {
                  cout << endl << "ERROR: Chyba na pozici: (" << (f+1) << ":" << (r+1) << "," << (c+1) << "), ";
                  cout << "In: out_sw/out_hw = " << pix_in_hw << ": " << (int)pix_out_sw << "/" << pix_out_hw <<  endl;
                  CCS_RETURN(1);
            } 
         }
      }

      // Simulace chovani MCU
      new_frame = (int)mcu_data[FPGA_FRAME_CNT];
      if((new_frame != prev_frame) && (new_frame % 10) == 0) {

         for(int k=0; k<PIXELS; k++) {
            histogram[k] = (int)mcu_data[k];
            mcu_data[k] = 0;
         }
         threshold = otsu(histogram, PIXELS);

         mcu_data[FPGA_THRESHOLD] = threshold;
         prev_frame = new_frame;
      }
   }
   cout << "INFO: ***********************************************************" << endl;
   cout << "INFO: Test referencniho kodu oproti upravenemu probehl v poradku." << endl;
   cout << "INFO: ***********************************************************" << endl;
   CCS_RETURN(0);
}
 
