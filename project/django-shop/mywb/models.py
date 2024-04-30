from django.db import models
# Create your models here.
class User(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=100)
    gender_choices = (("1", "男"), ("2", "女"))
    gender = models.CharField(verbose_name="性别", max_length=100, choices=gender_choices)
    password = models.CharField(verbose_name="密码", max_length=100)
    email = models.CharField(verbose_name="邮箱", max_length=100)
    role = models.CharField(verbose_name="角色", max_length=100, default="普通用户")
    integral = models.IntegerField(verbose_name="积分", default=0)
class Blogdoc(models.Model):
    name = models.CharField(verbose_name="博客名", max_length=100)
    content = models.TextField(verbose_name="博客内容")
    createtime = models.DateTimeField(verbose_name="创建时间")
    category = models.CharField(verbose_name="博客分类", max_length=100)
    image = models.FileField(verbose_name="博客图片", max_length=300, upload_to="blog/images/")
    user = models.TextField(verbose_name="发布人", max_length=100)
class Comment(models.Model):
    content = models.TextField(verbose_name="评论内容")
    createtime = models.DateTimeField(verbose_name="创建时间")
    blogdoc = models.ForeignKey(Blogdoc, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
class Category(models.Model):
    name = models.CharField(verbose_name="分类名", max_length=100)
    createtime = models.DateTimeField(verbose_name="创建时间")
class example(models.Model):
    class Mete:
        db_table = 'system_example'  # 指明数据库表名 默认 appname_modelname
    machine = models.IntegerField(verbose_name="机器号", max_length=100, default="")
    score = models.CharField(verbose_name="分数", max_length=100, default="")
class machine(models.Model):
    class Mete:
        db_table = 'system_machine'  # 指明数据库表名 默认 appname_modelname
    machine = models.CharField(verbose_name="机器名", max_length=100, default="")
    area = models.CharField(verbose_name="区域", max_length=100, default="")
class Admin(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=100)
    password = models.CharField(verbose_name="密码", max_length=100)
    email = models.CharField(verbose_name="邮箱", max_length=100)
class ShopInfo(models.Model):
    name = models.CharField(verbose_name="店铺名", max_length=100)
    phone = models.CharField(verbose_name="电话", max_length=100)
    email = models.CharField(verbose_name="邮箱", max_length=100)
    qq = models.CharField(verbose_name="QQ", max_length=100)
    wechat = models.CharField(verbose_name="微信", max_length=100)
class Merchant(models.Model):
    name = models.CharField(verbose_name="商户名", max_length=100)
    phone = models.CharField(verbose_name="电话", max_length=100)
    jylx = models.CharField(verbose_name="经营类型", max_length=100)
    level = models.CharField(verbose_name="商户级别", max_length=100)
    address = models.CharField(verbose_name="地址", max_length=100)
class Contract(models.Model):
    sn = models.CharField(verbose_name="合同编号", max_length=100)
    title = models.CharField(verbose_name="合同名称", max_length=100)
    money = models.CharField(verbose_name="合同金额", max_length=100)
    start_time = models.CharField(verbose_name="开始时间", max_length=100)
    end_time = models.CharField(verbose_name="结束时间", max_length=100)
    status = models.CharField(verbose_name="合同状态", max_length=100)
    create_time = models.CharField(verbose_name="创建时间", max_length=100)
    party1 = models.CharField(verbose_name="甲方", max_length=100)
    party2 = models.CharField(verbose_name="乙方", max_length=100)
    party3 = models.CharField(verbose_name="丙方", max_length=100)
    remarm = models.CharField(verbose_name="备注", max_length=100)
class Charge(models.Model):
    sn = models.CharField(verbose_name="缴费编号", max_length=100)
    merchant = models.CharField(verbose_name="缴费商户", max_length=100)
    title = models.CharField(verbose_name="缴费名称", max_length=100)
    money = models.CharField(verbose_name="缴费金额", max_length=100)
    status = models.CharField(verbose_name="缴费状态", max_length=100)
    create_time = models.CharField(verbose_name="创建时间", max_length=100)
class Promotion(models.Model):
    sn = models.CharField(verbose_name="促销编号", max_length=100)
    title = models.CharField(verbose_name="促销名称", max_length=100)
    address = models.CharField(verbose_name="促销地点", max_length=100)
    start_time = models.CharField(verbose_name="开始时间", max_length=100)
    end_time = models.CharField(verbose_name="结束时间", max_length=100)
    money = models.CharField(verbose_name="促销金额", max_length=100)
    status = models.CharField(verbose_name="促销状态", max_length=100)
    create_time = models.CharField(verbose_name="创建时间", max_length=100)
    def __str__(self):
        return self.title
# 公告
class Publicmsg(models.Model):
    sn = models.CharField(verbose_name="公告编号", max_length=100)
    title = models.CharField(verbose_name="公告标题", max_length=100)
    content = models.CharField(verbose_name="公告内容", max_length=100)
    status = models.CharField(verbose_name="公告状态", max_length=100)
    expriy = models.IntegerField(verbose_name="公告过期时间", max_length=100)
# 服务项目
class Service(models.Model):
    title = models.CharField(verbose_name="服务名称", max_length=100)
    content = models.CharField(verbose_name="服务内容", max_length=100)
    status = models.CharField(verbose_name="提供商户", max_length=100)
    price = models.CharField(verbose_name="服务价格", max_length=100)
class Parking(models.Model):
    Vehicletype = models.CharField(verbose_name="车辆类型", max_length=100)
    Vehiclenum = models.CharField(verbose_name="车辆号码", max_length=100)
    Parkingtime = models.CharField(verbose_name="停车时间", max_length=100)
    Parkingfee = models.CharField(verbose_name="停车费用", max_length=100)
    entrytime = models.CharField(verbose_name="入场时间", max_length=100)
    exittime = models.CharField(verbose_name="出场时间", max_length=100)
    status = models.CharField(verbose_name="停车状态", max_length=100)
class Device(models.Model):
    devicesn = models.CharField(verbose_name="设备编号", max_length=100)
    devicename = models.CharField(verbose_name="设备名称", max_length=100)
    devicetype = models.CharField(verbose_name="设备类型", max_length=100)
    devicestatus = models.CharField(verbose_name="设备状态", max_length=100)
    devicetime = models.CharField(verbose_name="设备时间", max_length=100)
    deviceaddress = models.CharField(verbose_name="所在位置", max_length=100)
# 活动项目
class Cxlist(models.Model):
    name = models.CharField(verbose_name="用户", max_length=100)
    cxname = models.CharField(verbose_name="活动名称", max_length=100)
    cxstarttime = models.CharField(verbose_name="参加时间", max_length=100)
    status = models.CharField(verbose_name="活动状态", max_length=100)
#商品信息
class Goods(models.Model):
    name = models.CharField(verbose_name="商品名称", max_length=100)
    price = models.CharField(verbose_name="商品价格", max_length=100)
    goodstype = models.CharField(verbose_name="商品类型", max_length=100)
    image= models.CharField(verbose_name="商品图片", max_length=100)
    goodsdesc = models.CharField(verbose_name="商品描述", max_length=1000)

