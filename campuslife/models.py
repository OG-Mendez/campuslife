from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField


class Picture(models.Model):
    lodge_name = models.CharField(max_length=100, default='')
    image = CloudinaryField('image')
    lodge_location = models.CharField(max_length=100)
    lodge_price = models.CharField(null=True, blank=True)
    available_vacancy = models.IntegerField(default=0)
    caretaker_number = models.CharField(max_length=11, null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    def __str__(self):
        return self.lodge_name


class Interior(models.Model):
    picture = models.ForeignKey(Picture, related_name='interior_images', on_delete=models.CASCADE)
    interior_image = models.ImageField(upload_to='pictures/interior/')

    def __str__(self):
        return f"Interior of {self.picture.lodge_name}"


class Rating(models.Model):
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', default=1)
    picture_rating = models.ForeignKey(Picture, related_name='picture_ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    review = models.CharField(max_length=500, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rated_by.username} - {self.picture_rating.lodge_name} ({self.rating}/5)"

