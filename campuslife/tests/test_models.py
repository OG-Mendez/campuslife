from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.test import TestCase

from campuslife.models import Picture, Rating, Review


class RatingConstraintTests(TestCase):
    """Rating enforces one rating per (user, lodge) pair."""

    def setUp(self):
        self.user = User.objects.create_user(username="alice", password="pw12345")
        self.picture = Picture.objects.create(
            lodge_name="Test Lodge", lodge_location="Nsukka",
        )

    def test_duplicate_rating_is_rejected(self):
        Rating.objects.create(rated_by=self.user, picture_rating=self.picture, rating=4)
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Rating.objects.create(rated_by=self.user, picture_rating=self.picture, rating=2)

    def test_different_users_can_each_rate_same_lodge(self):
        other = User.objects.create_user(username="bob", password="pw12345")
        Rating.objects.create(rated_by=self.user, picture_rating=self.picture, rating=4)
        Rating.objects.create(rated_by=other, picture_rating=self.picture, rating=2)
        self.assertEqual(self.picture.picture_ratings.count(), 2)


class ReviewLikeDislikeTests(TestCase):
    """total_likes/total_dislikes reflect the actual M2M state, not just non-zero."""

    def setUp(self):
        self.author = User.objects.create_user(username="author", password="pw12345")
        self.picture = Picture.objects.create(lodge_name="Lodge B", lodge_location="Enugu")
        rating = Rating.objects.create(rated_by=self.author, picture_rating=self.picture, rating=5)
        self.review = Review.objects.create(rating=rating, created_by=self.author, review="Great place.")

    def test_likes_and_dislikes_count_independently(self):
        liker1 = User.objects.create_user(username="liker1", password="pw12345")
        liker2 = User.objects.create_user(username="liker2", password="pw12345")
        disliker = User.objects.create_user(username="disliker", password="pw12345")

        self.review.likes.add(liker1, liker2)
        self.review.dislikes.add(disliker)

        self.assertEqual(self.review.total_likes(), 2)
        self.assertEqual(self.review.total_dislikes(), 1)

    def test_removing_a_like_updates_the_count(self):
        liker = User.objects.create_user(username="liker", password="pw12345")
        self.review.likes.add(liker)
        self.assertEqual(self.review.total_likes(), 1)

        self.review.likes.remove(liker)
        self.assertEqual(self.review.total_likes(), 0)
