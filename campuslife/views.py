from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Picture
from .serializers import PictureSerializer
# Create your views here.


def picture_list(request):
    # Get filter parameters
    available_vacancy = request.GET.get('available_vacancy')
    lodge_name = request.GET.get('lodge_name')
    lodge_location = request.GET.get('lodge_location')

    pictures = Picture.objects.all()

    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    # Filter by price range if provided
    if min_price and max_price:
        pictures = pictures.filter(lodge_price__gte=min_price, lodge_price__lte=max_price)

# Apply filters if they exist
    if available_vacancy:
        pictures = pictures.filter(available_vacancy__exact=available_vacancy)

    if lodge_name:
        pictures = pictures.filter(lodge_location__icontains=lodge_name)

    if lodge_location:
        pictures = pictures.filter(name__icontains=lodge_location)

    print(pictures.count())
    return render(request, 'campuslife/picture_list.html', {'pictures': pictures})



def picture_detail(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    return render(request, 'campuslife/picture_detail.html', {'picture': picture})



@api_view(['GET'])
def picture_list_api(request):
    pictures = Picture.objects.all()
    serializer = PictureSerializer(pictures, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def picture_detail_api(request, pk):
    picture = get_object_or_404(Picture, pk=pk)
    serializer = PictureSerializer(picture)
    return Response(serializer.data)
