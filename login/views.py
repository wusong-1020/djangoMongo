from django.shortcuts import render
from django.shortcuts import redirect
from . import models
from . import forms
import hashlib

# Create your views here.

#加密
def hash_code(s, salt='mysite'):
    h = hashlib.sha256()
    s += salt
    h.update(s.encode())
    return h.hexdigest()

def index(request):
    pass
    return render(request,'login/index.html')

def login(request):
    # 不允许重复登录
    if request.session.get('is_login',None):
        return register('/index/')
    if request.POST:
        login_form=forms.UserForm(request.POST)
        message='请检查填写的内容！'
        #使用表单类自带的is_valid()方法一步完成数据验证工作；
        '''
        如果验证不通过，则返回一个包含先前数据的表单给前端页面，方便用户修改。
        也就是说，它会帮你保留先前填写的数据内容，而不是返回一个空表！
        '''
        if login_form.is_valid():
            #验证成功后可以从表单对象的cleaned_data数据字典中获取表单的具体值；
            username=login_form.cleaned_data.get('username')
            password=login_form.cleaned_data.get('password')
            try:
                user=models.User.objects.get(name=username)
            except:
                message='用户不存在！'
                '''
                Python内置了一个locals()函数，它返回当前所有的本地变量字典，
                我们可以偷懒的将这作为render函数的数据字典参数值，
                就不用费劲去构造一个形如{'message':message, 'login_form':login_form}的字典了。
                '''
                return render(request,'login/login.html',locals())

            if user.password==hash_code(password):
                #往session字典内写入用户状态和数据
                request.session['is_login']=True
                request.session['user_id']=str(user.id)
                request.session['user_name']=user.name
                return redirect('/index/')
            else:
                message='密码不正确！'
                return render(request,'login/login.html',locals())
        else:
            return render(request,'login/login.html',locals())
    login_form=forms.UserForm()
    return render(request,'login/login.html',locals())

def register(request):
    if request.session.get('is_login',None):
        return register('/index/')
    if request.POST:
        register_form=forms.RegisterForm(request.POST)
        message='请检查填写的内容'
        if register_form.is_valid():
            username=register_form.cleaned_data.get('username')
            password1=register_form.cleaned_data.get('password1')
            password2=register_form.cleaned_data.get('password2')
            email=register_form.cleaned_data.get('email')
            sex=register_form.cleaned_data.get('sex')
            if password1 != password2:
                message='两次密码不一致'
                return render(request,'login/register.html',locals())
            else:
                same_user_name=models.User.objects.filter(name=username)
                if same_user_name:
                    message='用户名已存在'
                    return render(request, 'login/register.html', locals())
                same_email_user=models.User.objects.filter(email=email)
                if same_email_user:
                    message='该邮箱已经被注册了'
                    return render(request, 'login/register.html', locals())
                new_user=models.User()
                new_user.name=username
                new_user.password=hash_code(password1)
                new_user.email=email
                new_user.sex=sex
                new_user.save()
                return redirect('/login/')
        else:
            return render(request,'login/register.html',locals())
    register_form=forms.RegisterForm()
    return render(request,'login/register.html',locals())

def logout(request):
    if not request.session.get('is_login',None):
        return register('/login/')
    '''
    flush()方法是比较安全的一种做法，而且一次性将session中的所有内容全部清空，确保不留后患。
    但也有不好的地方，那就是如果你在session中夹带了一点‘私货’，会被一并删除，这一点一定要注意。
    '''
    request.session.flush()
    return render(request,'login/login.html')

