-- testbench.vhd: Testbench file
-- Author(s): Tomas Martinek <martinto at fit.vutbr.cz>
--
library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_arith.all;
use ieee.std_logic_unsigned.all;
use ieee.std_logic_textio.all;
use ieee.numeric_std.all;
use std.textio.all;

-- ----------------------------------------------------------------------------
--                        Entity declaration
-- ----------------------------------------------------------------------------
entity testbench is
end entity testbench;

-- ----------------------------------------------------------------------------
--                      Architecture declaration
-- ----------------------------------------------------------------------------
architecture behavioral of testbench is

   -- hodiny
   signal smclk     : std_logic;
   signal aclk      : std_logic;
   signal fclk      : std_logic;
   signal clk       : std_logic;

   signal reset     : std_logic;
   signal irq       : std_logic := 'Z';

   -- LED
   signal ledf      : std_logic;

   -- interni SPI
   signal spi_cs    : std_logic;
   signal spi_di    : std_logic;
   signal spi_di_req: std_logic;
   signal spi_do    : std_logic;
   signal spi_do_vld: std_logic;

   -- klavesnice 4x4
   signal kin       : std_logic_vector(3 downto 0);
   signal kout      : std_logic_vector(3 downto 0);

   -- display
   signal le        : std_logic;
   signal lrs       : std_logic;
   signal lrw       : std_logic;
   signal ld        : std_logic_vector(7 downto 0) := (others => 'Z');

   -- SDRAM
   signal ra        : std_logic_vector(14 downto 0);
   signal rd        : std_logic_vector(7 downto 0) := (others => 'Z');
   signal rdqm      : std_logic;
   signal rcs       : std_logic;
   signal rras      : std_logic;
   signal rcas      : std_logic;
   signal rwe       : std_logic;
   signal rclk      : std_logic;
   signal rcke      : std_logic;

   -- P3M
   signal p3m       : std_logic_vector(7 downto 0) := (others => 'Z');

   -- AFBUS
   signal afbus     : std_logic_vector(11 downto 0) := (others => 'Z');

   -- VGA
   signal blue_v    : std_logic_vector(2 downto 0);
   signal green_v   : std_logic_vector(2 downto 0);
   signal red_v     : std_logic_vector(2 downto 0);
   signal vsync_v   : std_logic;
   signal hsync_v   : std_logic;

   -- PS/2
   signal m_data    : std_logic := 'Z';
   signal m_clk     : std_logic := 'Z';
   signal k_data    : std_logic := 'Z';
   signal k_clk     : std_logic := 'Z';

   -- RS232 (DTE device)
   signal rxd_232   : std_logic;
   signal txd_232   : std_logic;
   signal rts_232   : std_logic;
   signal cts_232   : std_logic;

   -- unused X
   signal x         : std_logic_vector(26 downto 6);

   -- audio codec
   signal alrcin    : std_logic := 'Z';
   signal adin      : std_logic;
   signal alrcout   : std_logic := 'Z';
   signal adout     : std_logic    := 'Z';
   signal abclk     : std_logic := 'Z';

   constant smclkper  : time := 135.6 ns;
   constant clkper    : time := 40 ns;

-- ----------------------------------------------------------------------------
--                      Architecture body
-- ----------------------------------------------------------------------------
begin

uut : entity work.tlv_pc_ifc
port map(
   -- hodiny
   SMCLK     => smclk,
   ACLK      => aclk,
   FCLK      => fclk,
   CLK       => clk,

   RESET     => reset,
   IRQ       => irq,

   -- LED
   LEDF      => ledf,

   -- interni SPI
   SPI_CS    => spi_cs,
   SPI_DI    => spi_di,
   SPI_DI_REQ=> spi_di_req,
   SPI_DO    => spi_do,
   SPI_DO_VLD=> spi_do_vld,

   -- klavesnice 4x4
   KIN       => kin,
   KOUT      => kout,

   -- display
   LE        => le,
   LRS       => lrs,
   LRW       => lrw,
   LD        => ld,

   -- SDRAM
   RA        => ra,
   RD        => rd,
   RDQM      => rdqm,
   RCS       => rcs,
   RRAS      => rras,
   RCAS      => rcas,
   RWE       => rwe,
   RCLK      => rclk,
   RCKE      => rcke,

   -- P3M
   P3M       => p3m,

   -- AFBUS
   AFBUS     => afbus,

   -- VGA
   BLUE_V    => blue_v,
   GREEN_V   => green_v,
   RED_V     => red_v,
   VSYNC_V   => vsync_v,
   HSYNC_V   => hsync_v,

   -- PS/2
   M_DATA    => m_data,
   M_CLK     => m_clk,
   K_DATA    => k_data,
   K_CLK     => k_clk,

   -- RS232 (DTE device)
   RXD_232   => rxd_232,
   TXD_232   => txd_232,
   RTS_232   => rts_232,
   CTS_232   => cts_232,

   -- unused X
   X         => x,

   -- audio codec
   ALRCIN    => alrcin,
   ADIN      => adin,
   ALRCOUT   => alrcout,
   ADOUT     => adout,
   ABCLK     => abclk
);

-- -------------------------------------------------------------
-- smclkf clock generator
smclkfgen : process
begin
   smclk <= '1';
   wait for smclkper/2;
   smclk <= '0';
   wait for smclkper/2;
end process;

-- -------------------------------------------------------------
-- clk clock generator
clkfgen : process
begin
   clk <= '1';
   wait for clkper/2;
   clk <= '0';
   wait for clkper/2;
end process;


-- ----------------------------------------------------------------------------
--                         Main testbench process
-- ----------------------------------------------------------------------------
tb : process

begin
   reset <= '1';
   wait for 220 ns;
   reset <= '0';

   wait;
end process;

end architecture behavioral;

