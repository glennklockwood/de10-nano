/*
 * Based on the "Your First FPGA" Tutorial here:
 *
 * https://software.intel.com/en-us/articles/how-to-program-your-first-fpga-device
 *
 */
module blink (clk, LED);
    input wire clk;         /* 50 MHz input clock */
    output wire LED;   /* output LEDs */
    reg [31:0] cnt;         /* 32-bit counter */

    initial begin
        cnt <= 32'h0; /* start at zero */
    end

    /*
     * 50 MHz = do the following 50,000,000 times per sec
     */
    always @(posedge clk) begin
        cnt <= cnt + 1;
    end

    /*
     * 2**32 is about 4.3 billion, so at 50 MHz, it will take 85 seconds to
     * overflow cnt 
     */
    assign LED = cnt[24];
endmodule
