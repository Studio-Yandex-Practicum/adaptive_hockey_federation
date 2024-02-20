from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def main(request):
    return render(request, "main/home/main.html")


@login_required
def competitions_id(request, id):
    return render(request, "main/competitions_id/competitions_id.html")


@login_required
def analytics(request):
    return render(request, "main/analytics/analitics.html")


@login_required
def unloads(request):
    return render(request, "main/unloads/unloads.html")
