from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import CreationForm
from .models import User


class SingUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy('main:main')
    template_name = 'users/signup.html'


def profile(request, username):
    user = get_object_or_404(User, username=username)
    context = {
        'user': user
    }
    return render(request, 'users/profile_site.html', context)
