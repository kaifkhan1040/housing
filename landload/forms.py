from django import forms
from users.models import CustomUser
from django.forms import EmailInput
from django.forms import ModelForm, TextInput, EmailInput, CharField, PasswordInput, ChoiceField, BooleanField, \
    NumberInput, DateInput
from .models import Property,Rooms,Tenant,Dues

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

class DuesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    class Meta:
            model = Dues
            fields = "__all__"

class DuesReadOnlyForm(DuesForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['readonly'] = True
            field.widget.attrs['disabled'] = True


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

class TenantInviteForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter tenant email'})
    )
    class Meta:
            model = Tenant
            fields = ['property','room','rent','deposit','email']


class TenantInviteReadOnlyForm(TenantForm):
    first_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'})
    )
    middle_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Middle Name'})
    )
    last_name = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'last Name'})
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter tenant email'})
    )
    phone_number = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'})
    )

    class Meta:
        model = Tenant
        fields = ['property', 'room', 'rent', 'deposit', 'first_name', 'middle_name', 'email','phone_number',
                  'photo','id_proof','address_proof','visa_proof','bank_statement']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['middle_name'].initial = self.instance.user.middle_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
            self.fields['phone_number'].initial = self.instance.user.phone_number

        for name, field in self.fields.items():
            value = self.initial.get(name) or getattr(self.instance, name, None)

            if value:  
                field.widget.attrs['readonly'] = True
                field.widget.attrs['disabled'] = True