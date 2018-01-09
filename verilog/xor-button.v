/*
 *  Implement a physical XOR on DE10-Nano using the KEY0 and KEY1 buttons as
 *  inputs and LED0 as output.
 *
 *  Code from ftp://ftp.altera.com/up/pub/Intel_Material/16.1/Tutorials/Verilog/Quartus_II_Introduction.pdf
 *
 */
module light (x1, x2, f);
    input x1, x2;
    output f;
    assign f = (x1 & ~x2) | (~x1 & x2);
endmodule
