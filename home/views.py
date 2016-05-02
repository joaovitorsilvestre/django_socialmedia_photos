from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django_socialmedia_photos import settings
from accounts.models import Usuario
import json


#ESSA class É DA FUNCIONALIDADE DA HEADER
class header_objeto(object):
    def __init__(self,request):
        self.request = request
        self.active = request.user.is_authenticated()
        self.usuario = request.user
        self.todos_usuarios = []
        self.todos_usuarios = []
        for u in Usuario.objects.all().values_list('name', flat=True):
            self.todos_usuarios.append(u)

        self.results = json.dumps(self.todos_usuarios)

    def logica_login(self):
        if self.active == True:
            return render(self.request, 'home/home.html', {'active':True, 'usuario':self.usuario, 'results': self.results})
        else:
            next = self.request.GET.get('next', '/home/')
            if self.request.method == 'POST':
                username = self.request.POST['username']
                password = self.request.POST['password']

                user = authenticate(username=username, password=password) # ele tenta autenticar o usuario, se não conseguir ele retorna None

                if user is not None:   # se o user NÃO retornar None então ele executa
                    if user.is_active:
                        login(self.request, user)
                        return HttpResponseRedirect(next)
                    else:
                        return HttpResponse('Inactive user')
                else:
                    return render(self.request, 'home/home.html', {'fail':True, 'active':False, 'usuario': self.usuario, 'results': self.results})

class usuario_other_data(object):
    def __init__(self,usuario_encontrado):
        self.name = usuario_encontrado.name

def Home(request):
    header = header_objeto(request)
    header.logica_login()                  ## esse metodo faz toda a verificação se o usuario está logado, ou não etc

    return render(request, 'home/home.html', {'active':header.active, 'usuario': header.usuario, 'results': header.results})


def Usuario_page(request, usuario_other):
    header = header_objeto(request)
    header.logica_login()

    for u in Usuario.objects.all():             ## para cada usuario registrado ele vai procurar
        if u.name == usuario_other:          ## pelo que contem o mesmo username que o informado
            usuario_encontrado = u
            usuario_other = usuario_other_data(usuario_encontrado)  # essa variavel guarda o objeto usuario achado, por ex se seu procure por joao vaiter tudo sobre ele, pass, username etc
            achado = True
            break

    return render(request, 'home/usuario_other_page.html', {'active':header.active, 'usuario': header.usuario, 'results': header.results,
                                                            'usuario_other':usuario_other})
