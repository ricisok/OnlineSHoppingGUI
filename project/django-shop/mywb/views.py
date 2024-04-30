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


def getmchine(request):
    objs = machine.objects.all()
    print(len(objs))
    cas = []
    for c in objs:
        print(c)
        p = {"area": c.area, "machine": c.machine}
        cas.append(p)
    return JsonResponse({"code": 200, "data": cas})
    return JsonResponse({"code": 200, "msg": "获取机器成功", "data": cas})


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
    service = Service.objects.all()
    promotion = Promotion.objects.all()
    goods=Goods.objects.all()
    shls = Merchant.objects.all()
    return render(request, 'index.html', {'msg': msg, 'services': service, 'promotions': promotion, 'goods': goods})


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
    count_mer = len(Merchant.objects.all())
    count_ht = len(Contract.objects.all())
    print(count_ht, "合同数")
    count_jf = len(Charge.objects.all())
    print(count_jf, "缴费数")
    return render(request, 'welcome.html', {'count_mer': count_mer, 'count_ht': count_ht, 'count_jf': count_jf})


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


class ShopForm(ModelForm):
    class Meta:
        model = ShopInfo
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "password": PasswordInput(attrs={"class": "form-control"}),
            "email": TextInput(attrs={"class": "form-control"}),
            # "gender": ChoiceField(attrs={"class": "form-control"})
        }


class ShopEditForm(ModelForm):
    class Meta:
        model = ShopInfo
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "phone": TextInput(attrs={"class": "form-control"}),
            "email": TextInput(attrs={"class": "form-control"}),
            "qq": TextInput(attrs={"class": "form-control"}),
            "wechat": TextInput(attrs={"class": "form-control"}),
            # "gender": ChoiceField(attrs={"class": "form-control"})
        }


def shopinfo(request):
    shops = ShopInfo.objects.all().first()
    if request.method == 'GET':
        if shops:
            form = ShopEditForm(instance=shops)
            return render(request, 'shopinfo.html', {"form": form})
        else:
            form = ShopForm()
            return render(request, 'shopinfo.html', {"form": form})
    if shops:
        form = ShopEditForm(instance=shops, data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'shopinfo.html')
    else:
        form = ShopForm(data=request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'shopinfo.html')


def listmerchant(request):
    merchants = Merchant.objects.all()
    if request.method == 'GET':
        return render(request, 'merchant/merchantlist.html', {'list': merchants})


class MerchantForm(ModelForm):
    class Meta:
        model = Merchant
        fields = "__all__"
        widgets = {
            "name": TextInput(attrs={"class": "form-control"}),
            "phone": TextInput(attrs={"class": "form-control"}),
            "jylx": TextInput(attrs={"class": "form-control"}),
            "level": TextInput(attrs={"class": "form-control"}),
            "address": TextInput(attrs={"class": "form-control"}),
        }


def merchantadd(request):
    if request.method == 'GET':
        form = MerchantForm()
        return render(request, 'merchant/merchantadd.html', {"form": form})
    if request.method == 'POST':
        form = MerchantForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/listmerchant')


def merchantedit(request):
    id = request.GET.get('id', None)
    merchant = Merchant.objects.get(id=id)
    if request.method == 'GET':
        form = MerchantForm(instance=merchant)
        return render(request, 'merchant/merchantedit.html', {"form": form})
    if request.method == 'POST':
        form = MerchantForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/listmerchant')


def merchantdel(request):
    id = request.GET.get('id', None)
    merchant = Merchant.objects.get(id=id)
    if request.method == 'GET':
        merchant.delete()
        return redirect('/listmerchant')


'''
@description: 合同的表单模版
@Author: lyq
@Date: 2023-12-31 09:11:01
@return {*}
'''


class ContractForm(ModelForm):
    class Meta:
        model = Contract
        fields = "__all__"
        widgets = {
            "sn": TextInput(attrs={"class": "form-control"}),
            "title": TextInput(attrs={"class": "form-control"}),
            "money": TextInput(attrs={"class": "form-control"}),
            "start_time": TextInput(attrs={"class": "form-control"}),
            "end_time": TextInput(attrs={"class": "form-control"}),
            "status": TextInput(attrs={"class": "form-control"}),
            "create_time": TextInput(attrs={"class": "form-control"}),
            "party1": TextInput(attrs={"class": "form-control"}),
            "party2": TextInput(attrs={"class": "form-control"}),
            "party3": TextInput(attrs={"class": "form-control"}),
            "remark": TextInput(attrs={"class": "form-control"}),
        }


def contractlist(request):
    contract = Contract.objects.all()
    pprint(contract)
    return render(request, 'contract/list.html', {"list": contract})


def contractadd(request):
    if request.method == 'GET':
        form = ContractForm()
        return render(request, 'contract/add.html', {"form": form})
    if request.method == 'POST':
        form = ContractForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/contractlist')


def contractedit(request):
    id = request.GET.get('id', None)
    merchant = Contract.objects.get(id=id)
    if request.method == 'GET':
        form = ContractForm(instance=merchant)
        return render(request, 'contract/edit.html', {"form": form})
    if request.method == 'POST':
        form = ContractForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/contractlist')


def contractdel(request):
    id = request.GET.get('id', None)
    merchant = Contract.objects.get(id=id)
    if request.method == 'GET':
        merchant.delete()
        return redirect('/contractlist')


def codegenerator(request):
    if request.method == 'GET':
        return render(request, 'codegenerator.html')
    if request.method == 'POST':
        model_fields = Goods._meta.get_fields()
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


class ChargeForm(ModelForm):
    class Meta:
        model = Charge
        fields = "__all__"
        widgets = {
            "id": TextInput(attrs={"class": "form-control"}),
            "sn": TextInput(attrs={"class": "form-control"}),
            "merchant": TextInput(attrs={"class": "form-control"}),
            "title": TextInput(attrs={"class": "form-control"}),
            "money": TextInput(attrs={"class": "form-control"}),
            "status": TextInput(attrs={"class": "form-control"}),
            "create_time": TextInput(attrs={"class": "form-control"}),
        }


def chargeadd(request):
    if request.method == 'GET':
        print("收费add")
        form = ChargeForm()
        return render(request, 'charge/add.html', {'form': form})
    else:
        form = ChargeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/chargelist')


def chargeedit(request):
    id = request.GET.get('id', None)
    merchant = Charge.objects.get(id=id)
    if request.method == 'GET':
        form = ChargeForm(instance=merchant)
        return render(request, 'charge/edit.html', {'form': form})
    if request.method == 'POST':
        form = ChargeForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/chargelist')


def chargedel(request):
    id = request.GET.get('id', None)
    merchant = Charge.objects.get(id=id)
    if request.method == 'GET':
        merchant.delete()
        return redirect('/chargelist')


def chargelist(request):
    list = Charge.objects.all()
    print(list)
    return render(request, 'charge/list.html', {"list": list})


class PromotionForm(ModelForm):
    class Meta:
        model = Promotion
        fields = "__all__"
        widgets = {
            "id": TextInput(attrs={"class": "form-control"}),
            "sn": TextInput(attrs={"class": "form-control"}),
            "title": TextInput(attrs={"class": "form-control"}),
            "address": TextInput(attrs={"class": "form-control"}),
            "start_time": TextInput(attrs={"class": "form-control"}),
            "end_time": TextInput(attrs={"class": "form-control"}),
            "money": TextInput(attrs={"class": "form-control"}),
            "status": TextInput(attrs={"class": "form-control"}),
            "create_time": TextInput(attrs={"class": "form-control"}),
        }


# 商城促销模块
def promotionadd(request):
    if request.method == 'GET':
        form = PromotionForm()
        return render(request, 'promotion/add.html', {'form': form})
    else:
        form = PromotionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/promotionlist')


def promotionedit(request):
    id = request.GET.get('id', None)
    merchant = Promotion.objects.get(id=id)
    if request.method == 'GET':
        form = PromotionForm(instance=merchant)
        return render(request, 'promotion/edit.html', {'form': form})
    if request.method == 'POST':
        form = PromotionForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/promotionlist')


def promotiondel(request):
    id = request.GET.get('id', None)
    merchant = Promotion.objects.get(id=id)
    if request.method == 'GET':
        merchant.delete()
        return redirect('/promotionlist')


def promotionlist(request):
    list = Promotion.objects.all()
    return render(request, 'promotion/list.html', {'list': list})


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
        return render(request, 'register.html', {"form": form,"fsize":40})
    # 如果请求方法是POST，则将请求数据绑定到用户注册表单
    form = UserForm(data=request.POST)
    # 如果用户注册表单有效，则保存用户信息并返回首页
    if form.is_valid():
        form.save()
        return render(request, 'index.html')
    # 如果用户注册表单无效，则返回用户注册表单
    else:
        return render(request, 'register.html', {"form": form,"fsize":40})


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


'''
@description: 服务项目管理
@Author: lyq
@Date: 2023-12-31 09:13:40
@return {*}
'''


class ServiceForm(ModelForm):
    class Meta:
        model = Service
        fields = "__all__"
        widgets = {
            "id": TextInput(attrs={"class": "form-control"}),
            "title": TextInput(attrs={"class": "form-control"}),
            "content": TextInput(attrs={"class": "form-control"}),
            "status": TextInput(attrs={"class": "form-control"}),
            "price": TextInput(attrs={"class": "form-control"}),
            "img": TextInput(attrs={"class": "form-control"}),
        }


def serviceadd(request):
    if request.method == 'GET':
        form = ServiceForm()
        return render(request, 'service/add.html', {'form': form})
    else:
        form = ServiceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/servicelist')


def serviceedit(request):
    id = request.GET.get('id', None)
    merchant = Service.objects.get(id=id)
    if request.method == 'GET':
        form = ServiceForm(instance=merchant)
        return render(request, 'service/edit.html', {'form': form})
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/servicelist')


def servicedel(request):
    id = request.GET.get('id', None)
    merchant = Service.objects.get(id=id)
    if request.method == 'GET':
        merchant.delete()
        return redirect('/servicelist')


def servicelist(request):
    list = Service.objects.all()
    return render(request, 'service/list.html', {'list': list})


'''
@description: 设备管理
@Author: lyq
@Date: 2023-12-31 09:13:25
@return {*}
'''


class DeviceForm(ModelForm):
    class Meta:
        model = Device
        fields = "__all__"
        widgets = {
            "id": TextInput(attrs={"class": "form-control"}),
            "devicesn": TextInput(attrs={"class": "form-control"}),
            "devicename": TextInput(attrs={"class": "form-control"}),
            "devicetype": TextInput(attrs={"class": "form-control"}),
            "devicestatus": TextInput(attrs={"class": "form-control"}),
            "devicetime": TextInput(attrs={"class": "form-control"}),
            "deviceaddress": TextInput(attrs={"class": "form-control"}),
        }


def deviceadd(request):
    if request.method == 'GET':
        form = DeviceForm()
        return render(request, 'device/add.html', {'form': form})
    else:
        form = DeviceForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/devicelist')


def deviceedit(request):
    id = request.GET.get('id', None)
    merchant = Device.objects.get(id=id)
    if request.method == 'GET':
        form = DeviceForm(instance=merchant)
        return render(request, 'device/edit.html', {'form': form})
    if request.method == 'POST':
        form = DeviceForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/devicelist')


def devicedel(request):
    id = request.GET.get('id', None)
    merchant = Device.objects.get(id=id)
    if request.method == 'GET':
        merchant.delete()
        return redirect('/devicelist')


def devicelist(request):
    list = Device.objects.all()
    return render(request, 'device/list.html', {'list': list})


'''
@description: 停车表单
@Author: lyq
@Date: 2023-12-31 09:14:25
@return {*}
'''


class ParkingForm(ModelForm):
    class Meta:
        model = Parking
        fields = "__all__"
        widgets = {
            "id": TextInput(attrs={"class": "form-control"}),
            "Vehicletype": TextInput(attrs={"class": "form-control"}),
            "Vehiclenum": TextInput(attrs={"class": "form-control"}),
            "Parkingtime": TextInput(attrs={"class": "form-control"}),
            "Parkingfee": TextInput(attrs={"class": "form-control"}),
            "entrytime": TextInput(attrs={"class": "form-control"}),
            "exittime": TextInput(attrs={"class": "form-control"}),
            "status": TextInput(attrs={"class": "form-control"}),
        }


def parkingadd(request):
    if request.method == 'GET':
        form = ParkingForm()
        return render(request, 'parking/add.html', {'form': form})
    else:
        form = ParkingForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/parkinglist')


'''
@description: 停车场管理
@Author: lyq
@Date: 2023-12-31 09:13:10
@return {*}
@param {*} request
'''


def parkingedit(request):
    id = request.GET.get('id', None)
    merchant = Parking.objects.get(id=id)
    if request.method == 'GET':
        form = ParkingForm(instance=merchant)
        return render(request, 'parking/edit.html', {'form': form})
    if request.method == 'POST':
        form = ParkingForm(request.POST, instance=merchant)
        if form.is_valid():
            form.save()
            return redirect('/parkinglist')


def parkingdel(request):
    # Get the id of the parking space to be deleted
    id = request.GET.get('id', None)
    # Get the parking space object to be deleted
    merchant = Parking.objects.get(id=id)
    # If the request method is GET, delete the parking space and redirect to the parking list page
    if request.method == 'GET':
        merchant.delete()
        return redirect('/parkinglist')


def parkinglist(request):
    list = Parking.objects.all()
    return render(request, 'parking/list.html', {'list': list})


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


def cxlist(request):
    user_id = request.session.get('user')
    list = Cxlist.objects.filter(name=user_id)
    return render(request, 'my/cxlist.html', {'list': list})


def myslist(request):
    return render(request, 'my/servicelist.html')


'''
@description: 参加促销活动
@Author: lyq
@Date: 2023-12-31 09:12:53
@return {*}
@param {*} request
'''


def joincx(request):
    # _id = request.POST.get('id')
    # print(_id, "URL参数id")
    if request.method == 'POST':
        _id = request.POST.get('id')
        print(_id, "URL参数id")
        cx = Promotion.objects.get(id=_id)
        print(cx)
        mycx = Cxlist()
        mycx.name = request.session.get('user')
        mycx.cxname = cx.title
        mycx.cxstarttime = cx.start_time
        mycx.status = "报名参与"
        mycx.save()
        return JsonResponse({"code": 200, "msg": "参加成功"})


'''
@description: 促销展示
@Author: lyq
@Date: 2023-12-31 09:12:13
@return {*}
@param {*} request
'''


def cxshow(request):
    if request.method == "GET":
        id = request.GET.get('id')
        cx = Promotion.objects.get(id=id)
        return render(request, 'promotion/show.html', {"cx": cx})
    else:
        _id = request.POST.get('id')
        cx = Promotion.objects.get(id=_id)
        cx.save()
        return redirect('/index')


'''
@description: 促销删除

@Author: lyq
@Date: 2023-12-31 09:12:24
@return {*}
@param {*} request
'''


def cxlistdel(request):
    id = request.GET.get('id')
    merchant = Cxlist.objects.get(id=id)
    if request.method == 'GET':
        merchant.delete()
        return redirect('/my')


'''
@description: 服务展示
@Author: lyq
@Date: 2023-12-31 09:12:38
@return {*}
@param {*} request
'''


def serviceshow(request):
    if request.method == "GET":
        id = request.GET.get('id')
        cx = Service.objects.get(id=id)
        return render(request, 'service/show.html', {"cx": cx})


class GoodsForm(ModelForm):
    class Meta:
        model = Goods
        fields = "__all__"
        widgets = {"id": TextInput(attrs={"class": "form-control"}),
                   "name": TextInput(attrs={"class": "form-control"}),
                   "price": TextInput(attrs={"class": "form-control"}),
                   "goodstype": TextInput(attrs={"class": "form-control"}),
                   "image": TextInput(attrs={"class": "form-control"}),
                   "goodsdesc": TextInput(attrs={"class": "form-control"}),
                   }


def goodsadd(request):
    if request.method == 'GET':
        form = GoodsForm()
        return render(request, 'goods/add.html', {'form': form})
    else:
        form = GoodsForm(request.POST)
        if form.is_valid():
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

#上传文件处理类

from django.core.files.storage import FileSystemStorage

def upload_file(request):
    print("处理上传图片")
    if request.method == 'POST' and request.FILES['imageFile']:
        print(request.FILES['imageFile'])
        myfile = request.FILES['imageFile']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return JsonResponse({"code": 200, "msg": "参加成功","data":uploaded_file_url})
    else:
        return JsonResponse({"code": 200, "msg": "上传失败"})
