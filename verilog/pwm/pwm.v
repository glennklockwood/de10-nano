/*
 * Demonstrate PWM with Verilog
 *
 */
module pwm(clock, dips, led);
    input wire clock;       /* 50 MHz clock */
    input wire dips[3:0];   /* four slide switches */
    output wire led;        /* output LED */
    reg [15:0] count;       /* counter register to increment on each clock */
    reg [15:0] duty;        /* when count > duty, LED is on */

    initial begin
        count <= 16'b0;
        duty <= 16'b0;
    end

    /* 
     * Reminder: DE10-Nano's 50 MHz clock = 20 ns per clock 
     *
     *    8-bit register = 5.12 us between overflows (195.3 kHz)
     *   16-bit register = 1.31 ms between overflows (762.9 Hz)
     *
     * 762.9 Hz switching time seems to work well for a standard LED
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
     *   0000 = 100.0% duty cycle
     *   0001 = 92.75% duty cycle
     *   0010 = 87.50% duty cycle
     *   0100 = 75.00% duty cycle
     *   1000 = 50.00% duty cycle
     *   1100 = 25.00% duty cycle
     *   1110 = 12.50% duty cycle
     *   1111 =  6.25% duty cycle
     */
    assign duty[15] = dips[3];
    assign duty[14] = dips[2];
    assign duty[13] = dips[1];
    assign duty[12] = dips[0];
endmodule
