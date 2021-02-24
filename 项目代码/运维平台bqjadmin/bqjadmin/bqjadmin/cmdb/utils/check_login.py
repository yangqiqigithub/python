# from django.shortcuts import redirect
# def check_login(func):
#     def wrapper(request, *args, **kwargs):
#         userinfo = request.session.get('user_info')
#         if not userinfo:
#             return redirect('/login/')
#         else:
#             res = func(request, *args, **kwargs)
#             return res
#     return wrapper
