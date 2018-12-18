//  Catapult University Version 10.0c/745553 (Production Release) Wed Oct 11 16:38:17 PDT 2017
//  
//  Copyright (c) Mentor Graphics Corporation, 1996-2017, All Rights Reserved.
//                       UNPUBLISHED, LICENSED SOFTWARE.
//            CONFIDENTIAL AND PROPRIETARY INFORMATION WHICH IS THE
//          PROPERTY OF MENTOR GRAPHICS OR ITS LICENSORS
//  
//  Running on Windows 8 Fitkit@DESKTOP-NJUNEBJ  6.02 i686
//  
//  Package information: SIFLIBS v23.0_2.0, HLS_PKGS v23.0_1.0, 
//                       DesignPad v2.78_1.0
//  
//  This version may only be used for academic purposes.  Some optimizations 
//  are disabled, so results obtained from this version may be sub-optimal.
//  
solution new -state initial
solution options defaults
solution options set /Output/GenerateCycleNetlist false
solution file add {./src_filter/filter.h} -type CHEADER
solution file add {./src_filter/filter.cpp} -type C++
solution file add {./src_filter/addr_space.h} -type CHEADER
directive set -DESIGN_GOAL area
directive set -OLD_SCHED false
directive set -SPECULATE true
directive set -MERGEABLE true
directive set -REGISTER_THRESHOLD 256
directive set -MEM_MAP_THRESHOLD 32
directive set -FSM_ENCODING none
directive set -REG_MAX_FANOUT 0
directive set -NO_X_ASSIGNMENTS true
directive set -SAFE_FSM false
directive set -ASSIGN_OVERHEAD 0
directive set -UNROLL no
directive set -IO_MODE super
directive set -REGISTER_IDLE_SIGNAL false
directive set -IDLE_SIGNAL {}
directive set -STALL_FLAG false
directive set -TRANSACTION_DONE_SIGNAL false
directive set -DONE_FLAG {}
directive set -READY_FLAG {}
directive set -START_FLAG {}
directive set -BLOCK_SYNC none
directive set -TRANSACTION_SYNC ready
directive set -DATA_SYNC none
directive set -RESET_CLEARS_ALL_REGS true
directive set -CLOCK_OVERHEAD 40.000000
directive set -OPT_CONST_MULTS use_library
directive set -CHARACTERIZE_ROM false
directive set -PROTOTYPE_ROM true
directive set -ROM_THRESHOLD 64
directive set -CLUSTER_ADDTREE_IN_COUNT_THRESHOLD 0
directive set -CLUSTER_OPT_CONSTANT_INPUTS true
directive set -CLUSTER_RTL_SYN false
directive set -CLUSTER_FAST_MODE false
directive set -CLUSTER_TYPE combinational
directive set -COMPGRADE fast
go new
directive set -DESIGN_HIERARCHY filter__FR31ac_int__tm__17_XCiL_1_3XCbL_1_0RbT1P32ac_int__tm__18_XCiL_2_32XCbL_1_0
go compile
solution library add mgc_Xilinx-SPARTAN3-4_beh_xst -- -rtlsyntool Xilinx -manufacturer Xilinx -family SPARTAN3 -speed -4 -part 3s50tq144
solution library add Xilinx_RAMS
go libraries
directive set -CLOCKS {clk {-CLOCK_PERIOD 40.0 -CLOCK_EDGE rising -CLOCK_UNCERTAINTY 0.0 -CLOCK_HIGH_TIME 20.0 -RESET_SYNC_NAME rst -RESET_ASYNC_NAME arst_n -RESET_KIND sync -RESET_SYNC_ACTIVE high -RESET_ASYNC_ACTIVE low -ENABLE_ACTIVE high}}
go assembly
directive set /filter/core/main -PIPELINE_INIT_INTERVAL 2
directive set /filter/out_data:rsc -MAP_TO_MODULE mgc_ioport.mgc_out_stdreg_en
directive set /filter/in_data:rsc -MAP_TO_MODULE mgc_ioport.mgc_in_wire_en
directive set /filter/mcu_data:rsc -MAP_TO_MODULE Xilinx_RAMS.BLOCK_SPRAM_RBW
go architect
go extract
