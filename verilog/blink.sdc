create_clock -name clk -period "50MHz" [get_ports clk]
set_false_path -from * -to [get_ports LED]
