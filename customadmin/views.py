from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
# Create your views here.
def index(request):
    return render(request,'customadmin/index.html')

