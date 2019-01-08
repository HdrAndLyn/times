from django.core.cache import cache
from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

from firstApp.models import User


class LoginMiddlewares(MiddlewareMixin):
    def process_request(self, request):
        if request.path in ["/cart/", "/mine/"]:
            # 验证是否登录
            phone = request.session.get("phone")
            if not phone:
                return redirect("/login/")

            token = cache.get(phone)
            if not token:
                #去mysql中找
                try:
                    user = User.objects.get(pk=phone)
                    token = user.token
                    #同步
                    cache.set(phone, token)
                except User.DoesNotExist as e:
                    return redirect("/login/")

            tokenValue = request.COOKIES.get("token")
            if tokenValue != token:
                return redirect("/login/")