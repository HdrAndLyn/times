import random
import uuid
from django.core.cache import cache
from django.http import HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.urls import reverse
from firstApp.models import User
from firstApp.models import Circle

# from django.contrib.auth import logout

# Create your views here.
# 用户总列表
users_all = []


# 引导
def index(request):
    if request.method == 'GET':
        return render(request, 'firstApp/index.html')


# 注册
def register(request):
    if request.method == 'GET':
        return render(request, 'firstApp/register.html')
    elif request.method == "POST":
        user_id = request.POST.get("account")  # 获取表单提交数据
        u = None  # 接受数据库搜索结果
        try:
            # 验证账号是否存在
            u = User.objects.get(pk=user_id)  # 从数据库搜索该注册账号
        except Exception as e:
            pwd = request.POST.get("pwd")
            pwd2 = request.POST.get("pwd2")
            # 验证密码是否一致
            if pwd != pwd2:
                return redirect(reverse('firstApp:register1'))
            sign = request.POST.get("sign")
            sex = request.POST.get("sex")
            u = User.create(user_id, sex, sign, pwd)
            # token
            token = str(uuid.uuid4())
            u.token = token
            u.save()
            # 上传头像

            # 并保存至用户总列表
            users_all.append(u)

            # 同步到redis/将token写入cookie
            cache.set(user_id, token)
            # response.set_cookie("token", token)
            # 状态保持
            request.session['name'] = user_id
            request.session['sign'] = sign
            # 邮件验证
        else:
            return redirect(reverse('firstApp:login1'))


# 登录
def login(request):
    if request.method == 'GET':

        name = request.session.get('name')

        data = {
            "name": name or 'visitor',
        }
        return render(request, 'firstApp/login.html', data)
    elif request.method == 'POST':
        # 从表单获取
        user_id = request.POST.get("uid")
        pwd = request.POST.get("pwd")
        # 检索数据库
        try:
            u = User.objects.get(pk=user_id)
        except Exception as e:
            return redirect(reverse('firstApp:register1'))
        else:
            if u.user_id == user_id and u.pwd == pwd:
                request.session['name'] = u.user_id
                return redirect(reverse('firstApp:match1'))


# 我的主页
def mine(request):
    if request.method == 'GET':
        data = {
            "sign": request.session.get("sign", "赶快登陆写点什么吧~")
        }
        return render(request, 'firstApp/mine.html', data)


# 匹配用户
def match(request):
    if request.method == 'GET':
        return render(request, 'firstApp/match.html')
    else:
        unum = random.randrange(0, len(users_all) - 1)  # 随机获取用户列表下标匹配
        u = users_all[unum]  # 获取该用户对象储存地址(用二分查找法代替)
        users = Circle.objects.get(pk=(u.user_id))  # 1-n主查从
        cle = users.circle_set.all
        data = {
            "name": u.user_id,
            "sex": u.sex,
            "sign": u.sign,
            "cle": cle,
        }
        return render(request, 'firstApp/match.html', data)


# 广场
def square(request):
    if request.method == 'GET':
        return render(request, 'firstApp/match.html')


# 验证码
def verifycode(request):
    # 引入绘图模块
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(
        20, 100), random.randrange(20, 100))
    width = 70
    height = 30
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str = '1234567890QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str[random.randrange(0, len(str))]
    # 构造字体对象
    font = ImageFont.truetype(r'/home/hdr/times/fonts/ADOBEARABIC-BOLDITALIC.OTF', 28)
    # 构造字体颜色
    fontcolor1 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor2 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor3 = (255, random.randrange(0, 255), random.randrange(0, 255))
    fontcolor4 = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字
    draw.text((5, 0), rand_str[0], font=font, fill=fontcolor1)
    draw.text((20, 0), rand_str[1], font=font, fill=fontcolor2)
    draw.text((35, 0), rand_str[2], font=font, fill=fontcolor3)
    draw.text((50, 0), rand_str[3], font=font, fill=fontcolor4)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    # request.session['verifycode'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
