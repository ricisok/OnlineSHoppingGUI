import datetime
import importlib
import os.path
from datetime import time
from functools import wraps
from pprint import pprint
from django.core.checks import messages
from django.forms import ModelForm, ChoiceField, ComboField, CharField, Textarea, TextInput, PasswordInput
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_exempt  # 禁止csrf校验
# from mywb.models import User, Blogdoc, Category, machine, example, Admin, ShopInfo, Merchant, Contract, Charge, \
#     Promotion, Publicmsg, Service
from mywb.models import *
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from datetime import datetime
import re

# json数据处理
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import serializers
from django.core import serializers
from urllib.parse import unquote


# Create your views here.
# 装饰器函数 用来检测用户是否登录
def login_required_view(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        print(request.session['user'])
        if request.session['user'] == None:
            return redirect('/adminlogin')
        return view_func(request, *args, **kwargs)

    return wrapper


def getPostData(request):
    postData = request.POST.get('machine')
    print(postData)
    return JsonResponse({"code": 200, "msg": "获取post数据成功"})


def getdata(request):
    ls = example.objects.all();
    pprint(ls)
    return JsonResponse({"code": 200, "msg": "获取post数据成功"})


def getPostalarm(request):
    machine = request.POST.get('machine')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    if startDate == None or endDate == None:
        return JsonResponse({"code": 200, "msg": "获取单个post数据成功"})
    else:
        return JsonResponse({"code": 200, "msg": "获取时点post数据成功"})


def index(request):
    # user = request.session.get('user')
    # if user is None:
    #     return redirect('/login')
    msg = Publicmsg.objects.all()

    goods = Goods.objects.all()

    return render(request, 'index.html', {'msg': msg, 'goods': goods})


# @login_required_view
'''
@description: 后台主页面
@Author: lyq
@Date: 2023-12-31 09:08:48
@return {*}
@param {*} request
@param {*} admin
'''


def admin(request):
    user = request.session.get('user')
    if user is None:
        return redirect('/adminlogin')
    return render(request, 'admin.html')


def test(request):
    return render(request, 'test.html')


'''
@description: 欢迎页面 包含统计数据
@Author: lyq
@Date: 2023-12-31 09:09:21
@return {*}
@param {*} request
'''


def welcome(request):
    return render(request, 'welcome.html')


'''
@description: 管理员登录
@Author: lyq
@Date: 2023-12-31 09:10:06
@return {*}
@param {*} request
'''


def adminlogin(request):
    # 如果是GET请求，则返回login_admin.html页面
    if request.method == "GET":
        return render(request, 'login_admin.html')
    # 获取POST请求中的username和password
    _name = request.POST.get('username')
    _password = request.POST.get('password')
    # 在Admin表中查询username和password相匹配的用户
    user = Admin.objects.filter(name=_name, password=_password).first()
    # 如果查询结果存在，则将用户名存储在session中，并返回200
    if user:
        request.session['user'] = _name
        return JsonResponse({"code": 200, "msg": "登录成功"})
    # 否则返回400
    else:
        return JsonResponse({"code": 400, "msg": "账户或密码错误"})


'''
@description: 商铺信息
@Author: lyq
@Date: 2023-12-31 09:10:29
@return {*}
'''


def listmerchant(request):
    merchants = Merchant.objects.all()
    if request.method == 'GET':
        return render(request, 'merchant/merchantlist.html', {'list': merchants})


def codegenerator(request):
    if request.method == 'GET':
        return render(request, 'codegenerator.html')
    if request.method == 'POST':
        model_fields = Orders._meta.get_fields()
        dicts = {}
        for field in model_fields:
            tmp = {field.name: field.verbose_name}
            dicts.update(tmp)
        return JsonResponse({"code": 200, "msg": "获取post数据成功", "data": dicts})


'''
@description: 促销表单
@Author: lyq
@Date: 2023-12-31 09:11:38
@return {*}
'''


class PublicmsgForm(ModelForm):
    class Meta:
        model = Publicmsg
        fields = "__all__"
        widgets = {
            "id": TextInput(attrs={"class": "form-control"}),
            "sn": TextInput(attrs={"class": "form-control"}),
            "title": TextInput(attrs={"class": "form-control"}),
            "content": TextInput(attrs={"class": "form-control"}),
            "status": TextInput(attrs={"class": "form-control"}),
            "expriy": TextInput(attrs={"class": "form-control"})
        }


def publicmsgadd(request):
    if request.method == 'GET':
        form = PublicmsgForm()
        return render(request, 'publicmsg/add.html', {'form': form})
    else:
        form = PublicmsgForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/publicmsglist')


def publicmsgedit(request):
    id = request.GET.get('id', None)
    merchant = Publicmsg.objects.get(id=id)
    if request.method == 'GET':
        form = PublicmsgForm(instance=merchant)
        return render(request, 'publicmsg/edit.html', {'form': form})
    if request.method == 'POST':
        form = PublicmsgForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/publicmsglist')


def publicmsgdel(request):
    id = request.GET.get('id', None)
    merchant = Publicmsg.objects.get(id=id)
    if request.method == 'GET':
        merchant.delete()
        return redirect('/publicmsglist')


def publicmsglist(request):
    list = Publicmsg.objects.all()
    return render(request, 'publicmsg/list.html', {'list': list})


class UserForm(ModelForm):
    class Meta:
        model = User
        # fields = ['name', 'password', 'email', 'gender']
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "password": PasswordInput(attrs={"class": "form-control"}),
            "email": TextInput(attrs={"class": "form-control"}),
            "role": TextInput(attrs={"class": "form-control"}),
            "integral": TextInput(attrs={"class": "form-control"}),
        }


'''
@description: 用户注册
@Author: lyq
@Date: 2023-12-31 09:13:52
@return {*}
@param {*} request
'''


def register(request):
    # 如果请求方法是GET，则返回用户注册表单
    if request.method == 'GET':
        form = UserForm()
        return render(request, 'register.html', {"form": form, "fsize": 40})
    # 如果请求方法是POST，则将请求数据绑定到用户注册表单
    form = UserForm(data=request.POST)
    # 如果用户注册表单有效，则保存用户信息并返回首页
    if form.is_valid():
        form.save()
        return render(request, 'index.html')
    # 如果用户注册表单无效，则返回用户注册表单
    else:
        return render(request, 'register.html', {"form": form, "fsize": 40})


'''
@description: 用户登录
@Author: lyq
@Date: 2023-12-31 09:14:10
@return {*}
'''


@csrf_exempt
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    form = UserForm(data=request.POST)
    _name = request.POST.get('name')
    _password = request.POST.get('password')
    user = User.objects.filter(name=_name, password=_password).first()
    if user:
        request.session['user'] = _name
        return JsonResponse({"code": 200, "msg": "登录成功"})
    else:
        return JsonResponse({"code": 400, "msg": "账户或密码错误"})


def edituser(request):
    if request.method == "GET":
        user = User.objects.filter(name=request.session['user']).first()
        print(user.name, "登录用户")
        form = UserForm(instance=user)
        return render(request, 'edituser.html', {"form": form})
    form = UserForm(data=request.POST, instance=User.objects.filter(name=request.session['user']).first())
    _name = request.POST.get('name')
    _password = request.POST.get('password')
    user = User.objects.filter(name=request.session['user']).first()
    user.save()
    return redirect('/edituser')


def my(request):
    user = request.session.get('user')
    if user is None:
        return redirect('/login')
    return render(request, 'my.html')


'''
@description: 我的信息
@Author: lyq
@Date: 2023-12-31 09:14:45
@return {*}
@param {*} request
'''


def myinfo(request):
    user = User.objects.filter(name=request.session['user']).first()
    print(user)
    if request.method == 'GET':
        form = UserForm(instance=user)
        return render(request, 'my/myinfo.html', {'form': form})
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('/myinfo')


class GoodsForm(ModelForm):
    class Meta:
        model = Goods
        fields = '__all__'
        # widgets = {"id": TextInput(attrs={"class": "form-control"}),
        #            "name": TextInput(attrs={"class": "form-control"}),
        #            "price": TextInput(attrs={"class": "form-control"}),
        #            "image": TextInput(attrs={"class": "form-control"}),
        #            # "category": ComboField(attrs={"class": "form-control"},fields=),
        #            "goodsdesc": Textarea(attrs={"class": "form-control"}),
        #            }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            print(field)
            field.widget.attrs = {"class": "form-control", "plcaeholder": field.label}


'''
@description: 商品列表
@Author: lyq
@Date: 2023-12-31 09:15:03
@return {*}
@param {*} request
'''


def goodslist(request):
    goods_list = Goods.objects.all()
    return render(request, 'goods/list.html', {'goods_list': goods_list})


def goodsadd(request):
    if request.method == 'GET':
        form = GoodsForm()

        return render(request, 'goods/add.html', {'form': form})
    else:
        form = GoodsForm(request.POST)

        if form.is_valid():

            # 获取表单数据
            pprint(form)
            name = form.cleaned_data['name']
            goodsdesc = form.cleaned_data['goodsdesc']
            print(name)
            if checkmgc(name) == True or checkmgc(goodsdesc) == True:
                return render(request, 'goods/add.html', {'form': form, 'msg': '商品名或商品描述存在敏感词'})

            form.save()
            return redirect('/goodslist')


def goodsedit(request):
    id = request.GET.get('id', None)
    merchant = Goods.objects.get(id=id)
    if request.method == 'GET':
        form = GoodsForm(instance=merchant)
        return render(request, 'goods/edit.html', {'form': form})

    if request.method == 'POST':
        form = GoodsForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/goodslist')


def goodsdel(request):
    id = request.GET.get('id', None)

    merchant = Goods.objects.get(id=id)

    if request.method == 'GET':
        merchant.delete()
        return redirect('/goodslist')


def goodslist(request):
    list = Goods.objects.all()
    return render(request, 'goods/list.html', {'list': list})


# 上传文件处理类

from django.core.files.storage import FileSystemStorage


def upload_file(request):
    print("处理上传图片")
    if request.method == 'POST' and request.FILES['imageFile']:
        print(request.FILES['imageFile'])
        myfile = request.FILES['imageFile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return JsonResponse({"code": 200, "msg": "参加成功", "data": uploaded_file_url})
    else:
        return JsonResponse({"code": 200, "msg": "上传失败"})


# 敏感词匹配  # 使用示例
# sensitive_positions = find_sensitive_words('这里是包含敏感词的文本', ['敏感词1', '敏感词2'])
def find_sensitive_words(text, words):
    # 构建正则表达式模式
    pattern = '|'.join(map(re.escape, words))
    # 匹配文本中的敏感词
    matches = re.finditer(pattern, text)
    return [(match.start(), match.end() - 1) for match in matches]


# 敏感词过滤
def checkmgc(txt):
    # huoqu敏感词库
    sensitives = Sensitive.objects.all()
    # 敏感词列表
    sensitive_list = []
    for sensitive in sensitives:

        for p in sensitive.word.split(','):
            sensitive_list.append(p)

    # 获取敏感词位置
    sensitive_positions = find_sensitive_words(txt, sensitive_list)
    if len(sensitive_positions) > 0:
        print("检测出敏感词，已替换")
        return True
    else:
        return False
    # 替换敏感词
    # for start, end in sensitive_positions:
    #     txt = txt[:start] + '*' * (end - start + 1) + txt[end + 1:]
    # return txt


class SensitiveForm(ModelForm):
    class Meta:
        model = Sensitive
        fields = "__all__"
        widgets = {"id": TextInput(attrs={"class": "form-control"}),
                   "word": TextInput(attrs={"class": "form-control"}),
                   }


def sensitiveadd(request):
    if request.method == 'GET':
        form = SensitiveForm()
        return render(request, 'sensitive/add.html', {'form': form})
    else:
        form = SensitiveForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('/sensitivelist')


def sensitiveedit(request):
    id = request.GET.get('id', None)
    merchant = Sensitive.objects.get(id=id)
    if request.method == 'GET':
        form = SensitiveForm(instance=merchant)
        return render(request, 'sensitive/edit.html', {'form': form})

    if request.method == 'POST':
        form = SensitiveForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/sensitivelist')


def sensitivedel(request):
    id = request.GET.get('id', None)

    merchant = Sensitive.objects.get(id=id)

    if request.method == 'GET':
        merchant.delete()
        return redirect('/sensitivelist')


def sensitivelist(request):
    list = Sensitive.objects.all()
    return render(request, 'sensitive/list.html', {'list': list})


class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = "__all__"
        widgets = {"id": TextInput(attrs={"class": "form-control"}),
                   "name": TextInput(attrs={"class": "form-control"}),
                   "createtime": TextInput(attrs={"class": "form-control"}),
                   }


def categoryadd(request):
    if request.method == 'GET':
        form = CategoryForm()
        return render(request, 'category/add.html', {'form': form})
    else:
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/categorylist')


def categoryedit(request):
    id = request.GET.get('id', None)
    merchant = Category.objects.get(id=id)
    if request.method == 'GET':
        form = CategoryForm(instance=merchant)
        return render(request, 'category/edit.html', {'form': form})

    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/categorylist')


def categorydel(request):
    id = request.GET.get('id', None)

    merchant = Category.objects.get(id=id)

    if request.method == 'GET':
        merchant.delete()
        return redirect('/categorylist')


def categorylist(request):
    list = Category.objects.all()
    return render(request, 'category/list.html', {'list': list})


class OrdersForm(ModelForm):
    class Meta:
        model = Orders
        fields = "__all__"
        widgets = {"id": TextInput(attrs={"class": "form-control"}),
                   "orderid": TextInput(attrs={"class": "form-control"}),
                   "userid": TextInput(attrs={"class": "form-control"}),
                   "goodsid": TextInput(attrs={"class": "form-control"}),
                   "goodsname": TextInput(attrs={"class": "form-control"}),
                   "goodsnum": TextInput(attrs={"class": "form-control"}),
                   "goodsprice": TextInput(attrs={"class": "form-control"}),
                   "fee": TextInput(attrs={"class": "form-control"}),
                   "total": TextInput(attrs={"class": "form-control"}),
                   "ordertime": TextInput(attrs={"class": "form-control"}),
                   "orderstatus": TextInput(attrs={"class": "form-control"}),
                   "address": TextInput(attrs={"class": "form-control"}),
                   "name": TextInput(attrs={"class": "form-control"}),
                   "phone": TextInput(attrs={"class": "form-control"}),
                   "remark": TextInput(attrs={"class": "form-control"}),
                   }


def ordersadd(request):
    if request.method == 'GET':
        form = OrdersForm()
        return render(request, 'orders/add.html', {'form': form})
    else:
        form = OrdersForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/orderslist')


def ordersedit(request):
    id = request.GET.get('id', None)
    merchant = Orders.objects.get(id=id)
    if request.method == 'GET':
        form = OrdersForm(instance=merchant)
        return render(request, 'orders/edit.html', {'form': form})

    if request.method == 'POST':
        form = OrdersForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/orderslist')


def ordersdel(request):
    id = request.GET.get('id', None)

    merchant = Orders.objects.get(id=id)

    if request.method == 'GET':
        merchant.delete()
        return redirect('/orderslist')


def orderslist(request):
    list = Orders.objects.all()
    return render(request, 'orders/list.html', {'list': list})


###########API=========================
# 商品模糊查询
class GoodsSearch(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # 这里可以直接获取POST请求的JSON数据
        _name = ""
        if 'name' in data:
            _name = data['name']

        # _password = data['password']
        print(_name)
        print("================")
        decoded_url = unquote(_name)
        print(decoded_url)
        if _name:
            goods = Goods.objects.filter(name=decoded_url)

            json_data = serializers.serialize('json', goods)
            return JsonResponse({"code": 200, "msg": "获取成功", "data": json_data})
        else:
            goods = Goods.objects.all()
            json_data = serializers.serialize('json', goods)
            return JsonResponse({"code": 200, "msg": "获取成功", "data": json_data})


# 商品类型模糊查询
class CateSearch(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # 这里可以直接获取POST请求的JSON数据
        _name = ""
        if 'name' in data:
            _name = data['name']

        # _password = data['password']
        print(_name)

        if _name:
            goods = Category.objects.filter(name=_name)

            json_data = serializers.serialize('json', goods)
            return JsonResponse({"code": 200, "msg": "获取成功", "data": json_data})
        else:
            goods = Category.objects.all()
            json_data = serializers.serialize('json', goods)
            return JsonResponse({"code": 200, "msg": "获取成功", "data": json_data})


# 商品类型模糊查询
class GetGoodsbyId(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # 这里可以直接获取POST请求的JSON数据
        _name = "1"
        if 'id' in data:
            _name = data['id']

        # _password = data['password']
        print(_name)

        goods = Goods.objects.get(id=_name)
        pprint(goods)

        json_data = serializers.serialize('json', [goods])

        return Response({"code": 200, "msg": "获取成功", "data": json_data})


# 商品类型模糊查询
class AddOrders(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # 这里可以直接获取POST请求的JSON数据
        ord=Orders()
        ord.goodsname=data['goodsname']
        ord.goodsnum=data['goodsnum']
        ord.goodsprice=data['goodsprice']
        ord.total=int(ord.goodsnum)*int(ord.goodsprice)
        ord.userid=data['userid']
        now = datetime.now()
        ord.ordertime=now.strftime('%Y-%m-%d %H:%M:%S')
        ord.orderstatus="已下单"
        ord.save()
        # _password = data['password']
        print(data)
        return Response({"code": 200, "msg": "获取成功"})

#获取用户订单
class GetOrders(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # 这里可以直接获取POST请求的JSON数据
        _name = "1"
        if 'userid' in data:
            _name = data['userid']

        # _password = data['password']
        print(_name)

        orders = Orders.objects.filter(userid=_name)
        json_data = serializers.serialize('json', orders)
        return Response({"code": 200, "msg": "获取成功", "data": json_data})

#登录
class APILogin(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # 这里可以直接获取POST请求的JSON数据
        print(data)
        _name = "1"
        _password = "1"
        if 'username' in data:
            _name = data['username']
        if 'password' in data:
            _password = data['password']
        print(_name)
        print(_password)
        user = User.objects.filter(name=_name, password=_password)
        if user:
            return Response({"code": 200, "msg": "登录成功"})
        else:
            return Response({"code": 409, "msg": "用户名或密码错误"})

#注册
class APIRegister(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data  # 这里可以直接获取POST请求的JSON数据
        pprint(data)
        _name = "1"
        _password = "1"
        if 'name' in data:
            _name = data['name']
        if 'password' in data:
            _password = data['password']
        print(_name)
        print(_password)
        print("==================")
        user = User.objects.filter(name=_name)
        if user:
            return Response({"code": 400, "msg": "用户名已存在"})
        else:
            user = User.objects.create(name=_name, password=_password)
            return Response({"code": 200, "msg": "注册成功"})