from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from .forms import StudentLoginForm

from django.contrib.auth.decorators import login_required
from . import models
from django.contrib import messages

# Create your views here.

@login_required
def dashboard(request):
    # Retrieve the user profile information
    user_profile = models.Student.objects.get(user=request.user)

    context = {
        'user_profile': user_profile,
    }

    return render(request, 'results/dashboard.html', context)




