from django import forms
from users.models import CustomUser
from django.forms import EmailInput
from django.forms import ModelForm, TextInput, EmailInput, CharField, PasswordInput, ChoiceField, BooleanField, \
    NumberInput, DateInput
from .models import Property,Rooms,Tenant

class PropertyForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['short_name'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['name'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['address_1'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['address_2'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['city'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['postcode'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['property_type'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['rooms'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['cost'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['start_date'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['end_date'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['prop_thumbnail'].widget.attrs.update({'class': 'form-control valid'})
        
        
    class Meta:
            model = Property
            fields = "__all__"
            widgets = {
            'start_date':DateInput(attrs={
                'type': 'date',
                'class': "form-control mb-2",}),
             'end_date':DateInput(attrs={
                'type': 'date',
                'class': "form-control mb-2",
                'placeholder':"date hai"}),
                }
            
class PropertyReadOnlyForm(PropertyForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True


class RoomsForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['property'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['type_of_room'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['ensuite'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['total_capacity'].widget.attrs.update({'class': 'form-control valid'})
        self.fields['rent'].widget.attrs.update({'class': 'form-control valid'})
       
        
    class Meta:
            model = Rooms
            fields = "__all__"


class TenantForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
            model = Tenant
            fields = "__all__"

class TenantReadOnlyForm(TenantForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True
