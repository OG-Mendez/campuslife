from rest_framework import serializers
from .models import Picture, Interior, Rating, Review, Question, Answer, Reply
from django.conf import settings


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'


class InteriorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interior
        fields = '__all__'


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField()
    total_likes = serializers.SerializerMethodField()
    total_dislikes = serializers.SerializerMethodField()
    lodge_name = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id','lodge_name', 'review', 'created_at', 'rating', 'created_by', 'total_likes', 'total_dislikes']

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else None

    def get_total_likes(self, obj):
        return obj.likes.count()

    def get_total_dislikes(self, obj):
        return obj.dislikes.count()

    def get_lodge_name(self, obj):
        return obj.rating.picture_rating.lodge_name if obj.rating and obj.rating.picture_rating else None


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = '__all__'


class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'

