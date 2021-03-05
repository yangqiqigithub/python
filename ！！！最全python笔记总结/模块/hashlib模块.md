### 常用用法
固定格式
```
import hashlib
m=hashlib.md5()
m.update(b"mypasword")
print(m.hexdigest())
#8870fa80200cebd005e41da8909bf091
```
### 详细用法
用于加密相关的操作，3.x里代替了md5模块和sha模块，主要提供 SHA1, SHA224, SHA256, SHA384, SHA512 ，MD5 算法
```
import hashlib

#举例 md5的方式如下
m=hashlib.md5()
m.update(b"hello")
print(m.digest()) #b']A@*\xbcK*v\xb9q\x9d\x91\x10\x17\xc5\x92' 二进制

m.update(b"123")
print(m.digest()) #b"\xf3\n\xa7\xa6b\xc7(\xb7@|T\xaek\xfd'\xd1"
print(m.hexdigest()) #f30aa7a662c728b7407c54ae6bfd27d1 十六进制
```
### 其他的用法
其他的用法一样，只是不同的加密方式
```
import hashlib

# ######## md5 ########

hash = hashlib.md5()
hash.update('admin')
print(hash.hexdigest())

# ######## sha1 ########

hash = hashlib.sha1()
hash.update('admin')
print(hash.hexdigest())

# ######## sha256 ########

hash = hashlib.sha256()
hash.update('admin')
print(hash.hexdigest())

# ######## sha384 ########

hash = hashlib.sha384()
hash.update('admin')
print(hash.hexdigest())

# ######## sha512 ########

hash = hashlib.sha512()
```