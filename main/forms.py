from django import forms
from cloudinary.forms import CloudinaryFileField
from .models import Listing


class ListingForm(forms.ModelForm):
    class Meta:
        image = CloudinaryFileField()
        model = Listing
        fields = {
            "brand", "model", "vin", "mileage", "color", "description", "engine", "transmission", "image"
        }
