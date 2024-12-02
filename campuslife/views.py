from django.shortcuts import render, get_object_or_404, redirect
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from .models import Picture, Interior, Rating
from .serializers import PictureSerializer, InteriorSerializer, RatingSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.authentication import TokenAuthentication


# Create your views here.


def picture_list(request):
    available_vacancy = request.GET.get('available_vacancy')
    lodge_name = request.GET.get('lodge_name')
    lodge_location = request.GET.get('lodge_location')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    pictures = Picture.objects.all()

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
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

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
    pictures = Picture.objects.all()
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
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        token, _ = Token.objects.get_or_create(user=user)
        return Response({'token': token.key}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def interior_view_api(request):
    interiors = Interior.objects.filter()
    serializer = InteriorSerializer(interiors, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ratings(request):
    if request.method == 'GET':
        # Check if a specific lodge_name is provided
        lodge_name = request.query_params.get('lodge_name')

        if lodge_name:
            # Fetch ratings for the specific lodge
            try:
                picture = Picture.objects.get(lodge_name=lodge_name)
                ratings = Rating.objects.filter(picture_rating=picture)

                data = [
                    {
                        'rated_by': rating.rated_by.username,
                        'rating': rating.rating,
                        'review': rating.review,
                        'lodge_name': picture.lodge_name
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
@permission_classes([IsAuthenticated])
def create_rating(request):
    lodge_name = request.data.get('lodge_name')
    rating = request.data.get('rating')
    review = request.data.get('review')

    if not lodge_name or not rating or not review:
        return Response({'error': 'All fields are required'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        # Validate the rating
        rating = int(rating)
        if rating < 1 or rating > 5:
            return Response({'error': 'Rating must be between 1 and 5'}, status=status.HTTP_400_BAD_REQUEST)
    except ValueError:
        return Response({'error': 'Rating must be an integer'}, status=status.HTTP_400_BAD_REQUEST)

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
