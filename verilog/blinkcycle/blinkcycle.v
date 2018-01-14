/*
 * blinkcycle - cycle through LEDs 0-7
 */

module blinkcycle(clk, sw3, LED);
    input wire clk;       /* 50 MHz clock */
    input wire sw3;       /* slide switch #3 toggles forward/reverse iteration */
    output wire LED[7:0]; /* eight output LEDs */
    reg [31:0] cnt;
    reg [2:0] state;

    initial begin
        cnt <= 32'b0;
        state <= 3'b0;
    end

    always @(posedge clk) begin
        cnt = cnt + 1'b1;
        /* increment state by 1 when the lower 23 bits of cnt are all 1 */
        if (sw3 & 1'b1) begin
            state <= state + &(cnt[22:0] & ~23'h0);
        /* decrement state if sw3 is off */
        end else begin
            state <= state - &(cnt[22:0] & ~23'h0);
        end
    end

    assign LED[0] = &(3'd7 == state);
    assign LED[1] = &(3'd6 == state);
    assign LED[2] = &(3'd5 == state);
    assign LED[3] = &(3'd4 == state);
    assign LED[4] = &(3'd3 == state);
    assign LED[5] = &(3'd2 == state);
    assign LED[6] = &(3'd1 == state);
    assign LED[7] = &(3'd0 == state);
endmodule
