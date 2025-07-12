from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField


class Picture(models.Model):
    lodge_name = models.CharField(max_length=100, default='')
    image = models.ImageField(upload_to="lodges/")
    lodge_location = models.CharField(max_length=100)
    lodge_price = models.CharField(null=True, blank=True)
    agent_fee = models.CharField(null=True, blank=True)
    agreement_fee = models.CharField(null=True, blank=True)
    available_vacancy = models.IntegerField(default=0)
    caretaker_number = models.CharField(max_length=11, null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    vacant_room = models.IntegerField(null=True, blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_pictures', null=True, blank=True)

    def __str__(self):
        return self.lodge_name


class Interior(models.Model):
    picture = models.ForeignKey(Picture, related_name='interior_images', on_delete=models.CASCADE)
    interior_image = models.ImageField(upload_to="interiors/")

    def __str__(self):
        return f"Interior of {self.picture.lodge_name}"


class Rating(models.Model):
    rated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ratings', default=1)
    picture_rating = models.ForeignKey(Picture, related_name='picture_ratings', on_delete=models.CASCADE)
    rating = models.IntegerField(default=0, validators=[MinValueValidator(1), MaxValueValidator(5)])
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('rated_by', 'picture_rating')

    def __str__(self):
        return f"{self.rated_by.username} - {self.picture_rating.lodge_name} ({self.rating}/5)"


class Review(models.Model):
    rating = models.ForeignKey(Rating, related_name='reviews', on_delete=models.CASCADE)
    review = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_reviews')
    likes = models.ManyToManyField(User, related_name='liked_reviews', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_reviews', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.created_by.username} for Rating {self.rating.id}"

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()


class Question(models.Model):
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questioned_by', default=1)
    question = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    upvote_question = models.ManyToManyField(User, related_name='upvoted_question', blank=True)
    downvote_question = models.ManyToManyField(User, related_name='downvoted_question', blank=True)
    notification = models.ManyToManyField(User, related_name='notification')

    def total_upvote_question(self):
        return self.upvote_question.count()

    def total_downvote_question(self):
        return self.downvote_question.count()

    def total_answers(self):
        return self.answers.count()


class Answer(models.Model):
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answered_by', default=1)
    question_replied = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    upvote_answer = models.ManyToManyField(User, related_name='upvoted_answer', blank=True)
    downvote_answer = models.ManyToManyField(User, related_name='downvoted_answer', blank=True)
    parent_answer = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE,
                                      related_name='child_answers')

    def get_conversation_thread(self):
        thread = [self]
        for child in self.child_answers.all().order_by('created_at'):
            thread.extend(child.get_conversation_thread())
        return thread

    def total_upvote_answer(self):
        return self.upvote_answer.count()

    def total_downvote_answer(self):
        return self.downvote_answer.count()

    def total_replies(self):
        return self.replies.count()


class Reply(models.Model):
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replied_by')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_replies', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_replies', blank=True)

    def __str__(self):
        return f"Reply by {self.replied_by.username} for Answer {self.answer.id}"

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()


class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_notification")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="question_notification")
    notify = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} will be notified if new answers to {self.question.question}"


class Agent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="agent")
    first_name = models.CharField(null=False)
    last_name = models.CharField(null=False)
    phone_number = models.CharField()
    account_number = models.CharField(blank=True, null=True)
    bank_name = models.CharField(null=True, blank=True, max_length=256)
    wallet = models.IntegerField(default=0)


class Room(models.Model):
    lodge = models.ForeignKey(Picture, on_delete=models.CASCADE, related_name="room")
    room = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="room_agent")
    room_number = models.PositiveIntegerField(blank=True, null=True)
    room_type = models.CharField(null=True, blank=True)
    room_floor = models.CharField(null=True, blank=True)
    room_image = models.ImageField(upload_to="payment/", blank=True, null=True)
    room_video = models.FileField(upload_to="payment/", blank=True, null=True)
    room_inspection = models.IntegerField(null=True, blank=True)
    display = models.BooleanField(default=False)
    uploaded = models.BooleanField(default=False)
    vacancy_indicator = models.BooleanField(default=False)
    caretaker_number = models.CharField(null=True)
    agent = models.IntegerField(null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    agent_indicator = models.IntegerField(null=True, blank=True)


class Wallet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_points")
    point = models.PositiveIntegerField(default=0)


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_wallet")
    amount = models.PositiveIntegerField(blank=False)
    email = models.EmailField(blank=True)
    reference = models.CharField(null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)


class AgentEarning(models.Model):
    agent = models.ForeignKey(Agent, on_delete=models.CASCADE, related_name="earning")
    payout_date = models.DateTimeField()
    payout_amount = models.IntegerField(null=True, blank=True)
