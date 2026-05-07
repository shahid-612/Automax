from django import forms 
from django.contrib.auth.models import User
from .models import Location, Profile
from  .widgets import CustomImageWidget
from cloudinary.forms import CloudinaryFileField


class LocationForm(forms.ModelForm):
    address_1 = forms.CharField(max_length=128, required=True)
    class Meta:
        model = Location
        fields = {
            "address_1", "address_2", "city", "state", "zip_code",
        }
        
        
class UserForm(forms.ModelForm):
    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = (
            "username", "first_name", "last_name",
        )


class ProfileForm(forms.ModelForm):
    photo = CloudinaryFileField()
    class Meta:
        model = Profile
        fields = ["photo", "bio", "phone_number"] 
        # widgets = {
        #     'photo': forms.ClearableFileInput(attrs={
        #         'class': 'form-control-file',
        #     })
        # }
