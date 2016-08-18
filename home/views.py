from django.shortcuts import render
from django.http import HttpResponse

def Index(request):
    contex = {
        'title':'Pagina Inicial',
        'user': request.user.username
    }

    return render(request, 'home/index.html', contex)

def OwnPage(request):
    return render(request, 'home/ownPage.html')

def UserPage(request):
    return render(request, 'home/userPage.html')

def DefaultPage(request):
	return render(request, 'home/defaultPage.html')