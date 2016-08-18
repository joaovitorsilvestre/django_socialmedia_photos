from django.shortcuts import render
from django.http import JsonResponse, HttpResponse,HttpResponseRedirect

from accounts.manager import AccountsManager
from accounts.models import Usuario, RequestsFriends

def Search(request, searchString):
    users = []
    if len(searchString) > 0:
        for user in Usuario.objects.all():
            if not user.username == request.user.username:
                if searchString in user.username:
                    users.append(user.username)

    response = {
        'users': users
    }
    return JsonResponse(response)

def SendFiles(request):
    images = request.FILES.getlist('images')
    print(images)
    manager = AccountsManager(request)

    try:
        manager.saveFiles(images)
    except Exception as error:
        return HttpResponse(error,status=500)
    else:
        return HttpResponseRedirect('/home/#/own/')

def IsFriend(request, user):
    user = Usuario.objects.get(username=user)

    if user in request.user.friends.all():
        return JsonResponse({'isFriend':True})
    else:
        return JsonResponse({'isFriend':False})

def RequestFriend(request, user):
    user = Usuario.objects.get(username=user)
    if not user.request_friends.filter(user_that_request=request.user.username):
        user.request_friends.create(user_that_request=request.user.username)
        return HttpResponse(status=200)
    else:
        return HttpResponse(status=203)

def RequestToMe(request):
    response = {'requestToMe':[]}
    for item in request.user.request_friends.all():
        response['requestToMe'].append(item.user_that_request)

    return JsonResponse(response)

def AcceptRequest(request, user):
    request.user.request_friends.get(user_that_request=user).delete()

    user = Usuario.objects.get(username=user)

    request.user.friends.add(user)

    return HttpResponseRedirect('/home')

def GetSelfImages(request):
    response = {
        'images_links': request.user.get_images(),
        'path': '/media/users/{}'.format(request.user.username)
    }

    return JsonResponse(response)

def GetFriends(request):
    friends = []
    for friend in request.user.friends.all():
        friends.append(friend.username)

    response = {'friends': friends}
    return JsonResponse(response)
