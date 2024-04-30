from django.db import models
from django.forms.models import model_to_dict
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
    def __str__(self):
        return self.name

class Admin(models.Model):
    name = models.CharField(verbose_name="用户名", max_length=100)
    password = models.CharField(verbose_name="密码", max_length=100)
    email = models.CharField(verbose_name="邮箱", max_length=100)

# 公告
class Publicmsg(models.Model):
    sn = models.CharField(verbose_name="公告编号", max_length=100)
    title = models.CharField(verbose_name="公告标题", max_length=100)
    content = models.CharField(verbose_name="公告内容", max_length=100)
    status = models.CharField(verbose_name="公告状态", max_length=100)
    expriy = models.IntegerField(verbose_name="公告过期时间", max_length=100)


#商品信息
class Goods(models.Model):
    name = models.CharField(verbose_name="商品名称", max_length=100)
    price = models.CharField(verbose_name="商品价格", max_length=100)
    category = models.ForeignKey(to="Category", to_field="id", on_delete=models.CASCADE,verbose_name="商品分类",default=1)
    image= models.CharField(verbose_name="商品图片", max_length=100)
    goodsdesc = models.CharField(verbose_name="商品描述", max_length=1000)

    def toJSON(self):
        field_dict = model_to_dict(self)  # 使用from django.forms.models import model_to_dict
        return json.dumps(field_dict, ensure_ascii=False)

#敏感词
class Sensitive(models.Model):
    word = models.CharField(verbose_name="敏感词", max_length=300)
#订单表
class Orders(models.Model):
    orderid = models.CharField(verbose_name="订单编号", max_length=100)
    userid = models.CharField(verbose_name="用户编号", max_length=100)
    goodsid = models.CharField(verbose_name="商品编号", max_length=100)
    goodsname = models.CharField(verbose_name="商品名称", max_length=100)
    goodsnum = models.CharField(verbose_name="商品数量", max_length=100)
    goodsprice = models.CharField(verbose_name="商品价格", max_length=100)
    fee= models.CharField(verbose_name="运费", max_length=100)
    total= models.CharField(verbose_name="总价", max_length=100)
    ordertime = models.CharField(verbose_name="下单时间", max_length=100)
    orderstatus = models.CharField(verbose_name="订单状态", max_length=100)
    address = models.CharField(verbose_name="收货地址", max_length=100,default="")
    name = models.CharField(verbose_name="收货人", max_length=100,default="")
    phone = models.CharField(verbose_name="收货人电话", max_length=100,default="")
    remark = models.CharField(verbose_name="备注", max_length=1000,default="")

