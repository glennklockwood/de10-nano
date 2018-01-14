/*
 * blink an LED on and off
 *
 */
module blink (clk, led);
    input wire clk;     /* 50 MHz input clock */
    output wire led;    /* output LED */
    reg [31:0] cnt;     /* 32-bit counter */

    initial begin
        cnt <= 32'b0; /* start at zero */
    end

    /*
     * 50 MHz = do the following 50,000,000 times per sec
     */
    always @(posedge clk) begin
        cnt <= cnt + 1;
    end

    /*
     * 2**32 is about 4.3 billion, so at 50 MHz, it will take 85 seconds to
     * overflow cnt.  2**24 is about 16.8 million though, so cnt[24] will
     * be 1 after 0.34 seconds.
     */
    assign led = cnt[24];
endmodule
