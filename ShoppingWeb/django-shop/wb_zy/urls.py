"""
URL configuration for wb_zy project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.views.static import serve
from django.conf import settings
from django.urls import path,re_path
from mywb import views as wb
from system import views as sy


urlpatterns = [
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),

    # path('admin/', admin.site.urls),
    #路由对应
    #默认首页的第一个参数为空
    path("",wb.index),
    path("index/", wb.index),
    path("admin/",wb.admin),
    path("test/",wb.test),
    path("welcome/",wb.welcome),

    path("adminlogin/",wb.adminlogin),


    path("codegenerator/",wb.codegenerator),



    path("publicmsglist/", wb.publicmsglist),
    path("publicmsgadd/", wb.publicmsgadd),
    path("publicmsgedit/", wb.publicmsgedit),
    path("publicmsgdel/", wb.publicmsgdel),

    path("login/", wb.login),
    path("register/", wb.register),
    path("edituser/", wb.edituser),


    path("goodslist/", wb.goodslist),
    path("goodsadd/", wb.goodsadd),
    path("goodsedit/", wb.goodsedit),
    path("goodsdel/", wb.goodsdel),


    path("my/", wb.my),

    path("sensitivelist/", wb.sensitivelist),
    path("sensitiveadd/", wb.sensitiveadd),
    path("sensitiveedit/", wb.sensitiveedit),
    path("sensitivedel/", wb.sensitivedel),

    path("categorylist/", wb.categorylist),
    path("categoryadd/", wb.categoryadd),
    path("categoryedit/", wb.categoryedit),
    path("categorydel/", wb.categorydel),

    #上传数据
    path("uploadfile/",wb.upload_file),

    path("orderslist/", wb.orderslist),
    path("ordersadd/", wb.ordersadd),
    path("ordersedit/", wb.ordersedit),
    path("ordersdel/", wb.ordersdel),

    #######api=========================

    path("goodssearch/", wb.GoodsSearch.as_view()),
    path("catesearch/", wb.CateSearch.as_view()),
    path("getgoodsbyid/", wb.GetGoodsbyId.as_view()),
    path("addorder/", wb.AddOrders.as_view()),
    path("getorder/", wb.GetOrders.as_view()),


    path("apilogin/",wb.APILogin.as_view()),
    path("apiregister/",wb.APIRegister.as_view())

    # path("api/test/get_machine",sy.getmchine),
    # path("api/test/post_data",sy.getpostdata),
    # path("api/test/post_alarm",sy.getpostalarm),
    # path("api/test/post_reject",sy.getpostreject)
    # path("api/test/post_data",view.getPostData),
    # path("api/test/post_alarm",views.getPostalarm),



]
