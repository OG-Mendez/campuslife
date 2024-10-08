from django.urls import path
from . import views

urlpatterns = [
    path('', views.picture_list, name='picture_list'),
    path('<int:pk>/', views.picture_detail, name='picture_detail'),
]

urlpatterns += [
    path('api/pictures/', views.picture_list_api, name='picture_list_api'),
    path('api/pictures/<int:pk>/', views.picture_detail_api, name='picture_detail_api'),
]