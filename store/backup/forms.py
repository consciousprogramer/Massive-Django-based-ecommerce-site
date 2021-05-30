from .models import ShippingAddress,Customer,User
from django.forms import ModelForm,Select,RadioSelect
from django import forms
from django.contrib.auth.forms import UserCreationForm
class ShippingAddressForm(ModelForm):
    class Meta:
        model = ShippingAddress
        exclude = ['Owner','Father']
        ADDRESSTYPES = (('HOME','HOME') , ('WORK','Work/Office'))
        widgets = {
            'State':Select(choices=ADDRESSTYPES,),
            'District':Select(choices=ADDRESSTYPES,),
            'AddressType':Select(attrs={}),
        }

        help_texts = {
            'OwnerName':"If you are below 18 age, write your Mother/ Father/ Gaurdian's Name"
        }


# --> OMG FOR SO LONG I DIDNOT USED UserCreationform
# because i thought i can only keep fields which are present on user
# BUT I WAS HUGLY WRONG You can have extra fields on user creation form
# see below user actually do not have Ph num field,usercreationform
# here is acting as a sve crriar for the extra data i required while Creating New user 
# and saving other related models, ex- customer or profile
# i Think django forms have a behaviour that they take only
# the field data they have defined

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=128,label='Your Name')
    PhoneNumber = forms.CharField(label='Phone Number',max_length=11,min_length=10,help_text='10 Digit Phone Number',widget=forms.NumberInput())
    class Meta():
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name','PhoneNumber')
    
    help_text = {'password1',''}
    # form have method self.add_error(<field>,error_obj)

class RegisterForm(forms.Form):
    Username = forms.CharField(label='Enter Username',help_text='You can use your Email or Phone number')
    Name = forms.CharField(label='Your Full Name',)
    Password = forms.CharField(label='Password',widget=forms.PasswordInput())
    PhoneNumber = forms.CharField(label='Phone Number',max_length=11,min_length=10,help_text='10 Digit Phone Number',widget=forms.NumberInput())

class LoginForm(forms.Form):
    Username = forms.CharField(label='Enter Username')
    Password = forms.CharField(label='Password',widget=forms.PasswordInput())