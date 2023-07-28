`include "transistorlevel.v"
module cmosnot_test;
    reg  a;
    wire f;
    cmosnot not_1 (f,a);
    initial begin
        a=1;
    #1 a = 0;
    #1 a = 1;
    #1 $finish;
    end
    initial begin
        $monitor ($time,": a = %b;",a," f = %b;", f);
        $dumpfile("cmosnot.vcd");
        $dumpvars;
    end
endmodule