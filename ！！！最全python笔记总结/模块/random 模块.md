```
import random


print(random.random()) #输出随机0-1之间的小数 0.6389899235102466
print(random.uniform(0,3)) #输出自定义两个数之间的小数 1.3503966622873236

print(random.randint(1,3)) #[1,3] 输出随机两个数之间的整数
print(random.randrange(1,3)) #[1,3)输出随机两个数之间的整数

print(random.choice(["a",3,"b"])) #随机输出列表里的一个元素

print(random.sample([1,2,"b","c","d",9,0],4)) #列表元素任意N个组合

item=[1,2,3,4,5,6,"a","b","c","e"]
random.shuffle(item) #洗牌
print(item) #['c', 2, 6, 5, 'b', 'e', 'a', 1, 3, 4]
```
##### 验证码：
```
import random
def make_code(n):
    res=''
    for i in range(n):
        s1=chr(random.randint(65,90))
        s2=str(random.randint(0,10))
        res+=random.choice([s1,s2])
    return res

print(make_code(5)) # 9V7C4
```