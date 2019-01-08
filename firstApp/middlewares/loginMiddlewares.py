from django.core.cache import cache
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.deprecation import MiddlewareMixin
# 修改
from firstApp.models import User


class LoginMiddlewares(MiddlewareMixin):
    def process_request(self, request):
        if request.path in [reverse('firstApp:square1'), reverse('firstApp:match1'),
                            reverse('firstApp:mine1')]:
            # 验证是否登录
            user_id = request.session.get("name")
            if not user_id:
                return redirect(reverse('firstApp:login1'))

            token = cache.get(user_id)
            if not token:
                # 去mysql中找
                try:
                    user = User.objects.get(pk=user_id)
                    token = user.token
                    # 同步
                    cache.set(user_id, token)
                except Exception as e:
                    return redirect(reverse('firstApp:login1'))

            # tokenValue = request.COOKIES.get("token")
            # if tokenValue != token:
            #     return redirect(reverse('firstApp:login1'))
