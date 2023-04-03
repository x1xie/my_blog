# flask笔记

## 1.flask基本使用
```angular2html
from flask import Flask
app = Flask(__name__, template_folder="templates", static_folder='static', static_url_path='/static')
@app.route('/', methods=['GET', 'POST'])
def index():
    return 'Hello World!'
if __name__ == '__main__':
    app.run()
```
static_folder静态文件路径，static_url_path静态文件页面路径 /static/aa.jpg ; 改动static_url_path='/yy'  /yy/aa.jpg
html 建议使用 < img src="{{url_for('static',filename='xx/xx/aa.jpg')}}">
## 2.添加配置文件
#### 1.目录结构
![](../../static/ml.png)
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

