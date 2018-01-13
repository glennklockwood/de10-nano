/*
 * demonstrate PWM with Verilog
 */

module pwm(clock, LED);
    input wire clock;
    output wire LED;
    reg [31:0] count;

    initial begin
        count <= 32'b0;
    end

    always @(posedge clock) begin
        count <= count + 1'b1;
    end

    assign LED = count[24];
endmodule
