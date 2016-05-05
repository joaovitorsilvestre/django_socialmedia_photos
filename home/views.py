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

        try:                                            #precisa disso pq se for um AnonymousUser vai dar problema pois o mesmo não tem o campo solicitacao
            jsonDec = json.decoder.JSONDecoder()
            self.solicitacao = jsonDec.decode(request.user.solicitacao)
        except:
            self.solicitacao = []
            
#ESSA classe é utilizada para ser enviada para o html, desta forma garantindo que apenas os dados abaixo sairão do servidor para o cliente
class usuario_other_data(object):
    def __init__(self,usuario_encontrado):
        jsonDec = json.decoder.JSONDecoder()
        self.name = usuario_encontrado.name
        self.solicitacao = jsonDec.decode(usuario_encontrado.solicitacao)
        #self.solicitacao = json.loads(usuario_encontrado.solicitacao)

def Home(request):
    header = header_objeto(request)
    if header.active == True:
        return render(request, 'home/home.html', {'active':header.active, 'usuario':header.usuario, 'results': header.results})
    else:
        next = header.request.GET.get('next', '/home/')
        if request.method == 'POST':
            username = header.request.POST['username']
            password = header.request.POST['password']

            user = authenticate(username=username, password=password) # ele tenta autenticar o usuario, se não conseguir ele retorna None

            if user is not None:   # se o user NÃO retornar None então ele executa
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(next)
                else:
                    return HttpResponse('Inactive user')
            else:
                return render(request, 'home/home.html', {'fail':True, 'active':False, 'usuario': header.usuario, 'results': header.results})


    return render(request, 'home/home.html', {'active':header.active, 'usuario': header.usuario, 'results': header.results,
                                                'solicitacao': header.solicitacao, 'num_solicitacao': len(header.solicitacao)})

def Upload_image(request):
    usuario = request.user

    if request.method == 'POST':
        public_or_private = request.POST['public_or_private']
        try:
            imagens = request.FILES.getlist('imagens')
        except:
            imagens = None

        if imagens != None:
            if public_or_private == 'public':
                for item in imagens:
                    usuario.images_public = item
                    usuario.save()
                return HttpResponse('imagens upadas com sucesso')
            elif public_or_private == 'private':
                return HttpResponse('imagens privadas')
            else:
                return HttpResponse('Algo de errado...')

    return render(request, 'home/upload_image.html')

def Usuario_page(request, usuario_other):
    jsonDec = json.decoder.JSONDecoder()
    usuario = request.user

    header = header_objeto(request)
    header.logica_login()

    for u in Usuario.objects.all():             ## para cada usuario registrado ele vai procurar
        if u.name == usuario_other:          ## pelo que contem o mesmo username que o informado
            usuario_encontrado = u
            usuario_other = usuario_other_data(usuario_encontrado)  # essa variavel guarda o objeto usuario achado, por ex se seu procure por joao vaiter tudo sobre ele, pass, username etc
            achado = True
            break

    if request.method == 'POST':
        add_friend = request.POST['add_friend']

        get_user_enc_solic = jsonDec.decode(usuario_encontrado.solicitacao) # pega a lista do field do usuario encontrado, e transforma de json para a lista
        get_user_enc_solic.append(usuario.username)
        usuario_encontrado.solicitacao = json.dumps(get_user_enc_solic) ## da append do username do usuario que fez a solicitação a lista carregada

        usuario_encontrado.save()

        return HttpResponse('Solicitação enviada para o/a ' + usuario_encontrado.name + '...confirmação: ' + usuario_encontrado.solicitacao)


    return render(request, 'home/usuario_other_page.html', {'active':header.active, 'usuario': header.usuario, 'results': header.results, 'usuario_other':usuario_other,
                                                            'solicitacao': header.solicitacao, 'num_solicitacao': len(header.solicitacao)})
