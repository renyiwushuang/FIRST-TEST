`include "rtllevel.v"
module decoder3e_test;
    reg [2:0] n;
    reg ena;
    wire [7:0] e;
    integer i;
    decoder3e dec3e (n,ena,e);
    initial begin
        #0 $display("time\tena\tn\te");
        #0 ena = 1; n = 0;
        for (i = 1;i < 8;i = i+1) begin
            #1 n = i;
        end
        #1 ena = 0;
        #1 ena = 1; n = 0;
        #1 $finish;
    end
    initial begin
        $monitor("%d\t%b\t%b\t%b",$time,ena,n,e);
        $dumpfile("decoder3e_test.vcd");
        $dumpvars;
    end
endmodule

