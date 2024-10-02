from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def main(request):
    return render(request, "main/home/main.html")
