from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse_lazy

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .forms import CustomUserCreationForm
from users.models import CustomUser
from users.email import verification_mail
from django.contrib.sites.shortcuts import get_current_site

# Create your views here.
def index(request):
    return render(request,'customadmin/index.html')

def landload(request):
    landload = CustomUser.objects.filter(is_active=True,status='landload') 
    return render(request,'customadmin/landload.html',{'landload':landload})

def add_landload(request):
    token=''
    form=CustomUserCreationForm()
    if request.method=="POST":
        post_data = request.POST.copy()
        post_data['password1'] = "Root@123"
        post_data['password2'] = "Root@123"
        form=CustomUserCreationForm(post_data)
        email=request.POST.get('email')

        if form.is_valid():
            # signup_as = form.cleaned_data['role']
            preobj=form.save(commit=False)
            preobj.is_active=True
            preobj.status='landload'
            preobj.save()
            email1 = CustomUser.objects.get(email=email)
           
            messages.success(request,'Invite has benn send.')

            token = 'http://'+str(get_current_site(request).domain)+'/user/userverify/' + token
            # verification_mail(token, email)
            msg = 'The activation link has been send to your Email.'
            return redirect('customadmin:landload')
        else:
            messages.error(request,form.errors)
    return render(request,'customadmin/add_landload.html',{'form':form})

def delete_landload(request,id):
    leave_type = get_object_or_404(CustomUser, id=id)
    leave_type.is_active = False
    leave_type.save()
    messages.success(request, f'Landload has been deleted successfully!')
    return redirect('customadmin:landload')
