import csv


iter=[
    {'id':2,'name':'wanwu','age':23,'date':20180627},
    {'id':3,'name':'zhaoliu','age':24,'date':20180627},
    {'id':4,'name':'tianqi','age':25,'date':20180627}
]
#写入文件
with open('names.csv','w',newline='') as csvf:
    fieldnames=['id','name','age','date']
    writer=csv.DictWriter(csvf,fieldnames=fieldnames)
    writer.writeheader()
    writer.writerow({'id':1,'name':'lisii','age':22,'date':20180627})
    writer.writerows(iter)