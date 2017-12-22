from django.contrib.auth.decorators import login_required
from django.views.generic import View

# class LoginVerify(View):
#     @classmethod
#     def as_view(cls, **initkwargs):
#         # 调用父类的方法
#         view = super(LoginVerify,cls).as_view(**initkwargs)
#         return login_required(view)

class LoginVerify(object):
    @classmethod
    def as_view(cls, **initkwargs):
        # 调用父类的方法
        view = super(LoginVerify, cls).as_view(**initkwargs)
        return login_required(view)