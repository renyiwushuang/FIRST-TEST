`include "gates7_structural.v"
module gates7_structural_test;
    reg a, b;
    gates7_structural g7 (a, b, f_and, f_or, f_nand, f_nor, f_xor, f_xnor);
    initial begin
        a = 0;
        b = 0;
    #1 $display (
        " a=%b",a," b=%b",b," f_and=%b",f_and,
        " f_or=%b",f_or," f_nand=%b",f_nand,
        " f_nor=%b",f_nor," f_xor=%b",f_xor,
        " f_xnor=%b",f_xnor);
    end
    initial begin
        $dumpfile("gates7_structral.vcd");
        $dumpvars;
    end
endmodule