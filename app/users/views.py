from django.contrib import messages
from django.contrib.auth import get_user_model,login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetView
from django.http import HttpRequest,HttpResponse
from django.shortcuts import get_object_or_404,redirect,render
from django.urls import reverse_lazy
from .forms import LoginForm,ProfileDetailForm,RegistrationForm,UserProfileForm
from .models import Profile
User=get_user_model()
def register_view(request:HttpRequest)->HttpResponse:
    if request.user.is_authenticated: return redirect("posts:feed")
    if request.method=="POST":
        form=RegistrationForm(request.POST)
        if form.is_valid():
            user=form.save();Profile.objects.get_or_create(user=user);login(request,user)
            messages.success(request,"Добро пожаловать!");return redirect("posts:feed")
    else: form=RegistrationForm()
    return render(request,"users/register.html",{"form":form})
class UserLoginView(LoginView):
    form_class=LoginForm;template_name="users/login.html";redirect_authenticated_user=True
class UserLogoutView(LogoutView):
    next_page="/users/login/"
class UserPasswordResetView(PasswordResetView):
    template_name="users/password_reset.html";success_url=reverse_lazy("users:login")
@login_required
def profile_view(request:HttpRequest,user_id:int)->HttpResponse:
    u=get_object_or_404(User,pk=user_id);p,_=Profile.objects.get_or_create(user=u)
    return render(request,"users/profile.html",{"profile_user":u,"profile":p,"is_own":request.user.pk==u.pk})
@login_required
def profile_edit_view(request:HttpRequest)->HttpResponse:
    p,_=Profile.objects.get_or_create(user=request.user)
    if request.method=="POST":
        uf=UserProfileForm(request.POST,request.FILES,instance=request.user);pf=ProfileDetailForm(request.POST,instance=p)
        if uf.is_valid() and pf.is_valid(): uf.save();pf.save();return redirect("users:profile",user_id=request.user.pk)
    else: uf=UserProfileForm(instance=request.user);pf=ProfileDetailForm(instance=p)
    return render(request,"users/profile_edit.html",{"user_form":uf,"profile_form":pf})
