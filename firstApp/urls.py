from django.conf.urls import url

from firstApp import views

urlpatterns = [
    # 引导页
    url(r'^index/$', views.index, name='index1'),
    # 登录页
    url(r'^login/$', views.login, name='login1'),
    # 匹配页面
    url(r'^match/$', views.match, name='match1'),
    # 我的主页
    url(r'^mine/$', views.mine, name='mine1'),
    # 注册页
    url(r'^register/$', views.register, name='register1'),
    # 广场页面
    url(r'^square/$', views.square, name='square1'),
    #验证码
    url(r'^verifycode/$',views.verifycode, name='verifycode1')
]
