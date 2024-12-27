from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Picture, Interior, Rating, Question, Answer, Reply
from .serializers import PictureSerializer, InteriorSerializer, RatingSerializer, QuestionSerializer, AnswerSerializer, ReplySerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator

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

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'message': 'User created successfully', 'token': token.key}, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view_api(request):
    email = request.data.get('email')
    password = request.data.get('password')
    user = authenticate(email=email, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials, please check to make sure the email and/or password is correct'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        token = default_token_generator.make_token(user)

        reset_url = f"https://campuslifetechnologies.com.ng/reset-password/{user.id}/{token}"

        email = EmailMessage(
            subject='Password Reset Request',
            body=f'Please click the link to reset your password: {reset_url}\tIgnore this mail if you did not initiate this process',
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
                        'rating': rating.rating,
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
            # Fetch ratings for all lodges
            ratings = Rating.objects.select_related('picture_rating').all()

            data = {}
            for rating in ratings:
                lodge_name = rating.picture_rating.lodge_name
                if lodge_name not in data:
                    data[lodge_name] = []
                data[lodge_name].append({
                    'rated_by': rating.rated_by.username,
                    'rating': rating.rating,
                    'review': rating.review
                })

            return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def create_rating(request):
    lodge_name = request.data.get('lodge_name')
    rating = request.data.get('rating')
    review = request.data.get('review')
    likes = request.data.get('likes')
    dislikes = request.data.get('dislikes')

    if not lodge_name or not rating or not review:
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Fetch the lodge
        picture = Picture.objects.get(lodge_name=lodge_name)

        # Prevent duplicate ratings
        if Rating.objects.filter(rated_by=request.user, picture_rating=picture).exists():
            return Response({'error': 'You have already rated this lodge'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the new rating
        rating_instance = Rating.objects.create(
            rated_by=request.user,
            picture_rating=picture,
            rating=rating,
            review=review
        )
        return Response({
            'message': 'Rating and review added successfully!',
            'rating': {
                'lodge_name': lodge_name,
                'rating': rating_instance.rating,
                'review': rating_instance.review,
                'rated_by': rating_instance.rated_by.username,
            }
        }, status=status.HTTP_201_CREATED)
    except Picture.DoesNotExist:
        return Response({'error': 'Lodge not found'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_question(request):
    content = request.data.get('content')
    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    question = Question.objects.create(asked_by=request.user, content=content)
    serializer = QuestionSerializer(question)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_questions(request):
    questions = Question.objects.all().order_by('-vote_count', '-created_at')
    serializer = QuestionSerializer(questions, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_answer(request, question_id):
    content = request.data.get('content')
    if not content:
        return Response({'error': 'Content is required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        question = Question.objects.get(id=question_id)
        answer = Answer.objects.create(answered_by=request.user, question=question, content=content)
        serializer = AnswerSerializer(answer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([AllowAny])
def list_answers(request, question_id):
    try:
        question = Question.objects.get(id=question_id)
        answers = Answer.objects.filter(question=question).order_by('-vote_count', '-created_at')
        serializer = AnswerSerializer(answers, many=True)
        return Response(serializer.data)
    except Question.DoesNotExist:
        return Response({'error': 'Question not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_reply(request, answer_id):
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
def list_replies(request, answer_id):
    try:
        answer = Answer.objects.get(id=answer_id)
        replies = Reply.objects.filter(answer=answer).order_by('-created_at')
        serializer = ReplySerializer(replies, many=True)
        return Response(serializer.data)
    except Answer.DoesNotExist:
        return Response({'error': 'Answer not found'}, status=status.HTTP_404_NOT_FOUND)