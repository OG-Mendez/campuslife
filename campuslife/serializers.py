from rest_framework import serializers
from .models import Picture, Interior, Rating
from django.conf import settings


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'

    def get_image(self, obj):
        # Ensure the API always returns the correct URL
        return obj.image.url


class InteriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interior
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'
