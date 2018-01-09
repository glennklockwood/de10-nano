/*
 * Based on the "Your First FPGA" Tutorial here:
 *
 * https://software.intel.com/en-us/articles/how-to-program-your-first-fpga-device
 *
 */
module blink ( clk, LED );
    input wire clk;         /* 50 MHz input clock */
    output wire LED[7:0];   /* eight output LEDs */
    reg [31:0] cnt;         /* 32-bit counter */

    initial begin
        cnt <= 32'h00000000; /* start at zero */
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
    assign LED[0] = cnt[24]; /* 2**24 / 50e6 = turn on after 0.34 sec */
    assign LED[1] = cnt[25]; /* 2**25 / 50e6 = turn on (and turn off previous) after 0.67 sec */
    assign LED[2] = cnt[26];
    assign LED[3] = cnt[27];
    assign LED[4] = cnt[28]; /* 2**28 / 50e6 = 5.36 sec */
    assign LED[5] = cnt[29];
    assign LED[6] = cnt[30];
    assign LED[7] = cnt[31];
endmodule
