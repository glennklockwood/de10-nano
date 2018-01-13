create_clock -name clk -period "50MHz" [get_ports clock]

set_false_path -from * -to [get_ports {led dips[*]}]
