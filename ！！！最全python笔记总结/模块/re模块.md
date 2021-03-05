# 常用字符匹配
```
字符：
　　. 匹配除换行符以外的任意字符
　　\w 匹配字母或数字或下划线或汉字 [A-Za-z0-9]
   \W    匹配非[A-Za-z0-9]
　　\s 匹配任意的空白符 \t、\n、\r
\S 相反的  就是去掉任意空白字符
　　\d 匹配数字0-9
   \D 匹配非数字
　　\b 匹配单词的开始或结束
　　^ 匹配字符串的开始 \A
　　$ 匹配字符串的结束 \Z
   | 匹配|左或|右的字符
   \n 匹配换行符
   \t 匹配制表符
   (...) 分组匹配
 
次数：
代表左边的那一个字符的个数
　　* 重复零次或更多次
　　+ 重复一次或更多次
　　? 重复零次或一次
　　{n} 重复n次
　　{n,} 重复n次或更多次
　　{n,m} 重复n到m次
```
# 举例说明
### 普通字符举例
```
import re
print(re.findall('\w','geon | hello 123_'))
#['g', 'e', 'o', 'n', 'h', 'e', 'l', 'l', 'o', '1', '2', '3', '_']
print(re.findall('\W','geon | hello 123_'))
#[' ', '|', ' ', ' ']
print(re.findall('\s','geon | hello\n \r \t 123_'))
#[' ', ' ', '\n', ' ', '\r', ' ', '\t', ' ']
print(re.findall('\S','geon | hello\n \r \t 123_'))
#['g', 'e', 'o', 'n', '|', 'h', 'e', 'l', 'l', 'o', '1', '2', '3', '_']
print(re.findall('\d','geon | hello\n \r \t 123_'))
#['1', '2', '3']
print(re.findall('\D','geon | hello\n \r \t 123_'))
#['g', 'e', 'o', 'n', ' ', '|', ' ', 'h', 'e', 'l', 'l', 'o', '\n', ' ', '\r', ' ', '\t', ' ', '_']
print(re.findall('h','geon | hello h hoo\n \r \t 123_'))
#['h', 'h', 'h']
print(re.findall('^h','hello geon | hello h hoo\n \r \t 123_')) #\A ^ 从头开始匹配 有就匹配一次就结束没有就空
#['h']
print(re.findall('^h','eon | hello h hoo\n \r \t 123_')) #[] #\A 从头开始 但是开头没有就是空 不会忘后匹配的
#[]
print(re.findall('123$','eon | hello h hoo\n \r \t 123_')) #[]
#[]
print(re.findall('123$','eon | hello h hoo\n \r \t 123')) #['123'] \Z $从结尾开始 和\A的原理一样
#['123']
print(re.findall('\n','eon | hello h hoo\n \r \t 123'))
#['\n']
print(re.findall('\t','eon | hello h hoo\n \r \t 123'))
#['\t']
```
### 次数举例说明
##### 第一组：. [] [^]
. 任意一个字符  \n除外
```
import re

print(re.findall('a.c','a a1c a*c a2c abc a c aaaaaaac'))
#['a1c', 'a*c', 'a2c', 'abc', 'a c', 'aac']

print(re.findall('a.c','a a1c a*c a2c abc a c aaaaaaac a\nc'))
#['a1c', 'a*c', 'a2c', 'abc', 'a c', 'aac'] #默认不匹配 \n

print(re.findall('a.c','a a1c a*c a2c abc a c aaaaaaac a\nc' ,re.DOTALL))
#['a1c', 'a*c', 'a2c', 'abc', 'a c', 'aac', 'a\nc'] #匹配 \n
 
print(re.findall('a.c','a a1c a*c a2c abc a c aaaaaaac a\nc' ,re.S))
#['a1c', 'a*c', 'a2c', 'abc', 'a c', 'aac', 'a\nc'] #匹配 \n
```
[] 内部可以有多个字符，但是本身只匹配多个字符中的一个
```
import re
print(re.findall('a[1234]c','a a1c a*c a2c abc a c aaaaaaac'))
#['a1c', 'a2c']
print(re.findall('a[0-9]c','a a1c a*c a2c abc a c aaaaaaac')) #- 范围
#['a1c', 'a2c']
print(re.findall('a[a-z]c','a a1c a*c a2c abc a c aaaaaaac'))
#['abc', 'aac']
print(re.findall('a[A-Z]c','a a1c a*c a2c abc a c aaaaaaac'))
#[]
print(re.findall('a[0-9a-zA-Z]c','a a1c a*c a2c abc a c aaaaaaac aAc'))
#['a1c', 'a2c', 'abc', 'aac', 'aAc']

#匹配出 a-c  转义一下
print(re.findall('a[\-]c','a a+c a*c a/c a-c a c aaaaaaac'))
#['a-c']
```
[^ ] 取反
```
print(re.findall('a[^0-9]c','a a1c a*c a2c abc a c aaaaaaac aAc'))
#['a*c', 'abc', 'a c', 'aac', 'aAc']
```
\ 转义符
```
#在python里想转义一个\ 就得用三个来转义 最后一共三个
print(re.findall('a\\\\c','a\c abc acc'))
#['a\\c'] 显示两个\\ 其实就是 a\c
print(re.findall(r'a\\c','a\c abc acc'))
#['a\\c'] #加上r 就可以按照正常思维走了
```
##### 第二组： ？ *  +  {} 
代表左边的字符有几个 本身不代表一个字符 
如果有的话 贪婪匹配  

？ 左边那一个字符有0个或1个
```
import re

print(re.findall('ab?','a b  ab abb abbb abbbb bbbbbb'))
#['a', 'ab', 'ab', 'ab', 'ab'] 
'''
?左边的字符有0个或者一个
现在？左边的字符是b 那就是？左边的字符b可以有0个或者一个
也就是这个ab?只匹配 a  ab
'''
print(re.findall('a?b','a b  ab abb abbb a'))
#['b', 'ab', 'ab', 'b', 'ab', 'b', 'b']
```
* 左边那一个字符有0个或者无穷个
```
import re
print(re.findall('ab*','a b  ab abb abbb abbbb bbbbbb'))
print(re.findall('a*b','a b  ab abb abbb a bbbbb'))
'''
['a', 'ab', 'abb', 'abbb', 'abbbb']
['b', 'ab', 'ab', 'b', 'ab', 'b', 'b', 'b', 'b', 'b', 'b', 'b']

''
```
+ 左边那一个字符有一个或者无穷个
```
import re

print(re.findall('ab+','a b  ab abb abbb abbbb bbbbbb'))
print(re.findall('a+b','a b  ab abb abbb a bbbbb'))
'''
['ab', 'abb', 'abbb', 'abbbb']
['ab', 'ab', 'ab']
'''
```
{n,} 左边那一个字符有n个或者无穷个
{n,m} 左边那一个字符有n-m个
```
import re

print(re.findall('ab{2,}','a b  ab abb abbb abbbbb abbbbbb'))
print(re.findall('ab{2,4}','a b  ab abb abbb abbbbb abbbbbb'))
'''
['abb', 'abbb', 'abbbbb', 'abbbbbb']
['abb', 'abbb', 'abbbb',  'abbbb']
'''
```
##### 第三组：.*   .*?
.*  匹配任意长度 任意字符 贪婪匹配  一般不用贪婪匹配
```
print(re.findall('a.*b','ababbbbbb'))
#['ababbbbbb'] a和b之间可以有任意长度任意字符 这里不是匹配了 ab 和 ababbbbbb
而是.* 指的是dabbbbb 贪婪匹配 
```
.*?  非贪婪匹配 一般用这个 比较精准
```
print(re.findall('a.*?b','ababacbbbbb'))
#['ab', 'ab', 'acb']
```
##### 第四组： | 或者
```
print(re.findall("company|companies",'Too many companies have gone bankrupt, and the next one is her company'))
#['companies', 'company']
```
##### 第五个：（） 分组 不打印匹配的内容，打印的是组里的内容
```
import re
print(re.findall('(ab)','ababab123'))
print(re.findall('(ab)+','ababab123'))
print(re.findall('(ab)+123','ababab123'))
print(re.findall('(ab)+(123)','ababab123'))
'''
['ab', 'ab', 'ab']
['ab']
['ab']
[('ab', '123')]
'''
```
默认只显示组里的内容，加了 ?: 显示匹配成功的所有内容
```
import re
print(re.findall('(ab)+','ababab123'))
print(re.findall('(?:ab)+','ababab123'))
'''
['ab']
['ababab']
'''
```
```
print(re.findall("compan(y|ies)",'Too many companies have gone bankrupt, and the next one is her company'))
#['ies', 'y']
print(re.findall("compan(?:y|ies)",'Too many companies have gone bankrupt, and the next one is her company'))
#['companies', 'company']
```
##### re模块语法
```
import re

#1. findall 从头匹配到尾 把匹配对象都列出来
print(re.findall('ab','abababab123'))
#['ab', 'ab', 'ab', 'ab']

#2. search 从头开始匹配 一旦匹配成功就列出 并且结束匹配 
print(re.search('ab','abababab123'))
'''
<_sre.SRE_Match object; span=(0, 2), match='ab'>
直接拿到的是一个对象
'''
#通过group拿到结果
print(re.search('ab','abababab123').group())
#ab

#3. match
print(re.match('ab','abababab123'))
#<_sre.SRE_Match object; span=(0, 2), match='ab'>
print(re.match('ab','ab123ab345').group())
#ab
'''
match和search的区别
search 从头开始一直往后匹配 一旦匹配就结束
match  只匹配开头有就输出，没有就None
'''

# 4. split 切分
print(re.split("b","abcd"))
#['a', 'cd']

# 5. sub替换
print(re.sub('alex','SB','alex is happy alex'))
#SB is happy SB
print(re.subn('alex','SB','alex is happy alex'))
#('SB is happy SB', 2) 打印出替换了几个


print(re.sub('(\w+)(\W+)(\w+)(\W+)(\w+)',r'\5\2\3\4\1','alex make happy'))
#happy make alex

#6. compile 编译
obj=re.compile(('\d{2}')) #先编译好过滤规则  成为一个对象
print(obj.findall('123eeee')) #然后再调用 好处是可以重复使用
#['12']
print(obj.search('dhfdfk34').group())
#34
```