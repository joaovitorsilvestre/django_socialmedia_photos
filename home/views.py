from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from django_socialmedia_photos import settings
from accounts.models import Usuario
import json
import os

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

        try:           #precisa disso pq se for um AnonymousUser vai dar problema pois o mesmo não tem o campo solicitacao
            jsonDec = json.decoder.JSONDecoder()
            self.solicitacao = jsonDec.decode(self.usuario.solicitacao)
            self.friends = jsonDec.decode(self.usuario.friends)
        except:
            self.solicitacao = []
            self.friends = []

    # esse metodo vai adicionar o amigo no field e vice versa para os dois passarem a ter o outro no field
    def add_friend(self,add_friend_val):
        jsonDec = json.decoder.JSONDecoder()
        for u in Usuario.objects.all():              ## tenho q fazer isso para transformar a variavel com a string de username
            if u.username == add_friend_val:         ## se tornar uma variavel com o objeto correspondente ao usuario
                add_friend_val = u                   # para isso verifico se add_friend_val consta no field username de algum usuario

        ## fazendo para o usuario logado
        lista_friends = jsonDec.decode(self.usuario.friends)  ## le a lista
        lista_friends.append(add_friend_val.username)
        self.usuario.friends = json.dumps(lista_friends)      #

        ## remove da solicitacao de amizade o amigo adicionado
        try:
            lista_solicitacao = self.solicitacao
            lista_solicitacao.remove(add_friend_val.username)
            self.usuario.solicitacao = json.dumps(lista_solicitacao)
        except:
            pass

        ## fazendo para ou outro usuario, o que acabou de ser aceito a solicitação
        lista_friends = jsonDec.decode(add_friend_val.friends)
        lista_friends.append(self.usuario.username)
        add_friend_val.friends = json.dumps(lista_friends)

        self.usuario.save()
        add_friend_val.save()

    def get_images(self):
        images_user = []
        for root, dirs, files in os.walk("./media/image_profile_users/{}/images_public".format(self.usuario.username, topdown=False)):
            for name in files:
                images_user.append(name)

        return images_user

#ESSA classe é utilizada para ser enviada para o html, desta forma garantindo que apenas os dados abaixo sairão do servidor para o cliente
class usuario_other_data(object):
    def __init__(self,usuario_encontrado):
        jsonDec = json.decoder.JSONDecoder()
        self.name = usuario_encontrado.name
        self.username = usuario_encontrado.username
        self.solicitacao = jsonDec.decode(usuario_encontrado.solicitacao)
        #self.solicitacao = json.loads(usuario_encontrado.solicitacao)

def Home(request):
    header = header_objeto(request)

    dic_to_html =  {'active':header.active, 'usuario': header.usuario, 'results': header.results,
                    'solicitacao': header.solicitacao, 'num_solicitacao': len(header.solicitacao),
                    'friends': header.friends}
    ## tem que fazer isso para que se caso for um usuario anonimo não dar problema
    dic_to_html['images_user'] = header.get_images()  ##adiciona um item ao dicionario, as imagens encontradas no metodo do header

    #### SE O USUARIO ESTA LOGAOD
    if header.active == True:

        ### parte do form de aceitar solicitação de amigo
        if request.method == 'POST' and 'add_friend_val' in request.POST:
            add_friend_val = request.POST['add_friend_val']
            header.add_friend(add_friend_val)
            return render(request, 'home/home.html', dic_to_html)
        ###

        return render(request, 'home/home.html', dic_to_html)
    ## SE O USUARIO ESTÁ OFF
    else:
        next = header.request.GET.get('next', '/home/')
        if request.method == 'POST' and 'username' in request.POST:
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
                return render(request, 'home/home.html', dic_to_html)

    return render(request, 'home/home.html', dic_to_html)

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

    for u in Usuario.objects.all():             ## para cada usuario registrado ele vai procurar
        if u.name == usuario_other:          ## pelo que contem o mesmo username que o informado
            usuario_encontrado = u
            usuario_other = usuario_other_data(usuario_encontrado)  # essa variavel guarda o objeto usuario achado, por ex se seu procure por joao vaiter tudo sobre ele, pass, username etc
            achado = True
            break

    dic_to_html =  {'active':header.active, 'usuario': header.usuario, 'results': header.results,
                    'solicitacao': header.solicitacao, 'num_solicitacao': len(header.solicitacao),
                    'usuario_other':usuario_other,
                    'friends': header.friends}

    if header.active == True:
        if request.method == 'POST' and 'add_friend_val' in request.POST:
            add_friend_val = request.POST['add_friend_val']
            header.add_friend(add_friend_val)

            return render(request, 'home/usuario_other_page.html', dic_to_html)

        if request.method == 'POST' and 'solicitar_friend' in request.POST:
            solicitar_friend = request.POST['solicitar_friend']

            get_user_enc_solic = jsonDec.decode(usuario_encontrado.solicitacao) # pega a lista do field do usuario encontrado, e transforma de json para a lista
            get_user_enc_solic.append(usuario.username)
            usuario_encontrado.solicitacao = json.dumps(get_user_enc_solic) ## da append do username do usuario que fez a solicitação a lista carregada

            usuario_encontrado.save()

            return HttpResponse('Solicitação enviada para o/a ' + usuario_encontrado.name + '...confirmação: ' + usuario_encontrado.solicitacao)


        return render(request, 'home/usuario_other_page.html', dic_to_html)

    else:
        next = header.request.GET.get('next', '/home/')
        if request.method == 'POST' and 'username' in request.POST:
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
                return render(request, 'home/usuario_other_page.html', dic_to_html)

    return render(request, 'home/usuario_other_page.html', dic_to_html)
