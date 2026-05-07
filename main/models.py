from django.db import models
from users.models import Profile, Location
from cloudinary.models import CloudinaryField
from .consts import CARS_BRANDS, TRANSMISSION_OPTIONS
from .utils import listings_image_dir 
import uuid


class Listing(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)    # saves the datetime only first time the model is 
    # created while auto_now updates the datetime every data model is overwritten or saved
    updated_at = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(Profile, on_delete=models.CASCADE,)
    brand = models.CharField(max_length=24, choices=CARS_BRANDS, default=None)
    model = models.CharField(max_length=64)
    vin = models.CharField(max_length=17)
    mileage = models.IntegerField(default=0)
    color = models.CharField(max_length=24)
    description = models.TextField()
    engine = models.CharField(max_length=24)
    transmission = models.CharField(max_length=24, choices=TRANSMISSION_OPTIONS, default=None)
    location = models.OneToOneField(Location, on_delete=models.SET_NULL, null=True)
    image = CloudinaryField("image")
    
    def __str__(self):
        return f"{self.seller.user.username}'s Listing - {self.model}"
    
    
class LikedListing(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    like_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username} liked {self.listing.model}"
    