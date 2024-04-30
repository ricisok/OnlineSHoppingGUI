from django.db import models


class machine(models.Model):
    class Mete:
        db_table = 'system_machine'  # 指明数据库表名 默认 appname_modelname

    machine = models.CharField(verbose_name="机器名", max_length=100, default="")
    area = models.CharField(verbose_name="区域", max_length=100, default="")


class data(models.Model):
    class Mete:
        db_table = "system_data"

    machine = models.CharField(verbose_name="机器号", max_length=100, default="")
    brand=models.CharField(verbose_name="牌号", max_length=100, default="")
    output=models.IntegerField(verbose_name="产量", max_length=100, default=0)
    speed=models.IntegerField(verbose_name="速度", max_length=100, default=0)
    reject_count=models.IntegerField(verbose_name="剔除量", max_length=100, default=0)
    reject_rate=models.FloatField(verbose_name="剔除率", max_length=100, default=0)
    work_status=models.CharField(verbose_name="工作状态", max_length=100, default="")
    reject_status=models.CharField(verbose_name="剔除状态", max_length=100, default="")
    system_status=models.CharField(verbose_name="系统状态", max_length=100, default="")



class   alarm(models.Model):
    class Mete:
        db_table = "system_alarm"

    machine = models.CharField(verbose_name="机器号", max_length=100, default="")
    time=models.DateTimeField(verbose_name="时间", max_length=100, default="")
    alarm=models.CharField(verbose_name="报警", max_length=500, default=0)


class reject_module1(models.Model):
    machine_id = models.CharField(verbose_name="机器号", max_length=100, default="")
    reject=models.CharField(verbose_name="定位", max_length=100, default="")
    count=models.IntegerField(verbose_name="统计数", max_length=100, default=0)
class reject_module2(models.Model):
    machine_id = models.CharField(verbose_name="机器号", max_length=100, default="")
    reject=models.CharField(verbose_name="定位", max_length=100, default="")
    count=models.IntegerField(verbose_name="统计数", max_length=100, default=0)