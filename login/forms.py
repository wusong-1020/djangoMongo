#顶部要先导入forms模块
from django import forms
from captcha.fields import CaptchaField

#所有的表单类都要继承forms.Form类
class UserForm(forms.Form):
    '''
    每个表单字段都有自己的字段类型比如CharField，它们分别对应一种HTML语言中<form>内的一个input元素。
    这一点和Django模型系统的设计非常相似。
    label参数用于设置<label>标签
    widget=forms.PasswordInput用于指定该字段在form表单里表现为<input type='password' />，也就是密码输入框。
    '''
    username=forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': "Username",'autofocus': ''}))
    password=forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': "Password"}))
    captcha=CaptchaField(label='验证码')

class RegisterForm(forms.Form):
    gender=(
        ('male','男'),
        ('female','女'),
    )
    username=forms.CharField(label='用户名',max_length=128,widget=forms.TextInput(attrs={'class':'form-control'}))
    password1=forms.CharField(label='密码',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password2=forms.CharField(label='确认密码',max_length=256,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    email=forms.EmailField(label='邮箱地址',widget=forms.EmailInput(attrs={'class':'form-control'}))
    sex=forms.ChoiceField(label='性别',choices=gender)#sex是一个select下拉框；
    captcha=CaptchaField(label='验证码')