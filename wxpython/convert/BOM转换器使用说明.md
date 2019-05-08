# BOM转换器使用说明



## 按键功能说明

1. ERP：选择ERP编码表格提取编码，
2. calibration：校准，选择校准文件，提取校准信息，解决原BOM与库存型号有差异的问题
3. OUTPUT：选择输出文件夹
4. CONVERT：选择转化的文件



## 文件格式说明

### PCBABOM

![](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1556530859547.png)

根据BOM类型==PCBA焊接BOM 判断BOM类型

根据Designator确定起始行

根据commentname填写编码

这三项必须有

如果没有物料编码一列，编码会在最后一列后添加一列

### 整机BOM&结构BOM

![1556531120654](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1556531120654.png)

根据BOM类型==产品整机BOM 或产品组装结构BOM，判断BOM类型

根据日期确定起始行

根据物料型号填写编码

这三项必须有

如果没有物料编码一列，编码会在最后一列后添加一列



### 校准文件

![1556531396762](C:\Users\Administrator\AppData\Roaming\Typora\typora-user-images\1556531396762.png)

ERROR列为原BOM的型号，CORRECT为库存的正确型号