from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from  django.core.exceptions import PermissionDenied, ValidationError
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout
from django.urls import reverse
from .models import Listing, LikedListing
from .forms import ListingForm
from .filters import ListingFilter
from users.forms import LocationForm


def main_view(request):
    return render(request, "views/main.html", {
        "user":request.user,
    })
    

@login_required
def home_view(request):
    listings = Listing.objects.all()
    listing_filter = ListingFilter(request.GET, queryset=listings)
    
    # handling the liked listings
    liked_listings = LikedListing.objects.filter(profile=request.user.profile)
    liked_listing_objects = []
    for listing in liked_listings:
        liked_obj = listing.listing
        liked_listing_objects.append(liked_obj)
    
    # handling the no of likes
    like_nos = dict()
    for listing in listings:
        no_of_likes = len(LikedListing.objects.filter(listing=listing))
        like_nos.update({listing.id: no_of_likes,})
        
    return render(request, "views/home.html", {
        "listing_filter": listing_filter,
        "liked_listing_objects": liked_listing_objects,
        "likes_counter": like_nos,
    })


@login_required
def list_view(request):
    if request.method == "GET":
        listing_form = ListingForm()
        location_form = LocationForm()
        return render(request, "views/list.html", {
            "listing_form": listing_form,
            "location_form": location_form,
            "edit": False,
        })
    elif request.method == "POST":
        listing_form = ListingForm(request.POST, request.FILES)
        location_form = LocationForm(request.POST)
        if listing_form.is_valid() and location_form.is_valid():
            listing = listing_form.save(commit=False)
            location = location_form.save()
            listing.seller = request.user.profile
            listing.location = location
            listing.save()
            messages.info(request, f"{listing.model} is listed successfully.")
            return redirect("home")
        else:
            messages.error(request, "You entered invalid data.")
            return render(request, "views/list.html", {
                "listing_form": listing_form,
                "location_form": location_form,
                "edit": False,
            })
    else:
        logout(request.user)
        raise PermissionDenied
    

@login_required
def listing_view(request, id):
    try:
        listing_object = Listing.objects.get(pk=id)
        return render(request, "views/listing.html", {
            "listing": listing_object,
        })
    except ValidationError:
        messages.error(request, "Invalid url.")
        return redirect("home")
    
@login_required
def edit_view(request, id):
    try:
        listing_object = Listing.objects.get(pk=id)
        if listing_object.seller.user == request.user:
            if request.method == "GET":
                listing_form = ListingForm(instance=listing_object)
                location_form = LocationForm(instance=listing_object.location)
                return render(request, "views/list.html", {
                    "listing_form": listing_form,
                    "location_form": location_form,
                    "listing_object": listing_object,
                    "edit": True,
                })

            elif request.method == "POST":
                listing_form = ListingForm(request.POST, request.FILES, instance=listing_object)
                location_form = LocationForm(request.POST, instance=listing_object.location)
                if listing_form.is_valid() and location_form.is_valid():
                    listing = listing_form.save(commit=False)
                    location = location_form.save()
                    listing.seller = request.user.profile
                    listing.location = location
                    listing.save()
                    messages.success(request, "Listing edited successfully.")
                    print("reached here")
                    return redirect("listing", id=listing_object.id)
                else:
                    messages.error(request, "You entered invalid data.")
                    return render(request, "views/list.html", {
                        "listing_form": listing_form,
                        "location_form": location_form,
                        "listing_object": listing_object,
                        "edit": True,
                    })
                    
            else:
                raise PermissionDenied
        else:
            raise PermissionDenied(f"Only {listing_object.seller.user.username} can edit this listing.")
        
    except ValidationError:
        messages.error(request, "Invalid url")
        return redirect("home")


@login_required
def like_listing_view(request, id):
    listing = get_object_or_404(Listing, id=id)    # either it will return the model object or 404
    liked_listing, created = LikedListing.objects.get_or_create(profile=request.user.profile, listing=listing)   # 
    # it will return a tuple first containing the object and 2nd is boolean value either the object iis created
    # or already present
    if created:
        liked_listing.save()
    else:
        liked_listing.delete()
    return JsonResponse(
        {
            "liked_or_disliked": created,
        }
        )
    