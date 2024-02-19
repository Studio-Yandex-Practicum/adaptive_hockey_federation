from core.constants import STAFF_POSITION_CHOICES
from django.contrib.auth.decorators import login_required

from django.shortcuts import render

from adaptive_hockey_federation.core.utils import generate_file_name


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
