from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required
def analytics(request):
    return render(request, "main/analytics/analitics.html")
