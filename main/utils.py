def listings_image_dir(instance, filename):
    return f"{instance.seller.user.username}'s_data/listing_images/{filename}"
