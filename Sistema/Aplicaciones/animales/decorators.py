from django.shortcuts import redirect
from django.contrib import messages

def solo_admin(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.rol != 'administrador':
            messages.error(request, 'No tienes permisos para esta acción')
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return wrapper


def solo_lectura(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return redirect('login')

        if request.user.rol not in ['administrador', 'encargado', 'revisor']:
            messages.error(request, 'No tienes permisos para esta acción')
            return redirect('home')

        return view_func(request, *args, **kwargs)
    return wrapper
