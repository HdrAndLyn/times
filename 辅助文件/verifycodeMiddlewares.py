from django.shortcuts import redirect
from django.utils.deprecation import MiddlewareMixin

class VerifycodeMiddlewares(MiddlewareMixin):
    def process_request(self, request):
        if request.path in ["/login/"] and request.method == "POST":
            code1 = request.POST.get("code")
            code2 = request.session.get("verifycode")
            if code1 != code2:
                return redirect("/login/")
