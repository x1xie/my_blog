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
```
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
# 6.dbutils多线程调用数据库 
## 方法一：dbutils 结合 threading.local
- 这个是借鉴了多线程中的threading.local()方法，当每个线程都会去获取自己对应的数据，所以在每一个线程开启时就会执行task方法，这个方法中有with这方法，这个方法是去调用上下文管理器，就需要执行这个对象中的__enter__()方法和__exit__()方法；进来时执行__enter__()这个方法，并且需要又返回值，这个返回值就是with db as cur:中的cur的值，在结束的时候需要执行__exit__()方法；在执行__enter__()方法的时候在里边将当前这个线程的数据写成一个字典，字典的键是固定的名字stack,字典的值是一个列表套元组形式，元组中是conn,cursor(数据库连接，游标对象)；将这个保存到threading.local()实例化出来的对象中self.local,在对数据库操作完之后，with也要执行__exit__()方法，在这个方法中会使用现在的self.local对象去获取存在这个对象中的那个字典，获取对应的值，然后对对游标进行关闭，数据的连接进行关闭
```python
import pymysql
from dbutils.pooled_db import PooledDB
import threading

class SqlHelper(object):
    def __init__(self):
        self.pool = PooledDB(
            creator=pymysql,       # 使用连接数据库的模块
            maxconnections=6,      # 连接池允许的最大连接数，0和None表示不限制连接数
            mincached=2,           # 初始化时，连接池中至少创建的连接个数，0表示不创建
            blocking=True,         # 连接池中如果没有可用连接后是否阻塞等待，True 等待，让用户等待，尽可能的成功； False 不等待然后报错，尽快告诉用户错误，例如抢购，不成功就提示。
            ping=0,                # ping MySQL服务器，检测服务器是否可以，如0=None=never, 1=default=whenever it is requestsed, 2=when a cursor is created, 4=when a query is executed, 7=always
            host='127.0.0.1',
            port=3306,
            user='username',
            passwd='password',
            database='datadb',
            charset='utf8'
            # maxcached=0,          # 连接池中最多闲置的连接，0表示不限制，连接使用完成后的空闲连接保留数。
            # maxusage=5,           # 每个连接最多被重复使用的次数，None表示不限制
        )
        self.local = threading.local()

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

    def fetchone(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql)
        resulf = cursor.fetchone()
        self.close(conn, cursor)
        return resulf

    def __enter__(self):
        conn, cursor = self.open()
        rv = getattr(self.local, 'stack', None)
        if not rv:
            self.local.stack = [(conn, cursor), ]
        else:
            rv.append((conn, cursor))
            self.local.stack = rv
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        rv = getattr(self.local, 'stack', None)
        if not rv:
            del self.local.stack
            return
        conn, cursor = self.local.stack.pop()
        cursor.close()
        conn.close()

db = SqlHelper()
```
#### 测试运行
```
from sqlhelper import db
import threading,time

def task(i):
    with db as cursor:
        cursor.execute('select * from comments')
        aa = cursor.fetchone()
        print(i, aa)
        time.sleep(3)
if __name__ == '__main__':
    for i in range(12):
        th = threading.Thread(target=task, args=(i,))
        th.start()
```
## 方法2
- 创建一次数据库连接池，在SqlHelper类中只是调用执行就行，不用在重复实例化对象；每次执行sql语句是实例化SqlHelper方法就行，由于每次实例化的对象不一样所以就不会有数据覆盖了
```python
import pymysql
from dbutils.pooled_db import PooledDB

POOL = PooledDB(
    creator=pymysql,  # 使用连接数据库的模块
    maxconnections=6,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=2,  # 初始化时，连接池中至少创建的连接个数，0表示不创建
    blocking=True,  # 连接池中如果没有可用连接后是否阻塞等待，True 等待，让用户等待，尽可能的成功； False 不等待然后报错，尽快告诉用户错误，例如抢购，不成功就提示。
    ping=0,   # ping MySQL服务器，检测服务器是否可以，如0=None=never, 1=default=whenever it is requestsed, 2=when a cursor is created, 4=when a query is executed, 7=always
    host='127.0.0.1',
    port=3306,
    user='username',
    passwd='password',
    database='datadb',
    charset='utf8'
    # maxcached=0,          # 连接池中最多闲置的连接，0表示不限制，连接使用完成后的空闲连接保留数。
    # maxusage=5,           # 每个连接最多被重复使用的次数，None表示不限制
)

class SqlHelper(object):

    def __init__(self):
        self.conn = None
        self.cursor = None

    def open(self):
        conn = POOL.connection()
        cursor = conn.cursor()
        return conn, cursor

    def close(self):
        self.cursor.close()
        self.conn.close()

    def fetchall(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql)
        resulf = cursor.fetchall()
        self.close()
        return resulf

    def fetchone(self, sql, *args):
        conn, cursor = self.open()
        cursor.execute(sql)
        resulf = cursor.fetchone()
        self.close()
        return resulf

    def __enter__(self):
        self.conn, self.cursor = self.open()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
```
#### 测试运行
```python
import threading,time
from sqlhelper2 import SqlHelper

def task(i):
    with SqlHelper() as cursor:
        cursor.execute('select * from comments')
        aa = cursor.fetchone()
        print(i, aa)
        time.sleep(3)
if __name__ == '__main__':
    for i in range(12):
        th = threading.Thread(target=task, args=(i,))
        th.start()
```
# 7.生成随机验证码
- 字体下载：https://files.cnblogs.com/files/wupeiqi/%E9%AA%8C%E8%AF%81%E7%A0%81%E5%AD%97%E4%BD%93%E6%96%87%E4%BB%B6.zip
- 安装：pip3 install pillow
```python
import random
from PIL import Image,ImageDraw,ImageFont,ImageFilter

def check_code(width=120, height=30, char_length=5, font_file='kumo.ttf', font_size=28):
    code = []
    img = Image.new(mode='RGB', size=(width, height), color=(255, 255, 255))
    draw = ImageDraw.Draw(img, mode='RGB')
 
    def rndChar():
        """
        生成随机字母   
        :return:
        """
        return chr(random.randint(65, 90))
 
    def rndColor():
        """
        生成随机颜色
        :return:
        """
        return (random.randint(0, 255), random.randint(10, 255), random.randint(64, 255))
 
    # 写文字
    font = ImageFont.truetype(font_file, font_size)
    for i in range(char_length):
        char = rndChar()
        code.append(char)
        h = random.randint(0, 4)
        draw.text([i * width / char_length, h], char, font=font, fill=rndColor())
 
    # 写干扰点
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
 
    # 写干扰圆圈
    for i in range(40):
        draw.point([random.randint(0, width), random.randint(0, height)], fill=rndColor())
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.arc((x, y, x + 4, y + 4), 0, 90, fill=rndColor())
 
    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
 
        draw.line((x1, y1, x2, y2), fill=rndColor())
 
    img = img.filter(ImageFilter.EDGE_ENHANCE_MORE)
    return img,''.join(code)
 
 
if __name__ == '__main__':
    # 1. 直接打开
    # img,code = check_code()
    # img.show()
 
    # 2. 写入文件
    # img,code = check_code()
    # with open('code.png','wb') as f:
    #     img.save(f,format='png')
 
    # 3. 写入内存(Python3)
    # from io import BytesIO
    # stream = BytesIO()
    # img.save(stream, 'png')
    # stream.getvalue()
 
    # 4. 写入内存（Python2）
    # import StringIO
    # stream = StringIO.StringIO()
    # img.save(stream, 'png')
    # stream.getvalue()
 
    pass
```