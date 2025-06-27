import os

from django.shortcuts import render, get_object_or_404, redirect
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from .models import Picture, Interior, Rating, Review, Room, Wallet, Order, Agent, AgentEarning
from .serializers import PictureSerializer, InteriorSerializer,\
    ReviewSerializer, RoomSerializer, WalletSerializer, RoomUploadSerializer, AgentEarningSerializer
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib import messages
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django.db.models import Count, F
from paystackapi.transaction import Transaction


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
@permission_classes([IsAuthenticated])
def get_room(request):
    lodge_id = request.query_params.get('id')
    try:
        picture = Picture.objects.get(id=lodge_id)
        rooms = Room.objects.filter(lodge=picture)
        serializer = RoomSerializer(rooms, many=True)
        response_data = serializer.data
        has_paid = request.session.get(f'viewed_lodge_{lodge_id}', False)

        for room_data in response_data:
            room_data['display'] = has_paid

        return Response(serializer.data)
    except Picture.DoesNotExist:
        return Response({"error": "Picture not found"}, status=status.HTTP_404_NOT_FOUND)
    except Room.DoesNotExist:
        return Response({"error": "No rooms found for this picture"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def wallet_balance(request):
    wallet, created = Wallet.objects.get_or_create(user=request.user, defaults={'point': 0})

    serializer = WalletSerializer(wallet)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def payment(request):
    room_id = request.query_params.get('id')

    coin = Wallet.objects.filter(user=request.user)
    if coin.point > 0:
        coin.point = F('point') - 1
        coin.save()

        request.session[f'viewed_room_{room_id}'] = True
        request.session.modified = True

        room = Room.objects.filter(id=room_id)
        room.agent.wallet = F('point') + 0.5
        room.room_inspection = F('room_inspection') + 1
        room.save()

        return Response("Point deducted, display Info of ", status=status.HTTP_202_ACCEPTED)

    else:
        return Response("please purchase points to view info", status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def fund_account(request):
    amount = int(request.data.get('amount')) * 100
    email = request.user.email
    reference = Transaction.generate_reference()

    try:
        transaction = Transaction.initialize(
            key=os.getenv('PAYSTACK_SECRET_KEY'),
            amount=amount,
            email=email,
            reference=reference,
            callback_url=os.getenv('PAYSTACK_CALLBACK_URL')
        )
        auth_url = transaction['data']['authorization_url']
        Order.objects.create(user=request.user, amount=amount / 100, email=email, reference=reference)
        return Response(auth_url, status=status.HTTP_200_OK)
    except Exception as e:
        error_message = f"Payment initialization failed: {e}"
        return Response(error_message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@csrf_exempt
def payment_callback(request):
    if request.method == 'GET':
        reference = request.GET.get('reference')
        if reference:
            try:
                verification = Transaction.verify(
                    key=os.getenv('PAYSTACK_SECRET_KEY'),
                    reference=reference
                )
                if verification['status'] and verification['data']['status'] == 'success':
                    order = Order.objects.get(reference=reference)
                    order.is_paid = True
                    order.save()
                    transaction_data = verification['data']
                    amount_paid = transaction_data['amount'] / 100

                    wallet = Wallet.objects.filter(user=request.user)
                    wallet.point += amount_paid // 400
                    wallet.save()

                    return Response({'reference': reference})
                else:
                    return Response({'reference': reference, 'reason': verification['data']['gateway_response']})
            except Exception as e:
                error_message = f"Payment verification failed: {e}"
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error_message': 'No reference provided.'})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_agent(request):
    try:
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')
        phone_number = request.data.get('number')

        if not first_name or not last_name or not phone_number:
            return Response("All fields are required", status=status.HTTP_400_BAD_REQUEST)

        if Agent.objects.filter(user=request.user):
            return Response("Please login to your account", status=status.HTTP_403_FORBIDDEN)

        agent = Agent.objects.get_or_create(user=request.user, first_name=first_name, last_name=last_name, phone_number=phone_number)

        return Response(f"Agent created successfully for {agent.first_name}", status=status.HTTP_201_CREATED)

    except Exception as e:
        return Response({"error": f"An error was encountered : {e}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def agent_update_vacancy(request):
    lodge = request.query_params.get("id")
    room_number = request.data.get("number")
    room_type = request.data.get("type")
    room_floor = request.data.get("floor")
    try:
        user = request.user
        agent = Agent.objects.get(user=user)

        if not agent:
            return Response("You do not have an agent account", status=status.HTTP_403_FORBIDDEN)

        lodge_name = Picture.objects.get(id=lodge)

        room, created = Room.objects.get_or_create(
            lodge=lodge_name,
            room=agent.id,
            room_number=room_number,
            room_type=room_type,
            room_floor=room_floor,
        )

        if not created:
            return Response("This lodge already has a vacancy specified for this agent", status=status.HTTP_200_OK)

        emails = ['michaelezechukwu0@gmail.com', 'chinenyedavid781@gmail.com', 'jerrychukwu01@gmail.com']
        for _ in emails:
            email = EmailMessage(
                subject='Agent Vacancy Update',
                body=f'Agent {agent.first_name} {agent.last_name} updated a vacancy for {lodge_name}',
                from_email='info@campuslifetechnologies.com.ng',
                to=[_],
                headers={'Content-Type': 'text/plain'},
            )
            email.send()

        return Response("Vacancy successfully updated", status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Unexpected error: {e}"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def your_rooms(request):
    try:
        user = request.user
        room = Room.objects.filter(room__user=user)

        serializer = RoomSerializer(room, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Unexpected error: {e}"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def available_rooms(request):

    now = timezone.now()
    exp = now - timedelta(days=2)
    room = Room.objects.filter(vacancy_indicator=True, date_created__lt=exp, uploaded=False)

    serializer = RoomSerializer(room, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def all_rooms(request):
    room = Room.objects.all()

    serializer = RoomSerializer(room, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes((MultiPartParser, FormParser))
def upload_room(request):
    lodge = request.query_params.get("lodge")
    room_number = request.query_params.get("number")
    room_image = request.data.get("image")
    room_video = request.data.get("video")

    try:
        agent = Agent.objects.get(user=request.user)
    except Agent.DoesNotExist:
        return Response({"error": "Agent associated with this user not found."}, status=status.HTTP_400_BAD_REQUEST)

    data = {
        "lodge": lodge,
        "number": room_number,
        "image": room_image,
        "video": room_video,
        "agent": agent.id,
        "uploaded": True
    }

    serializer = RoomUploadSerializer(data=data, context={'request': request})
    if serializer.is_valid():
        room = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def account_details(request):
    account_number = request.data.get("number")
    bank_name = request.data.get("bank")
    try:
        agent = Agent.objects.get(user=request.user)
    except Agent.DoesNotExist:
        return Response({"error": "Agent associated with this user not found."}, status=status.HTTP_400_BAD_REQUEST)

    agent.account_number = account_number
    agent.bank_name = bank_name
    agent.save()

    return Response("Updated payment information", status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def room_earnings(request):
    try:
        user = request.user
        room = Room.objects.filter(room__user=user)

        serializer = RoomSerializer(room, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    except Exception as e:
        return Response({"error": f"Unexpected error: {e}"})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    try:
        agent = Agent.objects.get(user=request.user)
        agent_name = agent.first_name
        agent_lastname = agent.last_name
        balance = agent.wallet
        emails = ['michaelezechukwu0@gmail.com', 'chinenyedavid781@gmail.com', 'jerrychukwu01@gmail.com']
        for _ in emails:
            email = EmailMessage(
                subject='Agent Withdrawal Request',
                body=f'Agent {agent_name} {agent_lastname} initiated a withdrawal of amount: {balance}',
                from_email='info@campuslifetechnologies.com.ng',
                to=[_],
                headers={'Content-Type': 'text/plain'},
            )
            email.send()

        return Response("Withdrawal initiated successfully", status=status.HTTP_202_ACCEPTED)

    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def payout_history(request):
    try:
        agent_earnings = AgentEarning.objects.filter(
            agent__user=request.user
        ).order_by("-payout_date")
        serializer = AgentEarningSerializer(agent_earnings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except AgentEarning.DoesNotExist:
        return Response(
            {"error": "No payout history found for this agent."},
            status=status.HTTP_200_OK,
        )
    except Exception as e:
        print(f"Error in payout_history: {e}")
        return Response(
            {"error": "An unexpected error occurred"},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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

        total_raters = Rating.objects.filter(picture_rating_id=lodge_id).count()

        return Response({
            'lodge_id': lodge_id,
            'lodge_name': lodge_name,
            'average_rating': round(average, 1) if average else None,
            'total_raters': total_raters
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
