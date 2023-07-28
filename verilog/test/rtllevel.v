module mux2x32 (
    a0,a1,s,y
);
    input [31:0] a0,a1;
    input s;
    output [21:0] y;
    assign y = s? a1 : a0;
endmodule

module mux4x32 (
    a0,a1,a2,a3,s,y
);
    input [31:0] a0,a1,a2,a3;
    input [1:0] s;
    output [31:0] y;
    function [31:0] select;
        input [31:0] a0,a1,a2,a3;
        input [1:0] s;
        case (s)
            2'b00: select = a0;
            2'b01: select = a1;
            2'b10: select = a2;
            2'b11: select = a3;
        endcase
    endfunction
    assign y = select(a0,a1,a2,a3,s);
endmodule

module decoder3e (
    n,ena,e
);
    input [2:0] n;
    input ena;
    output [7:0] e;
    reg [7:0] e;
    always @(ena or n) begin
        e = 8'b0;
        e[n] = ena;
    end
endmodule

module shift (
    d,sa,right,arith,sh
);
    input [31:0] d;
    input [4:0] sa;
    input right, arith;
    output [31:0] sh;
    reg [31:0] sh;
    always @* begin
        if (!right) begin
            sh = d << sa;
        end else if (!arith) begin
            sh = d >> sa;
        end else begin
            sh = $signed(d) >>> sa;
        end
    end
endmodule

