from rest_framework import serializers
from .models import Picture, Interior, Rating, Review, Question, Answer, Reply, Notification, Room, Wallet


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
    lodge_id = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'lodge_name', 'lodge_id', 'review', 'created_at', 'rating', 'created_by', 'total_likes', 'total_dislikes']

    def get_created_by(self, obj):
        return obj.created_by.username if obj.created_by else None

    def get_total_likes(self, obj):
        return obj.likes.count()

    def get_total_dislikes(self, obj):
        return obj.dislikes.count()

    def get_lodge_name(self, obj):
        return obj.rating.picture_rating.lodge_name if obj.rating and obj.rating.picture_rating else None

    def get_lodge_id(self, obj):
        return obj.rating.picture_rating.id if obj.rating and obj.rating.picture_rating else None


class AnswerSerializer(serializers.ModelSerializer):
    net_score = serializers.SerializerMethodField()

    class Meta:
        model = Answer
        fields = ['id', 'question_replied', 'answered_by', 'content', 'created_at', 'net_score', 'total_replies']

    def get_net_score(self, obj):
        return obj.upvote_answer.count() - obj.downvote_answer.count()

    def get_total_replies(self, obj):
        return obj.total_replies.count()


class QuestionSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True, read_only=True, source='answers.all')

    class Meta:
        model = Question
        fields = ['id', 'asked_by', 'question', 'created_at', 'upvote_question', 'downvote_question', 'answers',
                  'total_answers']

    def get_net_score(self, obj):
        return obj.upvote_answer.count() - obj.downvote_answer.count()

    def get_total_answers(self, obj):
        return obj.total_answers.count()


class ReplySerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Reply
        fields = ['id', 'replied_by', 'answer', 'content', 'created_at', 'likes', 'dislikes']


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = '__all__'


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'
