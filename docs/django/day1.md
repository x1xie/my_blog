# django基础
# 1.快速上手
```
1.创建项目：
    django-admin startproject 项目名称
2.创建应用app：
    cd 项目名称
    django-admin startapp app名称  或者 python manage.py startapp app名称
3.启动项目：
    python manage.py ruserver 80
4.注册应用app:
    settings.py-->installed_apps添加 app1.apps.App1Config
5.view.py 编写视图
6.urls.py 编写路由
7.静态文件-->app1目录下创建static存放js,css,img
    模板中引用 推荐 {% load static %} <img src="{% static 'img/test.png' %}" alt="">
8.模板语法
    变量 {{ 变量 }}
        .索引  .key  .属性  .方法   方法后不加括号
        注：当模板系统遇到.时，按照如下顺序进行
        1.在字典中查询
        2.属性或方法
        3.数字索引
    过滤器 filters
        语法 {{ value | filter_name:参数 }}
        “:”左右不能代友空格
        1.default  （当value没有返回时，显示自定义字符串）
            {{ value | default:"nothing"}}
        2.filesizeformat  （将格式转换成“人类可读”，如valuse位1024显示1KB,1024*1024显示为1MB）
            {{ value|filesizeformat }}
        3.add (加法,如加2,也可以字符串拼接)
            {{ value|add:2}}
        first为[1,2,3],second为[4,5,6] 显示为[1,2,3,4,5,6]
            {{ first | add:second }}  
        4.lower(小写)于upper(大写)
            {{ value|lower }}   {{ value|upper }}
        5.title (标题:首字母大写)
            {{ value|title }}
        6.length (返回变量长度)
            {{ value|length }}    
        7.slice (切片,从第二到最后一个)
            {{ value|slice:"2:-1" }}
        8.first(第一个) 与 last(最后一个)
            {{value|first}} {{value|last}}
        9.join  (使用字符串拼接)
            {{ value|jion:"test" }}
        10.truncatechars (字符串多于指定字符数量时，截断，以...显示,如：太阳照在地上...)
            {{ value|truncatechars:9 }}
           truncatewords(以单词的形式截断，即空格 )
            {{ value|truncatewords:9 }}
        11. date (日期格式化 ，value = datetime.detetime.now())
            {{ value|date:"Y-m-d H:i:s" }}
        12.safe(djang为了安全会对html标签转义，当不需要转义时使用safe)
            {{ value|safe }}
          
    继承
        主页面 main.html
            <div>{% block content %}{% endblock %}</div>
        继承的页面
            {% extends 'main.html' %}
            {% block content %}
            <p>这是继承内容</p>
            {% endblock %}
    静态文件 {% static ''%}
    引用数据 {{name}}  data:name = "zhnagsan"
    引用列表数据 {{name.0}}  data:name = ["zhangsan","lisi"]
    循环 data:name = ["zhangsan","lisi"]
        {% for n1 in name%} 
            <p>{{nl}}</p> 
        {% empty %}
            没有循环的对象
        {% endfor %}
        empty 当循环为空时执行   
        forloop.counter 当前循环的序号从1开始
        forloop.courter() 当前循环的序号从0开始
        forloop.revcounter 当前循环的循环（倒序）到1结束
        forloop.revcounter() 当前循环的循环（倒序）到0结束
        forloop.first 是否是第一次循环 布尔值
        forloop.last  是否是最后一次循环 布尔值
        forloop.parentloop  当前循环的外层循环变量
    字典循环  data:user = {"name":"zhnagsan","age":"22"}
        获取name user.name
        获取所有的键{% for key in user.keys %} 
        获取所有的值{% for value in user.values%}
        获取所有的键值 {% for k,v in user.items %} 注意是user.items不是user.items()
    if条件判断 {% if key = 1 %}...{% elif key=2 %}...{% else %}...{% endif %}
    with 定义中间变量(起别名)
        {% with total = name.0 %}  或 {% with name.0 as total%}
        {{ tota l}}
        {% endwith %}
            
9.请求与相应（view.py）
    request.method 请求方式
    request.GET get请求的数据
    requwst.POST post请求的数据
```
# 2.django导入详解
### 1.返回字符串
```python
from django.shortcuts import HttpResponse  
def index(request):
    return HttpResponse("hello world")
```
### 2.返回html文件
```python
from django.shortcuts import render
def index(request):
    name = "zhangsan"
    #app1目录下templates目录寻找index.html（原理：根据app注册顺序，逐一去他们的templates目录中寻找）
    return render(request,"index.html",{"n1":name})
```
### 3.重定位
```python
from django.shortcuts import redirect
def index(request):
    return redirect('http://www.baidu.com')
```
### 4.返回html
```
from django.utils.safestring import mark_safe
html_page = mark_safe('<li><a href="?page=1">1</li>')
```
### 5.免除csrf认证（Ajax时使用）
```python
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def task_ajax(request):
    print(request.GET)
    return HttpResponse("请求成功")
```
### 6.json序列化
```
from django.http import JsonResponse
import json
    ...
    data_dict = {"staust":200, "data":[11,22,33]}
    json_str = json.dump(data_dict, ensure_ascil=False)
    # ensure_ascil 数据格式是否与以ascil格式返回
    return JsonResponse(json_str)
```
# 3.settings.py配置详解
```
1. TEMPLATES中设置了'DIRS':[os.path.join(BASE_DIR,'templasts')],
    模板优先去项目的根目录中templates寻找,之后再根据app注册顺序，逐一去他们的templates目录中寻找
2. TEMPLATES中设置了'DIRS':[],
    模板根据app注册顺序，逐一去他们的templates目录中寻找,不会去项目的根目录中templates寻找
3.给改默认时间格式
    USE_LION=False
    DATETIME_FORMAT = 'Y-m-d H:i:s'
    TIME_FORMAT = 'H:i:s'
    DATE_FORMAT = 'Y-m-d'
4.静态文件配置
    STATIC_URL = '/static/'
    STATICFILES_DIRS = [
            os.path.join(BASE_DIR, 'static')
    ]
    
```
# 4.数据库(0RM)
- 使用mysqlclient 不推荐使用pymysql,对新版django兼容性不好，内部有编码错误
- 下载    pip install mysqlclient 安装失败则网上下载mysqlclient wheel包安装
### 创建数据库
```
create database project1 DEFAULT CHARSET utf8 COLLAYE utf8_general_ci;
```
### settings.py 配置
```
DATABASES = {
    'default':{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'project1' # 数据库名称
        'USER': 'root',
        'PASSWORD': 'root123',
        'HOST': '127.0.0.1',  
        'PORT': '3306',
                
    }
}
```
### 字段类型
```
AutoField(Field)
- int自增列，必须填入参数 primary_key=True 

BigAutoField(AutoField)
- bigint自增列，必须填入参数 primary_key=True  
注：当model中如果没有自增列，则自动会创建一个列名为id的列   

SmallIntegerField(IntegerField):
- 小整数 -32768 ～ 32767

PositiveSmallIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField)
- 正小整数 0 ～ 32767

IntegerField(Field)
- 整数列(有符号的) -2147483648 ～ 2147483647

PositiveIntegerField(PositiveIntegerRelDbTypeMixin, IntegerField)
- 正整数 0 ～ 2147483647

BigIntegerField(IntegerField):
- 长整型(有符号的) -9223372036854775808 ～ 9223372036854775807

BooleanField(Field)
- 布尔值类型

NullBooleanField(Field):
- 可以为空的布尔值

CharField(Field)
- 字符类型
- 必须提供max_length参数， max_length表示字符长度

TextField(Field)
- 文本类型

EmailField(CharField)：
- 字符串类型，Django Admin以及ModelForm中提供验证机制

IPAddressField(Field)
- 字符串类型，Django Admin以及ModelForm中提供验证 IPV4 机制

GenericIPAddressField(Field)
- 字符串类型，Django Admin以及ModelForm中提供验证 Ipv4和Ipv6
- 参数：
protocol，用于指定Ipv4或Ipv6， 'both',"ipv4","ipv6"
unpack_ipv4， 如果指定为True，则输入::ffff:192.0.2.1时候，可解析为192.0.2.1，开启刺功能，需要protocol="both"

URLField(CharField)
- 字符串类型，Django Admin以及ModelForm中提供验证 URL

SlugField(CharField)
- 字符串类型，Django Admin以及ModelForm中提供验证支持 字母、数字、下划线、连接符(减号)

CommaSeparatedIntegerField(CharField)
- 字符串类型，格式必须为逗号分割的数字

UUIDField(Field)
- 字符串类型，Django Admin以及ModelForm中提供对UUID格式的验证

SlugField(CharField)
- 字符串类型，Django Admin以及ModelForm中提供验证支持 字母、数字、下划线、连接符(减号)

CommaSeparatedIntegerField(CharField)
- 字符串类型，格式必须为逗号分割的数字

UUIDField(Field)
- 字符串类型，Django Admin以及ModelForm中提供对UUID格式的验证

FilePathField(Field)
- 字符串，Django Admin以及ModelForm中提供读取文件夹下文件的功能
- 参数：
path, 文件夹路径
match=None, 正则匹配
recursive=False, 递归下面的文件夹
allow_files=True, 允许文件
allow_folders=False, 允许文件夹

FileField(Field)
- 字符串，路径保存在数据库，文件上传到指定目录
- 参数：
upload_to = "" 上传文件的保存路径
storage = None 存储组件，默认django.core.files.storage.FileSystemStorage

ImageField(FileField)
- 字符串，路径保存在数据库，文件上传到指定目录
- 参数：
upload_to = "" 上传文件的保存路径，一般配合settings.py中的MEDIA_ROOT使用
storage = None 存储组件，默认django.core.files.storage.FileSystemStorage
width_field=None, 上传图片的高度保存的数据库字段名(字符串)
height_field=None 上传图片的宽度保存的数据库字段名(字符串)

DateTimeField(DateField)
- 日期+时间格式 YYYY-MM-DD HH:MM[:ss[.uuuuuu]][TZ]

DateField(DateTimeCheckMixin, Field)
- 日期格式 YYYY-MM-DD

TimeField(DateTimeCheckMixin, Field)
- 时间格式 HH:MM[:ss[.uuuuuu]]

DurationField(Field)
- 长整数，时间间隔，数据库中按照bigint存储，ORM中获取的值为datetime.timedelta类型

FloatField(Field)
- 浮点型

DecimalField(Field)
- 10进制小数
- 参数：
max_digits，数据总长度
decimal_places，小数位长度

BinaryField(Field)
- 二进制类型

字段参数
null：是否允许为空
default：设置默认值
primary_key：是否主键
db_column：设置列名，这为了区分列名和类中的属性
db_index：创建索引
unique：创建唯一索引
unique_for_date：创建时间唯一索引
unique_for_month：创建月唯一索引
unique_for_year：创建年唯一索引
auto_now_add：记录数据记录创建时间
auto_now：记录数据更新时间，但只支持以下方式的更新，不支持直接update
choices：django admin中显示下拉框，避免连表查询
gender = models.IntegerFiekd(chioces=((1,'男')，(2,'女'),(0,'保密')), default=0)
blank：django admin是否能够为空
verbose_name：django admin中显示字段名称
editable：在django admin中能否编辑
error_messages：错误信息
help_text：帮助信息
```
### 外键
- 新建一个user的app，并且添加至settings中，在user中的models中写入代码，创建一个User模型
再在article中的models中添加这个外键，即在Article这个模型中新添加一个属性
```
# -to 与那一张表关联
# -to_field 表中那一列关联
# django自动  写的是author 生成数据列为author_id
author = models.ForeignKey(to="user.User",to_field="id",on_delete=models.CASCADE,null=True)
```
- 模型的外键引用的是本身自己这个模型，那么to参数可以为self，或者是这个模型的名字。在论坛开发中，一般评论都可以进行二级评论
```
class Comment(models.Model):
    content = models.TextField()
    orihin_comment = models.ForeignKey('self',on_delete=models.CASCADE)
```
- 如果一个模型使用了外键。那么在对方那个模型被删掉后，该进行什么样的操作。可以通过on_delete来指定。可以指定的类型如下：
```
CASCADE：级联操作。如果外键对应的那条数据被删除了，那么这条数据也会被删除。
PROTECT：受保护。即只要这条数据引用了外键的那条数据，那么就不能删除外键的那条数据。如果我们强行删除，Django就会报错。
SET_NULL：设置为空。如果外键的那条数据被删除了，那么在本条数据上就将这个字段设置为空。如果设置这个选项，前提是要指定这个字段可以为空。
SET_DEFAULT：设置默认值。如果外键的那条数据被删除了，那么本条数据上就将这个字段设置为默认值。如果设置这个选项，== 前提是要指定这个字段一个默认值 ==。
SET()：如果外键的那条数据被删除了。那么将会获取SET函数中的值来作为这个外键的值。SET函数可以接收一个可以调用的对象（比如函数或者方法），如果是可以调用的对象，那么会将这个对象调用后的结果作为值返回回去。== 可以不用指定默认值 ==
DO_NOTHING：不采取任何行为。一切全看数据库级别的约束。
```
### django操作表
- 创建
```
from django.db import models
class UserInfo(models.Model):
    name = models.CharField(verbose_name="姓名", max_length=32)
    password = models.CharField(max_length=32)
    mobile = models.CharField(max_length=18)
    def __str__(self):
        ruturn self.name
相当于
create table app名称_userinfo(
    id bigint auto_increament primary key,
    name varchar(32),
    password varchar(32)
    mobile varchar(18)
)
执行命令 python manage.py makemigrations
        python manage.py migrate
注意：执行之前需要app已注册
在表中新增列时，由于已存在列中可能已有数据，所有新增列必须要指定新增列对应额数据：
- 手动输入一个值
- 设置默认值
age = models.IntegerFiled(defualt=2)
- 允许为空
data = models.IntegerFiled(null=True, black=True)
在开发中如果对表结构进行调整：
- 在models.py文件中操作类即可
- 命令 ：python manage.py makemigrations
        python manage.py migrate
```
- 添加
```
UserInfo.objects.create(name='zhangsan', password='aa1234')
```
- 修改
```
UserInfo.object.filter(id=3).update(password='3232ss')
```
- 删除
```
UserInfo.objects.filter(id=3).delete()  # 删除id为3的用户
UserInfo.objects.all().delete() # 删除这个表的区别数据
```
- 查询
```
exclude()查询时排除      filter()筛选
id__gt=12 # 大于12      id__gte=12 # 大于等于12
id__lt=12 # 小于12      id__lte=12 # 小于等于12
# 筛选出以为999开头    mobile__startswith="999"
# 筛选出以999结尾      mobile__endswith="999"
# 筛选出包含999        mobile__contains="999"
# 查询所有字段的值
users = UserInfo.objects.all().values_list()
# 查询指定字段的值
users = UserInfo.objects.values_list('uid', 'username')

# aggregate() #聚合函数Avg, Min, Max, Count, Sum
from django.db.models import Avg, Min, Max, Count, Sum
users = UserInfo.objects.aggregate(uid=Count('uid'))

data_list = [对象，对象] QuerySet类型
data_list = UserInfo.objects.all()

data_list1 = [对象] QuerySet类型
data_list1 = UserInfo.objects.filter(id=1)

对象(不需要循环，直接row_obj.password可以获取数据)
row_obj = UserInfo.objects.filter(name='zhangsan').first()

# 多条件查询
models.User.Info.objects.filter(mobile="13616273812",id=3)
##写法2
data_dict + {"mobile":"13616273812","id":3}
models.User.Info.objects.filter(**data_dict)
```
- 查询之Q对象
```
Q对象(django.db.models.Q)可以对关键字参数进行封装，从而更好地应用多个查询。
可以组合使用 &（and）,|（or），~（not）操作符，当一个操作符是用于两个Q的对象,
它产生一个新的Q对象
每个接受关键字参数的查询函数（例如filter()、exclude()、get()）都可以传递
一个或多个Q 对象作为位置（不带名的）参数。如果一个查询函数有多个Q 对象参数，
这些参数的逻辑关系为“AND"
注意:一定要把Q对象放在关键字参数查询的前面

# 查询 用户名是xiaohong 和 没有注销的用户信息
users= UserInfo.objects.filter(
    Q(username='zhangsan') & Q(is_delete=False)
)
```
- 查询之F对象
```
在使用F对象进行查询的时候需要注意：一个 F() 对象代表了一个 Model 
的字段的值；F 对象可以在没有实际访问数据库获取数据值的情况下对字段
的值进行引用。
Django 支持对 F对象引用字段的算术运算操作，并且运算符两边可以是具体
的数值或者是另一个 F 对象
#给Book所有实例价格（retail_price）涨价20元 
Book.objects.all().update(retail_price=F('retail_price')+20)
```
# 5.Form组件
- 原始方式思路：不会采用（本质:麻烦）
```
- 用户提交数据没有校验。
- 错误，页面上应该有错误提示。
- 页面上，每一个字段都需要我们重新写一遍。
- 关联数据，手动去获取并循环展示在页面。
```
### Form组件（小简单）
#### view.py
```
from django import forms
from django.shortcuts import render
class Myform(forms.Form):
    user = forms.CharField(widget=forms.TextInput)
    pwd = forms.CharField(widget=forms.PasswordInput)
   
def user_add(request):
     if request.method == 'GET':
        form = Myform()
        return render(request, 'user_add.html', {'from':form})
    # 用户POST提交数据，数据校验
    form = Myform(data=request.POST)
    if form.is_vaild():
        #如果数据合法，直接保存到数据库
        form.save()
        return redirect('/user/list/')
    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_add.html', {'from':form})
```
#### user_add.html
使用models中verbose_name的值
{{ form.name.label }}:{{ form.name }}
```
方式一：
<form method="post">
    {{form.user}}
    {{form.pwd}}
</form>
<!--<input type="text" placeholder="姓名" name="user" />-->
方式二：
<form method="post">
    {% for field in form %}
        {{ field }}}
         # 错误提示
        {{ field.errors.0 }}
    {{% endfor %}}
</form>
<!--<input type="text" placeholder="姓名" name="user" />-->
```
### ModelForm组件（最简单, 推荐）
```
xx = forms.CharField(widget=forms.TextInput, disabled=True)
属性：
disabled 是否允许修改，True为不允许
validator 正则校验  eg. validator=[RegexValidator(r'^1[3-9]\d{9}$','手机号码格式错误'), ]
```
#### view.py
```
from django import forms
from django.shortcuts import render
from .models import UserInfo
class Myform(forms.ModelForm):
    # 定义models里面没有的字段xx
    xx = forms.CharField(widget=forms.TextInput)
    class Meta:
        model = UserInfo
        fields = ["name","password","xx"]
        # fields = "__all__"
        # exclude = ["email"]
def user_add(request):
    if request.method == 'GET':
        form = Myform()
        return render(request, 'user_add.html', {'from':form})
    # 用户POST提交数据，数据校验
    form = Myform(data=request.POST)
    if form.is_vaild():
        # form.instance.oid = 'xxxxxx' 添加oid字段数据，如订单号
        #如果数据合法，直接保存到数据库
        form.save()
        return redirect('/user/list/')
    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_add.html', {'from':form})
```
#### user_add.html
使用models中verbose_name的值
{{ form.name.label }}:{{ form.name }}
```
方式一：
<form method="post">
    {{ form.name }}
    {{ form.pwd }}
 
</form>
<!--<input type="text" placeholder="姓名" name="user" />-->
方式二：
<form method="post">
    {% for field in form %}
        {{ field.label }}：
        {{ field }}}
     # 错误提示
        {{ field.errors.0 }}
    {{% endfor %}}
</form>
<!--<input type="text" placeholder="姓名" name="user" />-->
```
#### 定义样式插件
disabled 是否允许修改，True为不允许
```
class Myform(forms.ModelForm):
    # 定义models里面没有的字段xx
    xx = forms.CharField(widget=forms.TextInput, disabled=True)
    # 重写name添加校验规则 validators属性可以添加正则
    name = forms.CharField(min_lenght=3, label="用户名")
    class Meta:
        model = UserInfo
        fields = ["name","password","xx"]
        # 使用所有字段：fields = "__all__"
        # 排除字段 : exclude = ["password"]
    ## 方式一
    # widgets = {
    #    "name": forms.TextInput(attrs={"class": "from-contorl"}), 
    #}
    ## 方式二
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs):
        # 循环找到所有的插件，添加class
        for name,field in self.fields.items():
           
            print (name,field)
            ## 结果 name <django.froms.fields.CharField object at xxx>
            ##     password <django.froms.fields.CharField object at xxx>
            
            # 让某个字段不添加
            # if name == "password":
            #    continue
            field.widget.attrs = {"class":"form-control"}
```
#### 备注
- setting.py form组件提示中文
```
LANGUAGE_CODE = 'zh-hans'
```
- html显示错误信息(novalidate忽略浏览器校验)
```
<form method="post" novalidate>
    {% for field in form %}
        {{ field.label }}:{{ field.name }}
        {{ field.errors.0 }}
    {{% endfor %}}
</form>
```
- view.py
```
if request.method == 'POST':
# 用户POST提交数据，数据校验
    form = Myform(data=request.POST)
    if form.is_vaild():
        #如果数据合法，直接保存到数据库
        form.save()
        return redirect('/user/list/')
    # 校验失败（在页面上显示错误信息）
    # 自定义错误返回
    form.add_error("password","用户密码错误")
    return render(request, 'user_add.html', {'from':form})
    
# 更新（编辑用户）
    ## 根据ID去数据库获取要编辑的那一行数据
    row_object = models.UserInfo.object.filter(id=nid).first()
    if request.method == 'GET':
        # instance 编辑的时候默认填充已有数据
        form = Myform(instance=row_object)
        if form.is_vaild():
        return render(request, 'user_add.html', {'from':form})
    form = Myform(data=request.POST, instance=row_object)
    if form.is_vaild():
        # 如果数据合法，直接保存到数据库
        # 默认保存的是用户输入的所有数据，如果想要在用户输入以外增加一些值
        # form.instance.字段名 = 值
        form.save()
        return redirect('/user/list/')
    # 校验失败（在页面上显示错误信息）
    return render(request, 'user_add.html', {'from':form})
```
#### 验证方式(ModdelForm里)
```
# 方式1：
modeile = forms.CharField(
        label="手机号"，
        validator=[RegexValidator(r'^1[3-9]\d{9}$','手机号码格式错误'), ],
)
# 方式二：(构造方法 clean_字段名 )
def clean_mobile(self):
    txt_mobile = self.cleaned_date["mobile"]
    exists = models.UserInfo.object.filter(mobile=txt_mobile).exists()
    if exists:
        raise ValidationError("手机号已存在")
    elif lem(txt_mobile) != 11:
        # 校验不通过
        raise ValidationError("格式错误")
    # 校验通过，用户输入的值返回
    return txt_mobile
在编辑中校验数据唯一（除自己之外）：
def clean_mobile(self):
    # 当前编辑哪一行的id
    # print(self.instance.pk)
    txt_mobile = self.cleaned_date["mobile"]
    # 排除自己校验是否已存在
    exists = models.UserInfo.object.exclude(id=self.instance.pk).filter(mobile=txt_mobile).exists()
    if exists:
        raise ValidationError("手机号已存在")
```
# 6.cookie与session
- session
session信息放在数据库的django_session表里面
view.py中
``` 
# 登录
# 网站生成随机字符串；写到用户浏览器的cookie中；再写入到session中；
request.session["info"] = {"id":"user.id", "name":"user.name"}
# request.session["user"] = user.name
# session保存7天
request.sesson.set_expiry(60 * 60 * 24 * 7)

# 校验
request.session.get("info")

# 注销
request.session.clear()
备注：
html模板中也可也使用{{ request.session.info.name }}获取用户名
```
# 7.中间件
- 应用中间件，中间件运行顺序为：M1来了，M2来了，M2走了，M1走了
- 在app1下新建一个middleware/auth.py
- settings.py  MIDDLEWARE中添加app1.middleware.auth.M1中间件的类，注册中间件
```
MIDDLEWARE = [
    ...
    app1.middleware.auth.M1,
    app1.middleware.auth.M2,
]

```
auth.py中
```
from django.utils.deprecation import MiddlewareMixin

class M1(MiddlewareMixin):
    def process_request(self, request):
        # 如果方法中没有返回值，继续向后走
        # 如果有返回值 这return 比如return HttpResponse("无权访问")
        # 这直接返回，不向后走
        print("M1,来了")
    def process_response(self, request, response):
        print("M1,走了")
        return  response

class M2(MiddlewareMixin):
    def process_request(self, request):
        # 排除那些不需要登录就能访问的页面
        # request.path_info 获取当前用户请求的URL /login/
        if request.path_info == "/login/":
            return 
        info_dict = request.session.get("info")
        if info_dict:
            return 
        # 2.没有登录，重新回到登录页面
        return redirect('/login/')
        print("M2,来了")
    def process_response(self, request, response):
        print("M2,走了")
        return  response
```
# 8.图形验证码
- html 模板中img标签动态返回图片
```
<img id="image_code" src="/image/code/" style="width:125px;">
```
- view.py中
```
# 导入生成随机验证码模块，代码详情参考看首页/python生成随机验证码
from app1.utls.code import check_code

from django.shortcuts import HttpResponse
from io import BytesIO

def image_code(request):
    # 调用pillow函数，生成图片
    img, code_string = check_code()
    # 写入到自己的session中（以便于后续获取验证码进行校验）
    request.session['image_code'] = code_string
    #给session设置60秒超时
    request.session.set_expiry(60)
    # request.session.clear()
    print(code_string)
    # 把图片写到内存中
    stream = BytesIO()
    img.save(stream, 'png')
    return HttpResponse(stream.getvalue())
```
- 验证码校验
采用session校验：
```
    if from.is_valid():
        user_input_code = from.cleaned_data.pop('code')
        code = request.session.get('image_code',"")
        if code.upper() != user_input_coe.upper()
        form.add_error("code", "验证码错误")
        return render(request, 'login.html', {'from':from})
```
# 9.Ajax请求（结合jquery使用）
- 一般返回json格式数据
- 例子
```javascript
function click1() {
    $.ajax({
        url: "/test/ajax",
        type: "get",
        data: {
            n1:123,
            n2:456
        },
        dataType: "JSON",
        success: function (res) {
            console.log(res);
        }
    })
}
```
- 例子2：

```
    <form id="form2">
    <input type="text" name="user" id="txtuser" placeholder="姓名">
    <input type="text" name="age" id="txtage" placeholder="年龄">
    </form>
    <input id="btn2" type="button" value="点击2">
    ...
    function click1() {
        $("#btn3").click(function() {
        $(".error-msg").empty();  //清空class="error-msg"的text
        $.ajax({
            url: "/test/ajax",
            type: "get",
            data: $("#form2").serialize(),
            dataType: "JSON",
            success: function (res) {
                if (res.status) {
                    console.log(res);
                    alert("添加成功");
                    // 清空表单 $("#form2")是jquery对象->$("#form2")[0]位DOM对象
                    $("#form2")[0].reset();
                    // 关闭对话框
                    $("#form2").modal('hide');
                    //刷新页面
                    location.reload();
                } else {
                    $.each(res.error, function (k, v)) {
                        $("#id_"+name).next().text(data[0]);
                    })
                }
                
            }
        })
        })
    }
    ### 如果通过id获取，则改为data：{ name: $("#txtuser").val(),age: $("#txtage").val()}
```
后端通过modelform进行校验
```
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
@csrf_exempt
def task_add(request):
    form = TaskModelForm(data=request.POST)
    if form.is_vaild():
        form.sava()
        data_dict = {"status": True}
        return HttpResponse(json.dumps(data_dict))
    else:
        data_dict = {"status": False, "error":form.errors}
        return HttpResponse(json.dumps(data_dict, ensure_ascii=False))
```
# 10.文件上传
### 1.基本操作
```html
<form method="post" enctype="multipart/form-data">
    {% csrf_token %}
    <input type="text" name="username">
    <input type="file" name="avatar">
    <input type="submit" value="提交">
</form>
```
view
```
## 'username':['img666']
# print(request.POST)
## <multivaluedict:{'avatar':[<inmemoryUploadefile:图片 1.png (image/png)>]}>
# print(request.FILES)
file_object = request.FILES.get("avatar")
# print(file_object.name) #文件名称
f = open(file_object.name, mode="wb")
for chunk in file_object.chunks():
    f.write(chunk)
f.close()
```
### 2.批量上传
```html
<form method="post" enctype="multipart/form-data" action="/depart/multi/">
    {% csrf_token %}
    <input type="file" name="exc">
    <input type="submit" value="提交">
</form>
```
view
```
def depart_multi(request):
    from openpyxl import load_workbook
    # 1.获取用户上传的文件对象
    file_object = request.FILES.get("exc")
    # 2.对象传递给openpyxl, 由openpyxl读取文件内容
    wb = load_workbook(file_object)
    sheet = wb.worksheets[0]
    #3.循环获取每一行数据
    for row in sheet.iter_rows(min_row=2):
        text = row[0].value
        exists = models.Department.objects.filter(title=text).exists()
        if not exists:
            models.Department.objects.create(title=text)
        return redirect('/depart/list')
```
11.CBV(class based view) 与FBV (function based view)
urls.py
```
urlpatterns = [
    #FBV
    url('/user/list', views.userlist)
    #CBV
    url('/user/list', views.UserList.as_view())
]
```
view
```
# FBV
def userlist(request):
    if request.method == 'GET':
        return HttpResponse("FBV模式")
    return HttpResponse("FBV模式")
# CBV
class UserList(View):
    def get(self, request):
        return HttpResponse("CBV模式")
    def post(self, request):
        return HttpResponse("CBV模式")
```