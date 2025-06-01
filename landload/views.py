from django.shortcuts import render,get_object_or_404,redirect
from .models import Property,Rooms,Tenant
from .forms import PropertyForm,PropertyReadOnlyForm,RoomsForm,TenantForm,TenantReadOnlyForm
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from users.models import CustomUser
# Create your views here.
def index(request):
    return render(request,'landload/index.html')


def listing(request):
    property = Property.objects.filter(landload=request.user,is_active=True)
    return render(request,'landload/listing.html',{'property':property})


def listing_add(request):
    form = PropertyForm()
    if request.method == "POST":
        post_data = request.POST.copy()
        print('post')
        print(request.POST)
        post_data['landload']=request.user
        post_data['is_active']=True
        form = PropertyForm(post_data,request.FILES)
        if form.is_valid():
            # form['landload']=request.user
       
            property_obj=form.save()
            for i in range(int(property_obj.rooms)):
                Rooms.objects.create(property=property_obj)
            messages.success(request, f'Property has been Created successfully!')
            return redirect('landload:listing')
        else:
            print('errr',form.errors)
            messages.error(request, f'{form.errors}')
    return render(request,'landload/add_listing.html',{'form':form})


def listing_view(request,id):
    property_obj = get_object_or_404(Property, pk=id)
    form = PropertyReadOnlyForm(instance=property_obj)
    return render(request,'landload/add_listing.html',{'form':form,'property_id':id,'property_obj':property_obj,'more_fun':True})


def listing_update(request,id):
    property_obj = get_object_or_404(Property, pk=id)
    old_number_of_room=property_obj.rooms
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['landload']=request.user
        post_data['is_active']=True
        form = PropertyForm(post_data, request.FILES, instance=property_obj)
        if form.is_valid():
            obj=form.save()
            if obj.rooms>old_number_of_room:
                num=int(obj.rooms)-int(old_number_of_room)
                for i in range(num):
                    Rooms.objects.create(property=property_obj)
            else:
                rooms_data = Rooms.objects.filter(property=property_obj).order_by('id')
                extra_rooms = rooms_data[int(obj.rooms):]  
                for room in extra_rooms:
                    room.delete()

            messages.success(request, f'Property has been updated successfully!')
            return redirect('landload:listing_view', id=id)
        else:
            print(form.errors)
    else:
        form = PropertyForm(instance=property_obj)
    return render(request,'landload/add_listing.html',{'form':form,'property_id':id,'property_obj':property_obj})

def room(request,id):
    # property_obj = get_object_or_404(Property, pk=id)
    # existing_rooms = Rooms.objects.filter(property=property_obj).order_by('id')

    # if request.method == 'POST':
    #     room_ids = request.POST.getlist('room_id')
    #     types = request.POST.getlist('type_of_room')
    #     ensuites = request.POST.getlist('ensuite')
    #     capacities = request.POST.getlist('total_capacity')
    #     rents = request.POST.getlist('rent')

    #     for room_id, type_, ensuite, capacity, rent in zip(room_ids, types, ensuites, capacities, rents):
    #         room = Rooms.objects.get(id=room_id)
    #         room.type_of_room = type_
    #         room.ensuite = ensuite
    #         room.total_capacity = capacity
    #         room.rent = rent
    #         room.save()

    #     return redirect('property_view', pk=id)


        
    # return render(request,'landload/room.html',{'property_id':id,'property_obj':range(property_obj.rooms),'property_obj_data': property_obj,})

    property_obj = get_object_or_404(Property, pk=id)
    existing_rooms = Rooms.objects.filter(property=property_obj).order_by('id')

    if request.method == 'POST':
        room_ids = request.POST.getlist('room_id')  
        types = request.POST.getlist('type_of_room')
        ensuites = request.POST.getlist('ensuite')
        capacities = request.POST.getlist('total_capacity')
        rents = request.POST.getlist('rent')
        for  room_ids,type_, ensuite, capacity, rent in zip(room_ids, types, ensuites, capacities, rents):
            if room_ids:  
                try:
                    room = Rooms.objects.get(id=room_ids, property=property_obj)
                except Rooms.DoesNotExist:
                    room = Rooms(property=property_obj)
            else:
                room = Rooms(property=property_obj)
            room.type_of_room = type_
            room.ensuite = ensuite
            room.total_capacity = capacity
            room.rent = float(rent)
            room.save()
        messages.success(request, f'Rooms has been updated successfully!')
        return redirect('landload:listing_view', id=id)

    context = {
        'property_obj': property_obj,
        'rooms': existing_rooms,
        # 'extra_rooms_needed': int(property_obj.rooms) - existing_rooms.count(),
        'room_range':range(int(property_obj.rooms))
    }
    return render(request,'landload/room.html',context)

@login_required(login_url='/')
def deactivate_property(request,pk):
    obj=Property.objects.get(id=pk)
    obj.is_active=False
    obj.save()
    return JsonResponse(True,safe=False)


def tenant(request):
    tenant = Tenant.objects.filter(landload=request.user,is_active=True)
    return render(request,'landload/tenant_list.html',{'tenant':tenant})

def tenant_add(request):
    property = Property.objects.filter(landload=request.user,is_active=True)
    form = TenantForm()
    if request.method == "POST":
        post_data = request.POST.copy()
        print('post')
        print(request.POST)
        post_data['landload']=request.user
        post_data['is_active']=True
        first_name=request.POST.get('first_name')
        middle_name=request.POST.get('middle_name')
        last_name=request.POST.get('last_name')
        phone_number=request.POST.get('phone_number')
        email=request.POST.get('email')
        form = TenantForm(post_data,request.FILES)
        if form.is_valid():
            user_data=CustomUser.objects.create(first_name=first_name,last_name=last_name,
                                      middle_name=middle_name,email=email,password='Tenant@123',
                                      phone_number=phone_number)
            # form['landload']=request.user
       
            property_obj = form.save(commit=False)
            property_obj.user = user_data  
            property_obj.save()
            messages.success(request, f'Tenant has been Created successfully!')
            return redirect('landload:tenant')
        else:
            print('errr',form.errors)
            messages.error(request, f'{form.errors}')
    return render(request,'landload/add_tenant.html',{'form':form,'property':property})


def get_room(request):
    category_id = request.GET.get('category_id')
    existing_rooms = Rooms.objects.filter(property_id=category_id).values('id', 'room_code')
    # symbole = Country.objects.get(code=category_id)
    return JsonResponse({'existing_rooms': list(existing_rooms)})

def tenant_view(request,id):
    property = Property.objects.filter(landload=request.user,is_active=True)
    tenant_obj = get_object_or_404(Tenant, pk=id)
    form = TenantReadOnlyForm(instance=tenant_obj)
    return render(request,'landload/add_tenant.html',{'form':form,'tenant_id':id,'tenant_obj':tenant_obj,'more_fun':True,
                                                      'saved_model_id': tenant_obj.room.id if tenant_obj.room else None,
    'saved_property_id': tenant_obj.property.id if tenant_obj.property else None,'property':property})

def tenant_update(request,id):
    property = Property.objects.filter(landload=request.user,is_active=True)
    tenant_obj = get_object_or_404(Tenant, pk=id)
    if request.method == 'POST':
        post_data = request.POST.copy()
        post_data['landload']=request.user
        post_data['is_active']=True
        post_data['user']=tenant_obj.user
        first_name=request.POST.get('first_name')
        middle_name=request.POST.get('middle_name')
        last_name=request.POST.get('last_name')
        phone_number=request.POST.get('phone_number')
        email=request.POST.get('email')
        form = TenantForm(post_data, request.FILES, instance=tenant_obj)
        if form.is_valid():

            obj=form.save()
            user = tenant_obj.user  # No need to query again
            # Update user fields if present in POST
            for field in ['first_name', 'middle_name', 'last_name', 'phone_number', 'email']:
                val = request.POST.get(field)
                if val:
                    setattr(user, field, val)
            user.save()
            messages.success(request, f'Tenant has been updated successfully!')
            return redirect('landload:tenant')
        else:
            print(form.errors)
    else:
        form = TenantForm(instance=tenant_obj)
    return render(request,'landload/add_tenant.html',{'form':form,'tenant_id':id,'tenant_obj':tenant_obj,
                                                      'saved_model_id': tenant_obj.room.id if tenant_obj.room else None,
    'saved_property_id': tenant_obj.property.id if tenant_obj.property else None,'property':property})