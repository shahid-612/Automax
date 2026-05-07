from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.views import View
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import UserForm, ProfileForm, LocationForm
from main.models import Listing, LikedListing


class RegisterView(View):
    
    def get(self, request):
        register_form = UserCreationForm()
        return render(request, "views/register.html", {
            "register_form": register_form,
        })
    
    def post(self, request):
        register_form = UserCreationForm(data=request.POST)
        if register_form.is_valid():
            user = register_form.save()
            user.refresh_from_db()
            login(request, user)
            messages.success(request, f"Welcome {user.username}! You registered succesfully.")
            return redirect("home")
        else:
            messages.error(request, "An error occured during registration.")
            return render(request, "views/register.html", {
                "register_form": register_form,
            })
            

@method_decorator(login_required, name="dispatch")
class ProfileView(View):
    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.profile = request.user.profile
        self.user_listings = Listing.objects.filter(seller=self.profile)
        
        # returning the liked lists of user
        self.user_liked_listings = LikedListing.objects.filter(profile=request.user.profile)
        self.liked_listings_objects = []
        for listing in self.user_liked_listings:
            listing_obj = listing.listing
            self.liked_listings_objects.append(listing_obj)
        
        # handling the no of likes
        self.listings = Listing.objects.all()
        self.like_nos = dict()
        for listing in self.listings:
            no_of_likes = len(LikedListing.objects.filter(listing=listing))
            self.like_nos.update({listing.id: no_of_likes})
    
    def get(self, request):
        user_form = UserForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        location_form = LocationForm(instance=request.user.profile.location)
        
        # handing that creepy profile photo issue as null is allowed for the photo, so handlig its url
        if self.profile.photo:
            photo_url = self.profile.photo.url
        else:
            photo_url = False
        
        return render(request, "views/profile.html", {
            "user_form": user_form,
            "profile_form": profile_form,
            "location_form": location_form,
            "user_listings": self.user_listings,
            "user_liked_listings": self.user_liked_listings,
            "liked_listing_objects": self.liked_listings_objects,
            "profile_photo_url": photo_url,
            "likes_counter": self.like_nos,
        })
    
    def post(self, request):
        user_form   = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        location_form = LocationForm(request.POST, instance=request.user.profile.location)
        if user_form.is_valid() and profile_form.is_valid() and location_form.is_valid():
            user_form.save()
            profile_form.save()
            location_form.save()
            messages.success(request, "Profile updated successfully.")
        else:
            messages.error(request, "Error occured while updating your profile.")
        return render(request, "views/profile.html", {
            "user_form": user_form,
            "profile_form": profile_form,
            "location_form": location_form,
            "user_listings": self.user_listings,
            "user_liked_listings": self.user_liked_listings,
            "liked_listing_objects": self.liked_listings_objects,
            "profile_photo_url": self.profile.photo.url,
            "likes_counter": self.like_nos,
        })


def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            login_form = AuthenticationForm(request=request, data=request.POST)
            if login_form.is_valid():
                username =login_form.cleaned_data.get("username")
                # password = login_form.cleaned_data.get("password") - no need of password as its already 
                # authenticated using authentication form
                user = login_form.get_user()
                login(request, user)
                messages.success(request, f"You are now logged in as {username}")
                return redirect("home")
            else:
                messages.error(request, "Wrong Username or Password.")
                return render(request, "views/login.html", {
                    "login_form": login_form,
                   # "error": "danger", -inspite of key and tricky stuff in templates I used settings to 
                   # fix its class styling using bootstrap  
                })
        else:
            login_form = AuthenticationForm()
            return render(request, "views/login.html", {
                "login_form": login_form,
                })


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, f"{request.user.username} logged out successfully.")
    return redirect("main")

