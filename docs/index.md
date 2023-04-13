# python 相关知识点
# 1. dbutils数据连接池的使用
```python
import pymysql
from dbutils.pooled_db import PooledDB

class SqlHelper(object):
    def __int__(self):
        self.pool = PooledDB(
            creator=pymysql,       # 使用连接数据库的模块
            maxconnections=6,      # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,           # 初始化时，连接池中至少创建的连接个数，0表示不创建
            blocking=True,         # 连接池中如果没有可用连接后是否阻塞等待，True 等待，让用户等待，尽可能的成功； False 不等待然后报错，尽快告诉用户错误，例如抢购，不成功就提示。
            ping=0,                # ping MySQL服务器，检测服务器是否可以，如0=None=never, 1=default=whenever it is requestsed, 2=when a cursor is created, 4=when a query is executed, 7=always
            host='127.0.0.1',
            port=3306,
            user='testuser',
            passwd='testpass',
            database='testdb',
            charset='utf8'
            # maxcached=0,          # 连接池中最多闲置的连接，0表示不限制，连接使用完成后的空闲连接保留数。
            # maxusage=5,           # 每个连接最多被重复使用的次数，None表示不限制
        )

    def open(self):
        conn = self.pool.connection()
        cursor = conn.cursor()
        return conn, cursor

    def close(self, conn, cursor):
        cursor.close()
        conn.close()

    def fetchall(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql)
        resulf = cursor.fetchall()
        self.close(conn, cursor)
        return resulf
    
db = SqlHelper()
```
#### 使用
```python
from sqlhelper import db
resulf = db.fetchall('select * from userlist')
```
# 2.上下文管理器（with）
with 之前执行__enter__，之后执行__exit__
```python
class Foo(object):
    def __enter__(self):
        return 'with之前操作'
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
obj1 = Foo()
with obj1 as f:
    print(f)
```
# 3.装饰器执行顺序：
(运行结果： 1  0  )  
@functools.wraps装饰器可以防止调用同一个装饰器时同名报错，否则调用装饰器后函数名都为inner
```python
import functools
def auth0(func):
    print('0')
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner
def auth1(func):
    print('1')
    @functools.wraps(func)
    def inner(*args, **kwargs):
        return func(*args, **kwargs)
    return inner
@auth0
@auth1
def index():
    print('index')
```
# 4. 面向对象的attr 
obj.one = 1 时调用setattr， obj.one时调用getattr （打印one 1  ；one）
```python
class Foo(object):
    def __setattr__(self, key, value):
        print(key, value)
    def __getattr__(self, item):
        print(item)
obj = Foo()
obj.one = 1
obj.one
```
扩展（通过storage保存setattr的key, value）
```python
class Foo(object):
    def __init__(self):
        # self.storage = {}   #self.时会调用setattr引发报错
        object.__setattr__(self, "storage", {})
    def __setattr__(self, key, value):
        self.storage[key] = value
    def __getattr__(self, item):
        return self.storage.get(item)
obj = Foo()
obj.one = 1
print(obj.one)
```
# 5.threading.local
当每个线程在执行val.yy=1, 在内部会为此线程开辟一个空间来存储yy=1,  
val.yy通过线程id找到此线程自己的内存地址去取自己储存的yy
```python
import time
import threading
val = threading.local()
def task(i):
    val.num =1
    time.sleep(2)
    print(val.num)
for i in range(5):
    t = threading.Thread(target=task,args=(i,))
    t.start()
```
扩展：线程的唯一标识 from threading import get_ident  
在task中添加 ident = get_ident()  
#### 自定义threadinglocal

```python
import threading
from threading import get_ident
class Local(object):
    def __init__(self):
        object.__setattr__(self, "storage", {})
    def __setattr__(self, key, value):
        ident = get_ident()
        if ident in self.storage:
            self.storage[ident][key] = value
        else:
            self.storage[ident] = {key:value}
        self.storage[key] = value
    def __getattr__(self, item):
        ident = get_ident()
        if ident not in self.storage:
            return
        return self.storage[ident].get(item)
local = Local()
def task(arg):
    local.x1 = arg
    print(local.x1)
for i in range(5):
    t = threading.Thread(target=task, args=(i,))
    t.start()
```