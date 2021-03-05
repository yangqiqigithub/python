## 安装模块
```
pip install XlsxWriter
```
## 常用命令
##### 创建exel文件
```
import xlsxwriter
workbook=xlsxwriter.Workbook('test.xlsx')
```
##### 创建sheet
```
worksheet = workbook.add_worksheet("first_sheet") 
```
##### 单元格数据写入
```
worksheet.write_row('A1','姓名')  #写入某个单元格的数据
```
![image](5527A0E43773454C9991444A0BF43F30)
##### 批量写入一行的数据
```
worksheet.write_row('A1',['姓名','年龄','部门']) #从A1开始
```
![image](5BD6760A3AF946C59BF01B95DC5285A1)
##### 批量写入一列的数据
```
worksheet.write_column('A1',['张三','李四','王五','赵六']) #从A1开始
```
![image](CCB358DFF9A54429BFA083352E22F781)
##### 写入函数
```
worksheet.write_column('A1',[1,2,3,4,5,])
worksheet.write('A6','=sum(A1:A5)')
```
![image](07BF652069D34DCA8CB52D132E07BD87)
##### 写入图片
```
worksheet.insert_image('D1','hh.jpg')
```
##### 写入日期
```
d = workbook.add_format({'num_format': 'yyyy-mm-dd'})
worksheet.write('E1', datetime.datetime.strptime('2017-09-13', '%Y-%m-%d'), d)
```
##### 设置行和列的属性
```
worksheet.set_row(0, 40)
worksheet.set_column('A:B', 20)
```
##### 合并单元格并输入内容
```
worksheet.merge_range('E1:G4', 'merge_range')
```
![image](5325A2AF24EB4C1AB90F62B14449C69A)
##### 自定义格式
```
#定义格式
f = workbook.add_format({'border': 1,
                         'font_size': 13,
                         'bold': True,
                         'align': 'center',
                         'color': '#FF0000'})


#绑定格式
worksheet.write_row('A1',['姓名','年龄','部门'],f)
```
![image](BEEDC5A431D84371B3BBEA6EF4A093EB)
##### 关闭文件
```
workbook.close()
```