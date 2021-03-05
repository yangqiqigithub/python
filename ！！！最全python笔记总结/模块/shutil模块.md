```
import  shutil
#shutil.copy(src,dst) cp文件和权限
shutil.copy("fs.txt","fd.txt")
#相当于目录间的cp -r  目标已经存在报错
shutil.copytree("glance","glance1")
#递归删除目录 rm -f
shutil.rmtree("glance1")
#递归移动目录 mv
shutil.move("glance","glance1")
#压缩到哪 什么格式  压缩谁   glance2.zip 压缩后的样子
shutil.make_archive("E:\s14\day05\glance2","zip","E:\s14\day05\glance1")
 
#shutil.copyfileobj(src,dst) 文件拷贝
fs=open("fs.txt","r")
fd=open("fd.txt","w",encoding="utf8")
shutil.copyfileobj(fs,fd)
fs.close()
fd.close()

#shutil.copyfile(src,dst) 直接用文件名拷贝文件 覆盖
shutil.copyfile("fs.txt","fd.txt")

#shutil.copymode(src,dst)  仅拷贝权限 其他应该会变
shutil.copystat(src,dst) # cp所有属性
```