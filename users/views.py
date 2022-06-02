from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views.generic.base import View

from .forms import RegistrationForm, ChangePasswordForm, ProfileForm


class MyRegistrationView(View):
    def get(self, request):
        return render(request, 'users/registration.html', context={'form': RegistrationForm})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/login/')
        return render(request, 'users/registration.html', context={'form': form})


class MyLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'users/login.html'


@method_decorator(login_required, name='get')
class ProfileView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/'

    def get(self, request):
        return render(request, 'users/profile.html', context={'form': ProfileForm(instance=request.user)})

    def post(self, request, *args, **kwargs):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            user.first_name = form.cleaned_data['first_name']
            user.last_name = form.cleaned_data['last_name']
            user.email = form.cleaned_data['email']
            user.save()
            messages.info(request, 'Профиль обновлен')
        return render(request, 'users/profile.html', context={'form': form})


@method_decorator(login_required, name='get')
class ChangePasswordView(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = '/'

    def get(self, request):
        return render(request, 'users/change_password.html', context={'form': ChangePasswordForm})

    def post(self, request, *args, **kwargs):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = User.objects.get(username=request.user.username)
            password_now = form.cleaned_data['password_now']
            if user.check_password(password_now):
                password_new = form.cleaned_data['password_new']
                user.set_password(password_new)
                user.save()
                messages.info(request, 'Пароль успешно обновлен')
                return redirect('/login/')
            form.add_error('password_now', 'Неверный пароль!')
        return render(request, 'users/change_password.html', context={'form': form})
