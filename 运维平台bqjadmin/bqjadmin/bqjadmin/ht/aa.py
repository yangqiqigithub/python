from bs4 import BeautifulSoup
import os
import csv

g = os.walk(r'/Users/yangqiqi/PycharmProjects/bqjadmin/ht')
data_list=[]
keyword_list = ['Total Files:', 'Total Lines of Code:', 'Developers:']
for par_dir, _, files in g:
    for file in files:
        filepath = os.path.join(par_dir, file)
        if 'index.html' in filepath:
            with open(filepath, 'r', encoding='utf8') as f:
                html=f.read()
            html=BeautifulSoup(html,'html.parser')

            tag_list=[ '%s' %i.string for i in html.dl.find_all("dt") ]
            string_list=[ '%s' %i.string for i in html.dl.find_all("dd") ]
            info_dict={}
            new_dict={}

            for i in list(zip(tag_list,string_list)):
                info_dict.setdefault(i[0],i[1])
            for n in keyword_list:
                if n in info_dict.keys():
                    new_dict.setdefault(n,info_dict.get(n))
            data_list.append(new_dict)

print(data_list)

#写入文件
with open('data.csv','w',newline='') as csvf:
    writer=csv.DictWriter(csvf,fieldnames=keyword_list)
    writer.writeheader()
    writer.writerows(data_list)



