from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django_socialmedia_photos import settings
from accounts.models import Usuario
import json

def Home(request):
    active = request.user.is_authenticated()

    usuario = request.user

    todos_usuarios = []
    for u in Usuario.objects.all().values_list('username', flat=True):
        todos_usuarios.append(u)

    results = json.dumps(todos_usuarios)


    if active == True:
        return render(request, 'home/home.html', {'active':True, 'usuario':usuario, 'results': results})
    else:
        next = request.GET.get('next', '/home/')
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']

            user = authenticate(username=username, password=password) # ele tenta autenticar o usuario, se não conseguir ele retorna None

            if user is not None:   # se o user NÃO retornar None então ele executa
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponse('Inactive user')
            else:
                return render(request, 'home/home.html', {'fail':True, 'active':False, 'usuario':usuario, 'results': results})

    return render(request, 'home/home.html', {'active':active, 'usuario': usuario, 'results': results})


def Usuario_page(request, usuario_page):
    return HttpResponse('Esta é a pagina do(a) '+ usuario_page)
