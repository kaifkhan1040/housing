from django.db import models
from django.db import transaction
# Create your models here.
from django.db import models
from users.models import CustomUser

class Property(models.Model):
    ROOM_CHOICES = [(str(i), i) for i in range(1, 11)]


    custom_id = models.CharField(max_length=10, unique=True, blank=True)
    short_name = models.CharField(max_length=100)
    name = models.CharField(max_length=200)
    address_1 = models.CharField(max_length=255)
    address_2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    postcode = models.CharField(max_length=20)

    property_type = models.CharField(max_length=100)
    rooms = models.CharField(choices=ROOM_CHOICES)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    status =models.BooleanField(default=True)
    prop_thumbnail = models.ImageField(upload_to='property_thumbnails/', blank=True, null=True)
    landload = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True)
    is_active =models.BooleanField(default=True)

    def __str__(self):
        return f"{self.short_name} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.custom_id:
            with transaction.atomic():
                # Lock the table during ID generation
                last_obj = Property.objects.select_for_update().order_by('-id').first()
                if last_obj and last_obj.custom_id.startswith('PP'):
                    try:
                        last_number = int(last_obj.custom_id[2:])
                    except ValueError:
                        last_number = 100
                    next_number = last_number + 1
                else:
                    next_number = 101

                # Loop to ensure uniqueness
                while True:
                    candidate_id = f'PP{next_number}'
                    if not Property.objects.filter(custom_id=candidate_id).exists():
                        self.custom_id = candidate_id
                        break
                    next_number += 1

        super().save(*args, **kwargs)
    

class Rooms(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='room_set')    
    type_of_room = models.CharField(choices=[('Single','Single'),('Double','Double')])
    ensuite = models.CharField(choices=[('Yes','Yes'),('No','No')])
    total_capacity = models.CharField(choices=[('1','1'),('2','2'),('3','3'),('4','4'),('5','5')])
    rent = models.FloatField(default=0.0)
    room_code = models.CharField(max_length=10, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.room_code:
            with transaction.atomic():
                last_obj = Rooms.objects.select_for_update().order_by('-id').first()
                if last_obj and last_obj.room_code.startswith('Room'):
                    try:
                        last_number = int(last_obj.room_code[4:])  # Use [4:] to skip "Room"
                    except ValueError:
                        last_number = 100
                    next_number = last_number + 1
                else:
                    next_number = 101

                # Generate unique room_code
                while True:
                    candidate_id = f'Room{next_number}'
                    if not Rooms.objects.filter(room_code=candidate_id).exists():
                        self.room_code = candidate_id
                        break
                    next_number += 1

        super().save(*args, **kwargs)


class Tenant(models.Model):
    user=models.ForeignKey(CustomUser,on_delete=models.CASCADE,null=True,blank=True)
    landload = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='landload_properties')
    property=models.ForeignKey(Property,on_delete=models.CASCADE)
    room=models.ForeignKey(Rooms,on_delete=models.CASCADE)
    rent=models.FloatField()
    deposit=models.FloatField()
    photo=models.ImageField(upload_to='tenant/photo',blank=True,null=True)
    id_proof=models.ImageField(upload_to='tenant/id_proof',blank=True,null=True)
    address_proof=models.ImageField(upload_to='tenant/address_proof',blank=True,null=True)
    visa_proof=models.ImageField(upload_to='tenant/visa_proof',blank=True,null=True)
    bank_statement=models.ImageField(upload_to='tenant/bank_statement',blank=True,null=True)
    custom_id = models.CharField(max_length=10, unique=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.custom_id:
            with transaction.atomic():
                # Lock the table during ID generation
                last_obj = Tenant.objects.select_for_update().order_by('-id').first()
                if last_obj and last_obj.custom_id.startswith('TN'):
                    try:
                        last_number = int(last_obj.custom_id[2:])
                    except ValueError:
                        last_number = 100
                    next_number = last_number + 1
                else:
                    next_number = 101

                # Loop to ensure uniqueness
                while True:
                    candidate_id = f'TN{next_number}'
                    if not Tenant.objects.filter(custom_id=candidate_id).exists():
                        self.custom_id = candidate_id
                        break
                    next_number += 1

        super().save(*args, **kwargs)




