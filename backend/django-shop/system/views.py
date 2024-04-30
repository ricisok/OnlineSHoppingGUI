from django import http
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.core import  serializers

from system.models import machine, data, alarm,reject_module1,reject_module2


def getmchine(request):
    objs = machine.objects.all()
    print(len(objs))
    cas = []

    for c in objs:
        print(c)
        p = {"area": c.area,"machine":c.machine}
        cas.append(p)
    return JsonResponse({"code": 200, "data": cas})
    return JsonResponse({"code": 200, "msg": "获取机器成功","data":cas})

def getpostdata(request):
    machine=  request.POST.get('machine')
    obj=data.objects.filter(machine=machine)
    print(obj)
    json_data = serializers.serialize('json', obj)
    # 打印JSON数据
    print(json_data)
    return HttpResponse(json_data)
    # return JsonResponse({"code": 200, "msg": "获取数据成功", "data": json_data})

def getpostalarm(request):
    machine = request.POST.get('machine')
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    if startDate == None or endDate == None:
        ls=alarm.objects.filter(machine=machine)
        json_data = serializers.serialize('json', ls)
        return HttpResponse(json_data)


    # obj=data.objects.filter(machine=machine)
    # print(obj)
    # json_data = serializers.serialize('json', obj)
    # # 打印JSON数据
    # print(json_data)
    # return HttpResponse(json_data)
    # # return JsonResponse({"code": 200, "msg": "获取数据成功", "data": json_data})
def getpostreject(request):
    machine = request.POST.get('machine')
    mz1=reject_module1.objects.filter(machine_id=machine)
    mz2=reject_module2.objects.filter(machine_id=machine)
    dict1=[]
    dict2=[]
    for i in mz1:
        _t={ "reject":i.reject,"count":i.count}
        dict1.append(_t)
    for i in mz2:
        _t = {"reject": i.reject, "count": i.count}
        dict2.append(_t)

    ret={
        "machine":machine,
        "module1":{
            "name":'组件1',
            "param":dict1

        },
        "module2": {
            "name": '组件2',
            "param": dict2

        }

    }
    return JsonResponse({"code": 200, "msg": "获取数据成功", "data": ret})




