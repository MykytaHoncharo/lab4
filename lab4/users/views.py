from django.utils import timezone

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect

from .models import CustomUser as User, LoginLog
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.urls.base import reverse
from .forms import CustomUserCreationForm, CustomAuthenticationForm


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/signup.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                login_log = LoginLog(user=user, role=user.role)
                login_log.save()
                return redirect(reverse('home'))
    else:
        form = CustomAuthenticationForm(request=request)
    return render(request, 'users/login.html', {'form': form})



def logout_view(request):
    if request.method == 'POST':
        login_logs = LoginLog.objects.filter(user=request.user, logout_time__isnull=True)
        for login_log in login_logs:
            login_log.logout_time = timezone.now()
            login_log.save()
        logout(request)
    return redirect('login')


@login_required
def admin_panel(request):
    if request.user.is_admin():
        users = User.objects.exclude(role="admin")
        context = {'users': users}
        return render(request, 'users/admin_panel.html', context)
    else:
        return redirect('home')

@login_required
def change_role(request, user_id):
    if request.user.is_admin():
        user = User.objects.get(id=user_id)
        if request.method == 'POST':
            new_role = request.POST.get('new_role')
            user.role = new_role
            user.save()
            return HttpResponseRedirect(reverse('admin'))
        else:
            return render(request, 'users/change_role.html', {'user': user})
    else:
        return redirect('home')
