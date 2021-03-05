```
import subprocess

status,res=subprocess.getstatusoutput('dir c:')
print('状态：',status,type(status))
print(res)
'''
状态： 0 <class 'int'>

驱动器 C 中的卷是 Windows
卷的序列号是 D286-9076
C:\ 的目录
2020/07/06  13:08    <DIR>          data
2020/09/11  23:22    <DIR>          DRIVERS
2020/03/18  23:09    <DIR>          kingsoft
'''

res=subprocess.getoutput('dir c:')
print(res)
'''
驱动器 C 中的卷是 Windows
卷的序列号是 D286-9076
C:\ 的目录
2020/07/06  13:08    <DIR>          data
2020/09/11  23:22    <DIR>          DRIVERS
2020/03/18  23:09    <DIR>          kingsoft
## '''
```