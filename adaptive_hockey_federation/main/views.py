from django.shortcuts import render


def users(request):
    return render(request, 'main/users.html')


def teams_id(request, id):
    return render(request, 'main/teams_id.html')


def teams(request):
    return render(request, 'main/teams.html')


def competitions_id(request, id):
    return render(request, 'main/competitions_id.html')


def competitions(request):
    return render(request, 'main/competitions.html')


def analytics(request):
    return render(request, 'main/analitics.html')


def unloads(request):
    return render(request, 'main/unloads.html')
