#include <fitkitlib.h>
#include "../cpu/common.h"

#define PROFILE

const int img_size[4] = {8,16,32,64};
const int prime_num[16] = {919, 929, 937, 941, 947, 953, 967, 971, \
                           977, 983, 991, 997, 1009, 1013, 1019, 1021};

/* 1 tik casovace = 30,518 us */
#define TIMER_TICK 30.518

typedef unsigned char t_pixel_sw;

/* globalni promenne */
unsigned long global_time=0;


/*******************************************************************************
 * Aktualizace globalniho casu
*******************************************************************************/
void global_time_update() {

   static unsigned long act_time, prev_time = 0;

   CCTL0 &= ~CCIE;  // disable interrupt               

   act_time = TAR;

   if (act_time >= prev_time)
      global_time += (act_time - prev_time); // v ramci stejneho cyklu
   else
      global_time += (act_time + (65536 - prev_time)); // preteceni

   prev_time = act_time;

   CCTL0 = CCIE;  // enable interrupt               
}

/*******************************************************************************
 * Aktualizace globalniho casu
*******************************************************************************/
unsigned long get_time() {

   global_time_update();

   return global_time;
}

/*******************************************************************************
 * Obsluha preruseni casovace timer A0
*******************************************************************************/
interrupt (TIMERA0_VECTOR) Timer_A (void) {

   global_time_update();

   CCR0 += 0x80;
}

/*******************************************************************************
 * Vypis uzivatelske napovedy (funkce se vola pri vykonavani prikazu "help")
*******************************************************************************/
void print_user_help(void) {
}

/*******************************************************************************
 * Dekodovani uzivatelskych prikazu a jejich vykonavani
*******************************************************************************/
unsigned char decode_user_cmd(char *cmd_ucase, char *cmd) {
   return (CMD_UNKNOWN);
}

/*******************************************************************************
 * Inicializace periferii/komponent po naprogramovani FPGA
*******************************************************************************/
void fpga_initialized() {
}

/***************************************************************************
 Procedura update_base_pos zajistuje aktualizaci bazove pozice, ktera posouva
 objekt po obrazovce
***************************************************************************/
void update_base_pos(unsigned int *base_r, unsigned int *base_c) {

   static int inc_r = 1, inc_c = 1;

   if (*base_r == BASE_LST_ROW) {
         inc_r = -1;
   }
   else if (*base_r == BASE_FST_ROW) {
         inc_r = 1;
   }

   if (*base_c == BASE_LST_COL) {
         inc_c = -1;
   }
   else if (*base_c == BASE_FST_COL) {
         inc_c = 1;
   }

   *base_r = (*base_r) + inc_r;
   *base_c = (*base_c) + inc_c;
}

/***************************************************************************
 Funkce gen_pixel() zajistuje generovani vstupnich pixelu.

 Vstupy
   frame_inc   pocet sminku, o ktere se ma generator pixelu posunout vpred.
               Pouze pro ucely simulace algoritmu na mikrokontroleru, ktery 
               ma nizky vypocetni vykon.

 Vystupy:
   navratova hodnota reprezentuje nove vygenerovany pixel
***************************************************************************/
t_pixel_sw gen_pixel(unsigned int frame_inc) {

   static unsigned int        r=0, c=0, base_r=100, base_c=100;
   static unsigned int        noise_cnt = 0, frame_cnt = 0;
   t_pixel_sw                 pixel_int, noise_pix, diff, diff_pix;
   unsigned int               diff_r, diff_c, i; 
   unsigned long              noise_inc;

   /* posun generatoru o nekolik smimku vpred */
   if(frame_inc > 0) {
      for (i = 0; i < frame_inc; i++)
         update_base_pos(&base_r, &base_c);
      noise_inc = (long)FRAME_ROWS*(long)FRAME_COLS*(long)frame_inc;
      noise_cnt =  (noise_cnt + noise_inc) % NOISE_INTERVAL;
      frame_cnt += frame_inc;
      return 0;
   }

   /* vypocet rozdilu aktualni pozice vuci bazove pozici */
   diff_r = r - base_r;
   diff_c = c - base_c;
   diff = (diff_r > diff_c) ? (diff_r >> NUM1) : (diff_c >> NUM1);
   diff = ~diff & MAX_PIXEL;
   diff_pix = diff + ((frame_cnt >> 3) & MAX_PIXEL);
   if (diff_pix > MAX_PIXEL)
      diff_pix = MAX_PIXEL;

   /* vykresli pixel pokud je v blizkosti bazovych souradnic */
   if ((diff_c < IMG_SIZE) && (diff_r < IMG_SIZE))
      pixel_int = diff_pix;
   else
      pixel_int = MIN_PIXEL;

   noise_pix = (noise_cnt == NOISE_INTERVAL-1) ? MAX_PIXEL : MIN_PIXEL;

   pixel_int |= noise_pix;

   /* aktualizace aktualnich souradnic */
   if (c == FRAME_COLS-1) {
      c = 0;
      if (r == FRAME_ROWS-1) {
         r = 0;
         /* na konci smiku - aktualizace bazovych souradnic */
         update_base_pos(&base_r, &base_c);
         frame_cnt++;
      }
      else
         r++;
   }
   else
      c++;

   /* citac sumu */
   noise_cnt =  (noise_cnt == NOISE_INTERVAL-1) ? 0 : noise_cnt+1;

   return pixel_int;
}

/*******************************************************************************
 * Hlavni funkce
*******************************************************************************/
int main(void)
{
   short counter = 0;
   unsigned long start_time, end_time;

   initialize_hardware();
   set_led_d6(1);  //rozsvitit LED D6
   set_led_d5(1);  //rozsvitit LED D5

   /* nastaveni casovace na periodu 10 ms */
   CCTL0 = CCIE;  // enable interrupt               
   CCR0 = 0x80;
   TACTL = TASSEL_1 + MC_2;

   /**************************************************************************/
   /*                      Puvodni hlavni program                            */
   /**************************************************************************/
   // Modifikovanou cast puvodniho hlavniho programu vlozte zde

#ifdef PROFILE
   // Demo priklad pro mereni casu
   start_time = get_time();
   delay_ms(100);
   end_time = get_time();

   term_send_str("Time diff (us): ");
   term_send_num((long)(((float)(end_time-start_time))*TIMER_TICK));
   term_send_crlf();
#endif
   
   CCTL0 &= ~CCIE;  // disable interrupt
   /**************************************************************************/

   set_led_d5(0);  //zhasnout LED D5

   while (1) {
      delay_ms(1);  //zpozdeni 1ms

      counter++;
      if (counter == 500) {
         flip_led_d6(); //invertovat LED
         counter = 0;
      }

      terminal_idle();  // obsluha terminalu
   }
}

