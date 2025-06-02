from django.shortcuts import render,redirect
from landload.models import TenentProfileVerify,Property,Rooms
from landload.forms import TenantInviteReadOnlyForm
from users.models import CustomUser
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='/')
def index(request):
    return render(request,'tenant/index.html')


def tenantverify(request, id):
    if (TenentProfileVerify.objects.filter(link=id).exists()):
        obj = TenentProfileVerify.objects.get(link=id)
        property = Property.objects.filter(landload=obj.tenant.landload,is_active=True)
        room = Rooms.objects.filter(property=obj.tenant.property)
        form=TenantInviteReadOnlyForm(instance=obj.tenant)
        if request.method == "POST":
            post_data = request.POST.copy()
            post_data['is_active']=True
            form = TenantInviteReadOnlyForm(post_data, request.FILES, instance=obj.tenant)
            if form.is_valid():
                user = obj.tenant.user
                user.first_name = form.cleaned_data.get('first_name', user.first_name)
                user.middle_name = form.cleaned_data.get('middle_name', user.middle_name)
                user.last_name = form.cleaned_data.get('last_name', user.last_name)
                user.email = form.cleaned_data.get('email', user.email)
                user.phone_number = form.cleaned_data.get('phone_number', user.phone_number)
                password = request.POST.get('password1')
                con_pass = request.POST.get('password2')
                user.is_verify=True
                user.is_active=True
                print(password,con_pass)
                # print(obj.user)
                if password == con_pass:
                    user.set_password(password)
                else:
                    messages.error(request, 'Password not match')
                    return redirect('tenant:home')
                user.save()
                obj1=form.save(commit=False)
                obj1.user=user
                obj1.save()
                obj.verify = True
                obj.save()
                messages.success(request, f'Profile has been Created successfully!')
                return redirect('tenant:home')
            else:
                print(form.errors)
                messages.error(request, f'{form.errors}')

        return render(request,'tenant/tenant_profile.html',{'form':form,'property':property,'tenant_obj':obj.tenant,'room':room})
    else:
        messages.error(request, f'Invalid token')
        return redirect('tenant:home')