from django.urls import path
from . import views

urlpatterns = [
    path('home', views.picture_list, name='picture_list'),
    path('home/<int:pk>/', views.picture_detail, name='picture_detail'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login')
]

urlpatterns += [
    path('api/pictures/', views.picture_list_api, name='picture_list_api'),
    path('api/pictures/<int:pk>/', views.picture_detail_api, name='picture_detail_api'),
    path('api/signup/', views.signup_view_api, name='signup_view_api'),
    path('api/login/', views.login_view_api, name='login_view_api'),
    path('api/ratings/', views.ratings, name='rating_api'),
    path('api/create_rating/', views.create_rating, name='create_rating_api')
]


