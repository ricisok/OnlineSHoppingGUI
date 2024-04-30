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
    path("shopinfo/",wb.shopinfo),
    path("listmerchant/",wb.listmerchant),
    path("merchantadd/",wb.merchantadd),
    path("merchantedit/",wb.merchantedit),
    path("merchantdel/",wb.merchantdel),

    path("contractlist/",wb.contractlist),
    path("contractadd/",wb.contractadd),
    path("contractedit/",wb.contractedit),
    path("contractdel/",wb.contractdel),
    path("codegenerator/",wb.codegenerator),


    path("chargelist/", wb.chargelist),
    path("chargeadd/", wb.chargeadd),
    path("chargeedit/", wb.chargeedit),
    path("chargedel/", wb.chargedel),

    path("promotionlist/", wb.promotionlist),
    path("promotionadd/", wb.promotionadd),
    path("promotionedit/", wb.promotionedit),
    path("promotiondel/", wb.promotiondel),

    path("publicmsglist/", wb.publicmsglist),
    path("publicmsgadd/", wb.publicmsgadd),
    path("publicmsgedit/", wb.publicmsgedit),
    path("publicmsgdel/", wb.publicmsgdel),

    path("servicelist/", wb.servicelist),
    path("serviceadd/", wb.serviceadd),
    path("serviceedit/", wb.serviceedit),
    path("servicedel/", wb.servicedel),

    path("login/", wb.login),
    path("register/", wb.register),
    path("edituser/", wb.edituser),

    path("devicelist/", wb.devicelist),
    path("deviceadd/", wb.deviceadd),
    path("deviceedit/", wb.deviceedit),
    path("devicedel/", wb.devicedel),

    path("goodslist/", wb.goodslist),
    path("goodsadd/", wb.goodsadd),
    path("goodsedit/", wb.goodsedit),
    path("goodsdel/", wb.goodsdel),

    path("parkinglist/", wb.parkinglist),
    path("parkingadd/", wb.parkingadd),
    path("parkingedit/", wb.parkingedit),
    path("parkingdel/", wb.parkingdel),
    path("my/", wb.my),

    path("myinfo/", wb.myinfo),
    path("cxlist/", wb.cxlist),
    path("myslist/", wb.myslist),

    path("cxshow/", wb.cxshow),
    path("joincx/", wb.joincx),
    path("cxlistdel/", wb.cxlistdel),
    path("serviceshow/",wb.serviceshow),

    #上传数据
    path("uploadfile/",wb.upload_file)
    # path("api/test/get_machine",sy.getmchine),
    # path("api/test/post_data",sy.getpostdata),
    # path("api/test/post_alarm",sy.getpostalarm),
    # path("api/test/post_reject",sy.getpostreject)
    # path("api/test/post_data",view.getPostData),
    # path("api/test/post_alarm",views.getPostalarm),



]
