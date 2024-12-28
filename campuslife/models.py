from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from cloudinary.models import CloudinaryField


class Picture(models.Model):

    lodge_name = models.CharField(max_length=100, default='')
    image = CloudinaryField('image', folder='media/pictures')
    lodge_location = models.CharField(max_length=100)
    lodge_price = models.CharField(null=True, blank=True)
    available_vacancy = models.IntegerField(default=0)
    caretaker_number = models.CharField(max_length=11, null=True, blank=True)
    is_visible = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_pictures', null=True, blank=True)

    def __str__(self):
        return self.lodge_name


class Interior(models.Model):
    picture = models.ForeignKey(Picture, related_name='interior_images', on_delete=models.CASCADE)
    interior_image = CloudinaryField('interior_image', folder='media/interior')

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
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='questions', default=1)
    question = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    upvote_question = models.ManyToManyField(User, related_name='upvoted_question', blank=True)
    downvote_question = models.ManyToManyField(User, related_name='downvoted_question', blank=True)
    notification = models.ManyToManyField(User, related_name='notification')


class Answer(models.Model):
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers', default=1)
    question_replied = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    upvote_answer = models.ManyToManyField(User, related_name='upvoted_answer', blank=True)
    downvote_answer = models.ManyToManyField(User, related_name='downvoted_answer', blank=True)


class Reply(models.Model):
    replied_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='replies')
    answer = models.ForeignKey(Answer, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name='liked_replies', blank=True)
    dislikes = models.ManyToManyField(User, related_name='disliked_replies', blank=True)

