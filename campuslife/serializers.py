from django.utils import timezone
from rest_framework import serializers
from .models import Picture, Interior, Rating, Review, Question, Answer, Reply, Notification, Room, Wallet, Agent, AgentEarning


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


class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Agent
        fields = '__all__'


class RoomUploadSerializer(serializers.Serializer):
    lodge = serializers.IntegerField()
    number = serializers.CharField(max_length=10)
    image = serializers.ImageField(required=False)
    video = serializers.FileField(required=True)
    agent = serializers.PrimaryKeyRelatedField(queryset=Agent.objects.all())

    def create(self, validated_data):
        agent = validated_data.pop('agent')
        image_file = validated_data.pop('image', None)
        video_file = validated_data.pop('video', None)
        lodge_id = validated_data.pop('lodge')
        room_number = validated_data.pop('number')

        try:
            lodge = Picture.objects.get(id=lodge_id)
        except Picture.DoesNotExist:
            raise serializers.ValidationError({"lodge": "Lodge with this id does not exist."})

        room = Room.objects.create(
            lodge=lodge,
            room=agent,
            room_number=room_number,
            room_image=image_file,
            room_video=video_file)
        return room

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "lodge": instance.lodge.lodge_name,
            "number": instance.room_number,
            "image_url": instance.room_image.url if instance.room_image else None,
            "video_url": instance.room_video.url if instance.room_video else None,
        }


class AgentEarningSerializer(serializers.ModelSerializer):
    payout_date = serializers.DateTimeField(
        format="%Y-%m-%d %H:%M:%S",
        default_timezone=timezone.get_current_timezone(),
    )

    class Meta:
        model = AgentEarning
        fields = ("payout_date", "payout_amount")