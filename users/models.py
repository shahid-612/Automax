from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from localflavor.pk.models import PKStateField
from cloudinary.models import CloudinaryField
from .utils import user_pic_dir



class Location(models.Model):
    address_1 = models.CharField(max_length=128, blank=True)
    address_2 = models.CharField(max_length=128, blank=True)
    city = models.CharField(max_length=64)
    state = PKStateField(default="PK-PB")
    zip_code = models.IntegerField(
        validators=[
            MinValueValidator(10000),
        ], blank=True,null=True
    )
    
    def __str__(self):
        return f"Location {self.id}"
    
    
    
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    photo = CloudinaryField("image", null=True)    # 2 attr are passed to user_pic_dir
    # 1 is the instance (Profile instance) and second is filename which is being selected 
    bio = models.TextField(max_length=2000, blank=True)
    phone_number = models.CharField(max_length=13, blank=True)
    location = models.ForeignKey(Location, null=True, on_delete=models.SET_NULL, 
                                    related_name="user_location")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    