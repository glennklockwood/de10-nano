/*
 * demonstrate PWM with Verilog
 */
module pwm(clock, dips, led);
    input wire clock;
    input wire dips[3:0];
    output wire led;
    reg [15:0] count;
    reg [15:0] duty;

    initial begin
        count <= 16'b0;
        duty <= 16'b0;
    end

    /* 
     * 50 MHz clock = 20 ns per clock 
     * 8-bit register = 5.12 us between overflows (195.3 kHz)
     * 16-bit register = 1.31 ms between overflows (762.9 Hz)
     */
    always @(posedge clock) begin
        count = count + 1'b1;
        if (count > duty)
            led <= 1'b1;
        else
            led <= 1'b0;
    end

    /*
     * four dip switches control the most significant bits of duty
     */
    assign duty[15] = dips[3];
    assign duty[14] = dips[2];
    assign duty[13] = dips[1];
    assign duty[12] = dips[0];
endmodule
