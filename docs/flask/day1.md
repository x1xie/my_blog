# flask笔记
补充装饰器相关：(运行结果： 1  0  )
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
对于flask使用装饰器时：
```
@app.route('/')
@auth0
```
简介：包含Jinja2模板渲染 ；基于Werkzeug的wsgi实现网关
```python
from werkzeug.serving import run_simple
from werkzeug.wrappers import Response
def func(environ, start_response):
    response = Response('hello world')
    print('请求到来')
    return response(environ, start_response)
if __name__ == '__main__':
    run_simple('127.0.0.1', 7000, func)
```
## 1.flask基本使用
```angular2html
from flask import Flask
app = Flask(__name__, template_folder="templates", static_folder='static', static_url_path='/static')
app.secret_key = 'sfddfffdh77789'
@app.route('/', methods=['GET', 'POST'], strict_slashes=False)
def index():
    return 'Hello World!'
if __name__ == '__main__':
    app.run()
```
- static_folder静态文件路径，static_url_path静态文件页面路径 /static/aa.jpg ; 改动static_url_path='/yy'  /yy/aa.jpg
html 建议使用 < img src="{{url_for('static',filename='xx/xx/aa.jpg')}}">
- strict_slashes 对url最后的/符合是否严格，默认为True，False为否
#### session设置 （flask通过加密的方式把session存在cookie中）
使用session时需要设置app.secret_key，否则会报错
@app.route('index', endpoint='bm')endpoint为别名，url_for('bm')可以使用别名
```
# login中添加session
session['username'] = 'xxxx'
# 在使用时验证session 
username = session.get('xxxx')
if not username:
    return redirect(url_for('login'))
```
#### 获取请求中的数据
```
# get请求
id = request.args.get('id')
# post请求
user = request.form.get('user')
```

## 2.添加配置文件
#### 1.目录结构
![](https://my-blogxie.readthedocs.io/zh/latest/static/ml.png)
#### 2.配置详情
新建config文件夹，创建localsettings.py与settings.py  
##### localsettings.py用法：
```angular2html
用法1：本地配置文件
用法2:线上创建，settings数据用户名密码不用写，更安全不用人手一份密码，使用localsettings的配置，把localsettings.py 
    设置为git忽略文件单独配置，git init初始化，vim .gitignore 输入 config/localsettings.py ;
    再通过git拉文件则忽略localsettings.py ，防止密码泄露.gitignoer 会忽略config/localsettings.py
    文件，将其他文件都提交到git,做版本控制
eg:
    DB_HOST = '127.0.0.1'
    DB_USER = 'root'
    DB_PWD = '123'
```
##### settings.py 用法：
```angular2html
# 线上配置文件
# 1000个配置
DB_HOST = '10.0.2.111'
DB_USER = 'root'
DB_PWD = '123'
SECRET_KEY = 'skenhjwi2837283'
try:
    from .localsettings import *
except ImportError:
    pass
```
项目中__init__.py
```angular2html
from flask import Flask,views
def create_app():
    app = Flask(__name__, template_folder="templates", static_folder='static', static_url_path='/static')
    app.secret_key = app.config['SECRET_KEY']
    # 加载配置文件
    app.config.from_object('config.settings')
    print(app.config['DB_HOST'])
    @app.route('/', methods=['GET', 'POST'])
    def index():
        return 'Hello World!'
    return app
```
manage.py:
```angular2html
from pro_app1 import create_app
app = create_app()
if __name__ == '__main__':
    app.run()
```
## 3.flask路由写法
```
# 路由写法1
    @app.route('/<name>', methods=['GET', 'POST'])  #<int:n> float path 
    def index(name):  # put application's code here
        return 'Hello World!%s'%name 
    #路由写法2：
    def index():  # put application's code here
        return 'Hello World!'
    app.add_url_rule('/index', 'index', index, methods=['GET', 'POST'])
    # 路由加载流程：
    # 将url和函数打包成rule对象，将rule对象添加到map对象中，app.url_map=map对象 
```
## 4.CBV视图
CBV视图 执行get请求之后控制台打印，before2 before1 get  after1 after2
```
from flask import Flask,views
app = Flask(__name__)
def test1(func):
    def inner(*args, **kwargs):
        print('before1')
        result = func(*args, **kwargs)
        print('after1')
        return result
    return inner
def test2(func):
    def inner(*args, **kwargs):
        print('before2')
        result = func(*args, **kwargs)
        print('after2')
        return result
    return inner
class UserView(views.MethodView):
    methods = ['GET', 'POST']
    decorators = [test1, test2]
    def get(self):
        print('get')
        return 'get'
app.add_url_rule('/user', view_func=UserView.as_view('user')) #user为endpoint别名
```
## 5.模板
#### if语句
```
{% if title %}
<title>{{ title }} - Microblog</title>
{% else %}
<title>Welcome to Microblog</title>
{% endif %}
```
#### for语句 (nums=[11, 22, 33])
```
{% for i in nums %}
<p>{{ i }}</p>
{% endfor %}
<h1>{{ nums[0] }}</h1>
```
#### 继承：
```
主页面 main.html
<div>{% block content %}{% endblock %}</div>
继承的页面
{% extends 'main.html' %}
{% block content %}
    <p>这是继承内容</p>
    {# 导入form.html #}
    {% include 'form.html' %}
{% endblock %}
form.html
<form action=""> <input type="text"> </form>
```
#### 传函数
```
def func(arg):
    return '你好'+arg
@app.route('/md')
def index():
    nums = [11,22,33,44]
    return render_template('md.html', nums=nums, f=func)
html中
{{ f("嗨") }}
```
#### 定义全局模板方法
```
# 方法1：
@app.template_global()  # {{ func("小鸟")}}
def func(arg):
    return '你好' + arg
# 方法2
@app.template_filter()  # {{ "海豚"|x1("小鸟") }}
def x1(arg, name):
    return '你好' + arg + name
# 在模板中可以直接使用，注意在蓝图中中注册时，应用返回只有本蓝图
```
## 6.特殊的装饰器 
(@app.before_request;@app.after_request)
运行结果（f1 f2 index f20 f10）;f20再到f10 是因为after_request中包含reversed()
```
# 方法一：
@app.before_request
def f1():
    print('f1')
@app.before_request
def f2():
    print('f2')
@app.after_request
def f10():
    print('f10')
@app.after_request
def f20():
    print('f20')
@app.route('/md')
def index():
    print('index')
    return render_template('index.html')
# 方法2：
def f1():
    print('f1')
app.before_request(f1)
def f10():
    print('f10')
app.after_request(f10)
```
## 7蓝图(app.register_blueprint)
### 7.1小蓝图(分功能蓝图)
构建业务功能可拆分的目录结构。  
在项目pro_app1下创建view文件夹存放视图  
访问时url为 xxxx/user/vshow
#### 注册：
```python
from flask import Flask
from .view.vtest1 import vtest1
from .view.vtest2 import vtest2
app = Flask(__name__)
app.register_blueprint(vtest1,url_prefix='/user') #访问时添加前序
app.register_blueprint(vtest2)
```
view文件夹中创建vtest1.py2,及vtest2.py   
与vtest1.py为例：
```python
from flask import Blueprint
vtest1 = Blueprint('vtest1', __name__, template_folder='templates')
@vtest1.route('/vshow')
def vshow():
    return 'vshow'
```
### 7.2大蓝图（分结构蓝图）
- 补充 当bigblue目录下 和 bigblue/account/ 目录下同时出现templates，默认使用bigblue目录下templates的模板
#### 目录结构
![](https://my-blogxie.readthedocs.io/zh/latest/static/ml2.png)
#### manage.py
```python
from bigblue import create_app
app = create_app()
if __name__ == '__main__':
    app.run()
```
#### bigblue/account/__init__.py
- from .views import forget 需要放在最后加载到内存， 否则会出现importerror;缺少from .views import forget则无法加载视图
```python
from flask import Blueprint

account = Blueprint('account', __name__, template_folder='templates')
from .views import forget
```
#### bigblue/account/views/forget.py
```python
from .. import account
from flask import render_template

@account.route('/')
def login():
    return render_template('login.html')
```
#### bigblue/__init__.py
```python
from flask import Flask

def create_app():
    app = Flask(__name__)
    app.secret_key = app.config['SECRET_KEY']
    # 加载配置文件
    app.config.from_object('config.settings')
    from .account import account
    from .admin import admin
    app.register_blueprint(account)
    app.register_blueprint(admin)
    return app
```
# 8. flask 源码关于local的实现
请求上下文管理   
应用上下文管理
```
在flask中有个local类，他和threading.local的功能一样，为每个线程开辟空间
进行存取数据，他们两个的内部实现机制，内部维护一个字典，以线程（协程）ID为key
,进行数据隔离，如：
__storage__={
    1233:{'k1':123}
}
obj = Local()
obj.k1 = 123
在flask中还有一个LocalStack类，它内部会依赖local对象，local对象负责存储数据
，对localstack对象用于将local中的值维护成一个栈。
__storage__={
    1233:{'stack':['k1',]}
}
obj = LocalStack()
obj.push('k1')
obj.top
obj.pop()
flask源码中总共有2个localstack对象
__storage__={
    1111:{'stack':[RequestContext(request.session),]}
}
_request_ctx_stack = LocalStack()

__storage__={
    1111:{'stack':[AppContext(app.g),]}
}
app_ctx_stack = LocalStack()
_request_ctx_stack.push('xxx')
app_ctx_stack.push('xxx')
_request_ctx_stack   ---请求上下文管理
app_ctx_stack        ---应用上下文管理
```

