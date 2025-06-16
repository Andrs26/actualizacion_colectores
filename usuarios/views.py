from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.groups.filter(name='colector').exists():
                return redirect('asignacion_usuario')
            elif user.is_superuser or user.groups.filter(name='admin').exists():
                return redirect('dashboard_home')
            else:
                return redirect('dashboard_home')  # valor por defecto
        else:
            messages.error(request, 'Credenciales inválidas.')
    return render(request, 'auth/login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')
