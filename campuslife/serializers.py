from rest_framework import serializers
from .models import Picture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = ['lodge_name', 'image', 'lodge_location', 'lodge_price', 'available_vacancy', 'caretaker_number']
