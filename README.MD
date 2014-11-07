# FT-Yield-Report-Generator FT良率月报自动生成工具  
## 概述
- 自动绘制*Tango*系统中的`PareTo`柱状图和`TrendChart`趋势图
- 自动生成本月所有产品的`Summary`
- 自动绘制每位工程师的`Summary`柱状图

## 例子
- PareTo柱状图：
![image](https://raw.githubusercontent.com/eric6356/FT-Yield-Report-Generator/master/example/SH79F3211M_FUJI_SMK_CU_201410_PareTo.png)
- TrendChart趋势图：
![image](https://raw.githubusercontent.com/eric6356/FT-Yield-Report-Generator/master/example/SH79F3211M_FUJI_SMK_CU_201410_TrendChart.png)
- Summary柱状图：
![image](https://raw.githubusercontent.com/eric6356/FT-Yield-Report-Generator/master/example/summary.png)


## 使用方法
1.	在Tango系统中抓取本月的所有lot信息，补全Au/Cu后，[注1]追加在alq.csv中。
2.	确保alq.csv按照日期递增排序。
3.	在Tango中抓取本月的VendorLot Report，另存为./month/VendorLot.csv，注意month必须按照格式。
4.	运行go.py，按格式输入month，得到所有图表和Summary。
5.	出现以下4种情况说明binList.csv相应的部分需要维护：  
    i.	图片输出到unknown文件夹——需修改工程师名。  
    ii.	summary.csv中出现unknown封装——需修改封装名。  
    iii.	PareTo中bin name缺失——需增加Bin Name。  
    iv.	Summay中的OS不正确——需补上OS Bin Name。OS Bin Name可写成OS，O\S，O/S三者中的一者，不区分大小写。若无OS Bin Name，则默认以Bin8作为OS Bin。
    
注1：在Tango系统中，按下extract之前的预览表格中有Au/Cu的信息，而extract之后的表格则没有。因此需要手动补全后再追加到alq.csv中。可以在Tango中将extract前后的数据都按照lot名字排序后再下载，然后直接复制mental列到extract后的表格即可。


## 文件说明
### 脚本文件
| 文件名         | 说明                            |
| ------------- |:------------------------------|
| go.py         | 所有脚本的入口                   |
| deletelot.py  | 删除跨越Lot的前一笔记录           |
| pareTo.py     | 绘制PareTo，可以单独执行          |
| trendChart.py | 绘制TrendChart，可以单独执行      |
| summary.py    | 绘制Summary，生成CSV，可以单独执行 |
| index.py      | 输入文件的下标                   |


First Header | Second Header | Third Header
------------ | ------------- | ------------
Content Cell | Content Cell  | Content Cell
Content Cell | Content Cell  | Content Cell

