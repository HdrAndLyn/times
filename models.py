from django.db import models


# Create your models here.
class User(models.Model):
    # 用户id，性别，个性签名，密码
    user_id = models.CharField(primary_key=True,max_length=11)
    sex = models.BooleanField(default=True)
    sign = models.CharField(max_length=30)
    pwd = models.CharField(max_length=30)
    token = models.CharField(max_length=40, null=True)
    img = models.CharField(max_length=400, null=True)

    class Meta:
        db_table = 'users'

    @classmethod
    def create(cls, user_id, sex, sign, pwd):
        return cls(user_id=user_id, sex=sex, sign=sign, pwd=pwd)


class Circle(models.Model):
    # 主题，用户id，circles（1-n外键连接）
    title = models.CharField(max_length=30)
    circles = models.CharField(max_length=250)  # HTMLField()
    user = models.ForeignKey('User')

    class Meta:
        db_table = 'circles'

    @classmethod
    def create(cls, title, circles, user):
        return cls(title=title, circles=circles, user=user)
