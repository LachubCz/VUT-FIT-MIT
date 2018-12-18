-- top_level.vhd: Top Level soubor pro FPGA
-- Copyright (C) 2012 Brno University of Technology,
--                    Faculty of Information Technology
-- Author(s): Tomas Martinek <martinto AT fit.vutbr.cz>
--
-- LICENSE TERMS
--
-- Redistribution and use in source and binary forms, with or without
-- modification, are permitted provided that the following conditions
-- are met:
-- 1. Redistributions of source code must retain the above copyright
--    notice, this list of conditions and the following disclaimer.
-- 2. Redistributions in binary form must reproduce the above copyright
--    notice, this list of conditions and the following disclaimer in
--    the documentation and/or other materials provided with the
--    distribution.
-- 3. All advertising materials mentioning features or use of this software
--    or firmware must display the following acknowledgement:
--
--      This product includes software developed by the University of
--      Technology, Faculty of Information Technology, Brno and its
--      contributors.
--
-- 4. Neither the name of the Company nor the names of its contributors
--    may be used to endorse or promote products derived from this
--    software without specific prior written permission.
--
-- This software or firmware is provided ``as is'', and any express or implied
-- warranties, including, but not limited to, the implied warranties of
-- merchantability and fitness for a particular purpose are disclaimed.
-- In no event shall the company or contributors be liable for any
-- direct, indirect, incidental, special, exemplary, or consequential
-- damages (including, but not limited to, procurement of substitute
-- goods or services; loss of use, data, or profits; or business
-- interruption) however caused and on any theory of liability, whether
-- in contract, strict liability, or tort (including negligence or
-- otherwise) arising in any way out of the use of this software, even
-- if advised of the possibility of such damage.
--
-- $Id$
--
--

library IEEE;
library UNISIM;
use IEEE.std_logic_1164.ALL;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use work.vga_controller_cfg.all; 
use UNISIM.vcomponents.all;

-- pragma translate_off 
use ieee.std_logic_textio.all;
use std.textio.all;

library unisim;
use unisim.vcomponents.all;
-- pragma translate_on 

architecture arch_beh of tlv_pc_ifc is

   -- VGA kontroler
   signal isettings   : std_logic_vector(60 downto 0);

   signal vga_hstate  : vga_hfsm_state;
   signal vga_vstate  : vga_vfsm_state;
   signal col_red     : std_logic_vector(2 downto 0) := (others => '0');
   signal col_green   : std_logic_vector(2 downto 0) := (others => '0');
   signal col_blue    : std_logic_vector(2 downto 0) := (others => '0');
   signal vga_row     : std_logic_vector(11 downto 0);
   signal vga_col     : std_logic_vector(11 downto 0);
   signal vga_color   : std_logic_vector(2 downto 0);
   signal vga_enable  : std_logic;

   -- Vstupy a vystupy pro medianovy filtr 
   signal pixel_pause            : std_logic;
   signal pixel_req              : std_logic;
   signal pixel                  : std_logic_vector(2 downto 0);
   signal pixel_vld              : std_logic;
   signal filter_out_data        : std_logic_vector(2 downto 0);
   signal filter_out_data_vld    : std_logic;

   -- Komunikacni rozhrani mezi MCU a FPGA
   type    t_spi_mcu_ram is array (511 downto 0) of std_logic_vector (31 downto 0);
   shared variable  spi_mcu_ram : t_spi_mcu_ram := (others => X"00000000");

   signal spi_bram_addr          : std_logic_vector(8 downto 0);
   signal spi_bram_data_out      : std_logic_vector(31 downto 0);
   signal spi_bram_data_in       : std_logic_vector(31 downto 0);
   signal spi_bram_we            : std_logic;
   signal spi_bram_en            : std_logic;
   signal spi_bram_data_out_mux  : std_logic_vector(31 downto 0);
   signal spi_bram_data_in_mux   : std_logic_vector(31 downto 0);

   signal mcu_bram_addr          : std_logic_vector(8 downto 0);
   signal mcu_bram_data_out      : std_logic_vector(31 downto 0);
   signal mcu_bram_data_in       : std_logic_vector(31 downto 0);
   signal mcu_bram_we            : std_logic;

component genpix
  PORT(
    clk : IN STD_LOGIC;
    rst : IN STD_LOGIC;
    pause_rsc_z : IN STD_LOGIC;
    req_rsc_z : IN STD_LOGIC;
    pixel_rsc_z : OUT STD_LOGIC_VECTOR (2 DOWNTO 0);
    pixel_vld_rsc_z : OUT STD_LOGIC
  );
end component;

component video_buf 
   port (
      in_data_rsc_z : IN std_logic_vector (2 DOWNTO 0) ;
      in_data_vld_rsc_z : IN std_logic ;
      vga_row_rsc_z : IN std_logic_vector (9 DOWNTO 0) ;
      vga_col_rsc_z : IN std_logic_vector (9 DOWNTO 0) ;
      out_data_rsc_z : OUT std_logic_vector (2 DOWNTO 0) ;
      vga_enable_rsc_z : OUT std_logic ;
      gen_pause_rsc_z : OUT std_logic ;
      clk : IN std_logic ;
      rst : IN std_logic) ;
end component;

component filter
  PORT(
    clk : IN STD_LOGIC;
    rst : IN STD_LOGIC;
    in_data_rsc_z : IN STD_LOGIC_VECTOR (2 DOWNTO 0);
    in_data_rsc_lz : OUT STD_LOGIC;
    in_data_vld_rsc_z : IN STD_LOGIC;
    out_data_rsc_z : OUT STD_LOGIC_VECTOR (2 DOWNTO 0);
    out_data_rsc_lz : OUT STD_LOGIC;
    mcu_data_rsc_adr : OUT STD_LOGIC_VECTOR (8 DOWNTO 0);
    mcu_data_rsc_q : IN STD_LOGIC_VECTOR (31 DOWNTO 0);
    mcu_data_rsc_d : OUT STD_LOGIC_VECTOR (31 DOWNTO 0);
    mcu_data_rsc_we : OUT STD_LOGIC
  );
end component;

begin

   ---------------------------------------------------------------------
   -- Graphic output control
   SetMode(r640x480x60, isettings);

   -- VGA
   vga: entity work.vga_controller
      generic map (REQ_DELAY => 2)
      port map (
         CLK    => CLK,
         RST    => RESET,
         ENABLE => vga_enable,
         MODE   => isettings,

         DATA_RED    => col_red,
         DATA_GREEN  => col_green,
         DATA_BLUE   => col_blue,
         ADDR_COLUMN => vga_col,
         ADDR_ROW    => vga_row,

         VGA_RED   => RED_V,
         VGA_BLUE  => BLUE_V,
         VGA_GREEN => GREEN_V,
         VGA_HSYNC => HSYNC_V,
         VGA_VSYNC => VSYNC_V,
      
         -- H/V Status
         STATUS_H  => vga_hstate,
         STATUS_V  => vga_vstate);

   ---------------------------------------------------------------------
   -- Pixel generator
   GENPIX_U: genpix
   port map(
      CLK               => CLK,
      RST               => RESET,

      PAUSE_RSC_Z       => pixel_pause,
      REQ_RSC_Z         => pixel_req,
      PIXEL_RSC_Z       => pixel,
      PIXEL_VLD_RSC_Z   => pixel_vld 
   );

   ---------------------------------------------------------------------
   -- Medianovy filtr a segmentace
    FILTER_U: filter
      port map(
      CLK                 => CLK,
      RST                 => RESET,

      -- Vstupni pixel
      IN_DATA_RSC_Z       => pixel,
      IN_DATA_RSC_LZ      => pixel_req,
      IN_DATA_VLD_RSC_Z   => pixel_vld,

      -- Vystupni pixel
      OUT_DATA_RSC_Z      => filter_out_data,
      OUT_DATA_RSC_LZ     => filter_out_data_vld,

      -- Komunikace MCU_FPGA
      MCU_DATA_RSC_D => mcu_bram_data_in,
      MCU_DATA_RSC_ADR => mcu_bram_addr,
      MCU_DATA_RSC_WE => mcu_bram_we,
      MCU_DATA_RSC_Q => mcu_bram_data_out
   );

   ---------------------------------------------------------------------
   -- Video buffer
   VIDEO_BUF_U: video_buf
   port map(
      CLK               => CLK,
      RST               => RESET,

      -- Vstupni pixel
      IN_DATA_RSC_Z     => filter_out_data,
      IN_DATA_VLD_RSC_Z => filter_out_data_vld,

      -- VGA rozhrani
      VGA_ROW_RSC_Z     => vga_row(9 downto 0),
      VGA_COL_RSC_Z     => vga_col(9 downto 0),
      OUT_DATA_RSC_Z    => vga_color,
      VGA_ENABLE_RSC_Z  => vga_enable,

      GEN_PAUSE_RSC_Z   => pixel_pause
   );
 
   col_red     <= vga_color;
   col_blue    <= vga_color;
   col_green   <= vga_color;

   ---------------------------------------------------------------------
   -- MCU - FPGA komunikace s vyuzitim SPI kontroleru
   spidecd: entity work.SPI_adc
      generic map (
         ADDR_WIDTH => 16,      -- sirka adresy 16 bitu
         DATA_WIDTH => 32,      -- sirka dat 16 bitu
         ADDR_OUT_WIDTH => 9,  -- sirka adresy k adresaci BRAM 10 bitu
         BASE_ADDR  => 16#0000# -- adresovy prostor od 0x0000 - 0x03FF
      )
      port map (
         CLK      => CLK,
         CS       => SPI_CS,

         DO       => SPI_DO,
         DO_VLD   => SPI_DO_VLD,
         DI       => SPI_DI,
         DI_REQ   => SPI_DI_REQ,

         ADDR     => spi_bram_addr,
         DATA_OUT => spi_bram_data_in_mux,
         DATA_IN  => spi_bram_data_out_mux,
         WRITE_EN => spi_bram_we,
         READ_EN  => spi_bram_en
   );

   -- Preusporadani bajtu v ramci vstupniho/vystupniho 32-bitoveho slova
   spi_bram_data_out_mux <= spi_bram_data_out(7 downto 0) &
                       spi_bram_data_out(15 downto 8) &
                       spi_bram_data_out(23 downto 16) &
                       spi_bram_data_out(31 downto 24);

   spi_bram_data_in <= spi_bram_data_in_mux(7 downto 0) &
                       spi_bram_data_in_mux(15 downto 8) &
                       spi_bram_data_in_mux(23 downto 16) &
                       spi_bram_data_in_mux(31 downto 24);

   ---------------------------------------------------------------------
   -- MCU - FPGA komunikace - dvouportova BlockRAM
   process (CLK)
   begin
      if (CLK'event and CLK = '1') then
         if (spi_bram_we = '1') then
            spi_mcu_ram(conv_integer(spi_bram_addr)) := spi_bram_data_in;
         end if;
         spi_bram_data_out <= spi_mcu_ram(conv_integer(spi_bram_addr));
      end if;
   end process;

   process (CLK)
   begin
      if (CLK'event and CLK = '1') then
         if (mcu_bram_we = '1') then -- active at low for Precision at high for Xilinx
            spi_mcu_ram(conv_integer(mcu_bram_addr)) := mcu_bram_data_in;
         end if;
         mcu_bram_data_out <= spi_mcu_ram(conv_integer(mcu_bram_addr));
      end if;
   end process;

end arch_beh;
