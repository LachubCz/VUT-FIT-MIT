#include "genpix.h"

#include <cstdlib>
#include <iostream>
using namespace std;
#include "mc_scverify.h"
#include "../../cpu/common.h"
#include "../../cpu/cpu.h"

/***************************************************************************
***************************************************************************/
CCS_MAIN(int argv, char *argc){
   t_pixel pixel = 0;
   t_pixel_sw pixel_sw = 0;
   bool req = true, pause = false, next, valid;

   for(int i=0; i<100000; i++) {
      if (i > 0)
         req = ((rand() % 2) == 0);
      pause = ((rand() % 2) == 0);
      next = req && (!pause);
      CCS_DESIGN(genpix)(pause, next, pixel, valid);
      if (next) {
         pixel_sw = gen_pixel();
         if(pixel_sw != pixel) {
            cout << "ERROR: ("<< i << ": " << (int)pixel << "/" << (int)pixel_sw << ") ";
            CCS_RETURN(1);
         }
      }
   }
   
   cout << "Done" << endl;

   CCS_RETURN(0);
}
 
