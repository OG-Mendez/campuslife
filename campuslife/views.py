from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime
from random import sample, seed
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Picture, Interior, Rating, Review, Question, Answer, Reply, Notification
from .serializers import PictureSerializer, InteriorSerializer, RatingSerializer, QuestionSerializer, AnswerSerializer, \
    ReplySerializer, ReviewSerializer, NotificationSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
import numpy as np
from sentence_transformers import SentenceTransformer
from django.db.models import Count


# Create your views here.

def picture_list(request):
    available_vacancy = request.GET.get('available_vacancy')
    lodge_name = request.GET.get('lodge_name')
    lodge_location = request.GET.get('lodge_location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    pictures = Picture.objects.all().order_by('-id')

    if min_price and max_price:
        pictures = pictures.filter(lodge_price__gte=min_price, lodge_price__lte=max_price)

    if available_vacancy:
        pictures = pictures.filter(available_vacancy=available_vacancy)

    if lodge_name:
        pictures = pictures.filter(lodge_name__icontains=lodge_name)

    if lodge_location:
        pictures = pictures.filter(lodge_location__icontains=lodge_location)  # Corrected typo here

    return render(request, 'campuslife/picture_home.html', {'pictures': pictures})


def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'campuslife/picture_detail.html', {'picture': picture})


def display_accounts(request):
    users = User.objects.all()
    user_count = User.objects.count() - 8  # Subtract founder accounts more efficiently
    return render(request, 'campuslife/get_accounts.html', {'users': users, 'user_count': user_count})


def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
        else:
            User.objects.create_user(username=username, email=email, password=password)
            messages.success(request, 'Account created successfully!')
            return redirect('login')

    return render(request, 'campuslife/signup.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('picture_list')
        else:
            messages.error(request, 'Invalid credentials.')

    return render(request, 'campuslife/login.html')


@api_view(['GET'])
@permission_classes([AllowAny])
def picture_list_api(request):
    pictures = Picture.objects.all().order_by('-id')
    serializer = PictureSerializer(pictures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def picture_detail_api(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    serializer = PictureSerializer(picture)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def signup_view_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')

    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already taken'}, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(email=email).exists():
        return Response({'error': 'Email already taken'}, status=status.HTTP_400_BAD_REQUEST)

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'message': 'User created successfully', 'token': token.key}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view_api(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response(
            {'error': 'Invalid credentials, please check to make sure the email and/or password is correct'},
            status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view_api(request):
    try:
        token = Token.objects.get(user=request.user)
        token.delete()
        return Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
    except Token.DoesNotExist:
        return Response({"error": "Token not found"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    username = request.data.get('username')
    email = request.data.get('email')
    if User.objects.filter(email=email, username=username).exists():
        user = User.objects.get(username=username)
        token = default_token_generator.make_token(user)

        reset_url = f"https://campuslifetechnologies.com.ng/reset-password/{user.id}/{token}"

        email = EmailMessage(
            subject='Password Reset Request',
            body=f'You are receiving this email because we received a request to change the password for your '
                 f'Campuslife account.\n\nClick the link to reset password: {reset_url}\n\nIf you did not initiate this '
                 f'request, please contact us immediately at info@campuslifetechnologies.com.ng\n\nThank '
                 f'you\nCampuslife Technologies',
            from_email='info@campuslifetechnologies.com.ng',
            to=[email],
            headers={'Content-Type': 'text/plain'},
        )
        email.send()

        return Response({'message': 'Password reset link sent to your email.'})
    return Response({'message': 'Email not found.'}, status=404)


@api_view(['POST'])
def password_reset_confirm(request):
    user_id = request.data.get('user_id')
    token = request.data.get('token')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(id=user_id)
        if default_token_generator.check_token(user, token):
            user.set_password(new_password)
            user.save()
            return Response({'message': 'Password reset successful.'})
        return Response({'message': 'Invalid token.'}, status=400)
    except User.DoesNotExist:
        return Response({'message': 'User not found.'}, status=404)


@api_view(['GET'])
def interior_view_api(request):
    interiors = Interior.objects.all()
    serializer = InteriorSerializer(interiors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ratings(request):
    if request.method == 'GET':
        lodge_name = request.query_params.get('lodge_name')

        if lodge_name:
            try:
                picture = Picture.objects.get(lodge_name=lodge_name)
                ratings = Rating.objects.filter(picture_rating=picture)

                data = [
                    {
                        'rated_by': rating.rated_by.username,
                        'review': rating.review,
                        'lodge_name': picture.lodge_name,
                        'total_likes': rating.total_likes(),
                        'total_dislikes': rating.total_dislikes()
                    }
                    for rating in ratings
                ]
                return Response({'lodge_name': lodge_name, 'ratings': data}, status=status.HTTP_200_OK)
            except Picture.DoesNotExist:
                return Response({'error': 'Lodge not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            ratings = Rating.objects.select_related('picture_rating').all()

            data = {}
            for rating in ratings:
                lodge_name = rating.picture_rating.lodge_name
                if lodge_name not in data:
                    data[lodge_name] = []
                data[lodge_name].append({
                    'review_id': rating.review.id,
                    'rated_by': rating.rated_by.username,
                    'rating': rating.rating,
                    'review': rating.review,
                    'total_likes': rating.total_likes(),
                    'total_dislikes': rating.total_dislikes()
                })

            return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_rating(request):
    lodge_id = request.data.get('id')
    rating = request.data.get('rating')

    if not lodge_id or not rating:
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        picture = Picture.objects.get(id=lodge_id)

        if Rating.objects.filter(rated_by=request.user, picture_rating=picture).exists():
            return Response({'error': 'You have already rated this lodge'}, status=status.HTTP_400_BAD_REQUEST)

        rating_instance = Rating.objects.create(
            rated_by=request.user,
            picture_rating=picture,
            rating=rating,
        )
        lodge_name = picture.lodge_name
        return Response({
            'message': 'Rating added successfully!',
            'rating': {
                'lodge_name': lodge_name,
                'rating': rating_instance.rating,
                'rated_by': rating_instance.rated_by.username,
            }
        }, status=status.HTTP_201_CREATED)
    except Picture.DoesNotExist:
        return Response({'error': 'Lodge not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_review(request):
    try:
        lodge_id = request.data.get("id")
        rating_value = request.data.get("rating")
        review_text = request.data.get("review_text")

        if not lodge_id or not rating_value or not review_text:
            return Response({"error": "Lodge ID, rating, and review text are required."}, status=400)

        try:
            lodge = Picture.objects.get(id=lodge_id)
        except Picture.DoesNotExist:
            return Response({"error": "Lodge not found."}, status=404)

        rating, created = Rating.objects.get_or_create(
            rated_by=request.user,
            picture_rating=lodge,
            defaults={"rating": rating_value}
        )

        if not created and rating.rating != rating_value:
            rating.rating = rating_value
            rating.save()

        if Review.objects.filter(rating=rating, created_by=request.user).exists():
            return Response({"error": "You have already reviewed this rating."}, status=400)

        review = Review.objects.create(
            rating=rating,
            review=review_text,
            created_by=request.user
        )

        return Response({
            "message": "Review created successfully",
            "review_id": review.id,
            "lodge_id": lodge.id,
            "lodge_name": lodge.lodge_name,
            "rating": rating.rating,
            "review_text": review.review,
            "created_by": request.user.username,
        }, status=201)

    except Exception as e:
        return Response({"error": f"An unexpected error occurred: {str(e)}"}, status=500)


@api_view(['GET'])
def list_reviews(request):
    if request.method == "GET":
        try:
            reviews = Review.objects.all()

            serializer = ReviewSerializer(reviews, many=True)

            return Response(serializer.data, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)
    return Response({"error": "Invalid request method"}, status=405)


@api_view(['GET'])
@permission_classes([AllowAny])
def average_rating_for_lodge(request):
    lodge_id = request.query_params.get("id")

    if not lodge_id:
        return Response({'error': 'Lodge ID is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        average = Rating.objects.filter(picture_rating_id=lodge_id).aggregate(
            average_rating=Avg('rating')
        )['average_rating']

        picture = Picture.objects.get(id=lodge_id)
        lodge_name = picture.lodge_name

        return Response({
            'lodge_id': lodge_id,
            'lodge_name': lodge_name,
            'average_rating': round(average, 1) if average else None
        }, status=status.HTTP_200_OK)
    except Picture.DoesNotExist:
        return Response({'error': 'Lodge not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_dislike_review(request):
    review_id = request.data.get('id')
    review = get_object_or_404(Review, id=review_id)
    action = request.data.get('action')
    if not review_id or not action:
        return Response({'error': 'Review ID and action are required'}, status=status.HTTP_400_BAD_REQUEST)

    if action not in ['like', 'dislike']:
        return Response({'error': 'Invalid action. Use "like" or "dislike".'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if action == 'like':
            if request.user in review.dislikes.all():
                review.dislikes.remove(request.user)
            review.likes.add(request.user)
        elif action == 'dislike':
            if request.user in review.likes.all():
                review.likes.remove(request.user)
            review.dislikes.add(request.user)

        return Response({
            'message': f'Review {action}d successfully!',
            'review_id': review.id,
            'total_likes': review.likes.count(),
            'total_dislikes': review.dislikes.count()
        }, status=status.HTTP_200_OK)

    except Rating.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)


model = SentenceTransformer("all-MiniLM-L6-v2")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    content = request.data.get('content')
    similarity_threshold = 0.7

    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        global model
        new_question_embedding = model.encode(content, convert_to_numpy=True)

        existing_questions = Question.objects.all()

        suggested_questions = []
        for existing_question in existing_questions:
            existing_embedding = model.encode(existing_question.question, convert_to_numpy=True)
            similarity = np.dot(new_question_embedding, existing_embedding) / (
                np.linalg.norm(new_question_embedding) * np.linalg.norm(existing_embedding)
            )

            if similarity >= similarity_threshold:
                suggested_questions.append({
                    'id': existing_question.id})
                break

        question = Question.objects.create(asked_by=request.user, question=content)
        serializer = QuestionSerializer(question)

        response_data = {
            'question': serializer.data,
            'suggested_similar_questions': suggested_questions
        }
        return Response(response_data, status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_questions(request):
    questions = Question.objects.all().order_by('-created_at')
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def homepage(request):
    try:
        user = request.user
        all_question_ids = list(Question.objects.values_list('pk', flat=True))
        today = datetime.now().strftime("%Y-%m-%d")  # Format: "YYYY-MM-DD"
        seed(f"{user.id}-{today}")
        random_question_ids = sample(all_question_ids, min(10, len(all_question_ids)))
        random_questions = Question.objects.filter(pk__in=random_question_ids)
        serializer = QuestionSerializer(random_questions, many=True)

        return Response({'random_questions': serializer.data})

    except Exception as e:
        return Response({'error': str(e)}, status=500)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_answer(request):
    global model
    similarity_threshold = 0.7

    question_id = request.query_params.get("id")
    content = request.data.get('content')
    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        question = Question.objects.get(id=question_id)
        existing_answers = Answer.objects.filter(question_replied=question).order_by('-created_at')

        new_answer_embedding = model.encode(content, convert_to_numpy=True)

        parent_answer = None

        for answer in existing_answers:
            existing_embedding = model.encode(answer.content, convert_to_numpy=True)
            similarity = np.dot(new_answer_embedding, existing_embedding) / (
                np.linalg.norm(new_answer_embedding) * np.linalg.norm(existing_embedding)
            )

            if similarity >= similarity_threshold:
                parent_answer = answer
                break

        answer = Answer.objects.create(answered_by=request.user, question_replied=question, content=content, parent_answer=parent_answer)

        thread = answer.get_conversation_thread()
        serializer = AnswerSerializer(thread, many=True)

        return Response({
            'new_answer': AnswerSerializer(answer).data,
            'conversation_thread': serializer.data
        }, status=status.HTTP_201_CREATED)

    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_answers(request):
    question_id = request.query_params.get("id")
    try:
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question_replied=question).annotate(
            net_score=Count('upvote_answer') - Count('downvote_answer')
        ).order_by('-net_score', '-created_at')

        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_answers_stacked(request):
    question_id = request.query_params.get("id")
    try:
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question_replied=question, parent_answer__isnull=True).order_by('-created_at')

        conversation_threads = []
        for answer in answers:
            thread = answer.get_conversation_thread()
            conversation_threads.append({
                'stack': AnswerSerializer(thread, many=True).data
            })

        return Response(conversation_threads)

    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reply(request):
    answer_id = request.query_params.get("id")
    content = request.data.get('content')
    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        answer = Answer.objects.get(id=answer_id)
        reply = Reply.objects.create(replied_by=request.user, answer=answer, content=content)
        serializer = ReplySerializer(reply)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Answer.DoesNotExist:
        return Response({'error': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_replies(request):
    answer_id = request.query_params.get('id')
    try:
        answer = Answer.objects.get(id=answer_id)
        replies = Reply.objects.filter(answer=answer).order_by('-created_at')
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)
    except Answer.DoesNotExist:
        return Response({'error': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)


"""@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_question(request):
    question_id = request.query_params.get('id')
    question = get_object_or_404(Question, id=question_id)
    action = request.data.get('action')

    if action not in ['upvote', 'downvote']:
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    if action == 'upvote':
        if request.user in question.downvote_question.all():
            question.downvote_question.remove(request.user)
        question.upvote_question.add(request.user) if request.user not in question.upvote_question.all() else question.upvote_question.remove(request.user)
    else:
        if request.user in question.upvote_question.all():
            question.upvote_question.remove(request.user)
        question.downvote_question.add(request.user) if request.user not in question.downvote_question.all() else question.downvote_question.remove(request.user)

    return Response({'message': f'Question {action}d successfully!', 'total_upvotes': question.upvote_question.count(), 'total_downvotes': question.downvote_question.count()}, status=status.HTTP_200_OK)"""


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def vote_answer(request):
    answer = get_object_or_404(Answer, id=request.data.get('id'))
    action = request.data.get('action')
    if action not in ['upvote', 'downvote']:
        return Response({'error': 'Invalid action'}, status=status.HTTP_400_BAD_REQUEST)

    if action == 'upvote':
        if request.user in answer.downvote_answer.all():
            answer.downvote_answer.remove(request.user)
        answer.upvote_answer.add(request.user) if request.user not in answer.upvote_answer.all() else answer.upvote_answer.remove(request.user)
    else:
        if request.user in answer.upvote_answer.all():
            answer.upvote_answer.remove(request.user)
        answer.downvote_answer.add(request.user) if request.user not in answer.downvote_answer.all() else answer.downvote_answer.remove(request.user)

    return Response({'message': f'Answer {action}d successfully!', 'total_upvotes': answer.upvote_answer.count(), 'total_downvotes': answer.downvote_answer.count()}, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def like_dislike_reply(request):
    reply_id = request.query_params.get('id')
    reply = get_object_or_404(Reply, id=reply_id)
    action = request.data.get('action')
    if not reply_id or not action:
        return Response({'error': 'Reply ID and action are required'}, status=status.HTTP_400_BAD_REQUEST)

    if action not in ['like', 'dislike']:
        return Response({'error': 'Invalid action. Use "like" or "dislike".'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        if action == 'like':
            if request.user in reply.dislikes.all():
                reply.dislikes.remove(request.user)
            reply.likes.add(request.user)
        elif action == 'dislike':
            if request.user in reply.likes.all():
                reply.likes.remove(request.user)
            reply.dislikes.add(request.user)

        return Response({
            'message': f'Review {action}d successfully!',
            'reply_id': reply.id,
            'total_likes': reply.likes.count(),
            'total_dislikes': reply.dislikes.count()
        }, status=status.HTTP_200_OK)

    except Reply.DoesNotExist:
        return Response({'error': 'Review not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def question_notification(request):
    question_id = request.query_params.get("id")
    noti = request.data.get('notification')

    try:
        question = Question.objects.get(id=question_id)

        if request.method == "POST":
            if noti.lower() == 'yes':
                notify, created = Notification.objects.get_or_create(user=request.user, defaults={'notify': True}, question=question)
            return Response({
                "message": f"Notification {'updated' if not created else 'set'} for question {question.id}"
            }, status=status.HTTP_200_OK)

        elif request.method == "GET":
            notifications = Notification.objects.filter(question=question, user=request.user)

            serializer = NotificationSerializer(notifications, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
    except Question.DoesNotExist:
        return Response({'error': 'Question does not exist'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def notify_user(request):
    data = []
    for notification in Notification.objects.filter(user=request.user, notify=True):
        question = Question.objects.get(id=notification.question.id)
        answer = Answer.objects.filter(question=question)
        if answer.created_at >= notification.created_at:
            data.append({question: 'A question you are interested in has been answered'})

    return Response(data, status=status.HTTP_200_OK)
