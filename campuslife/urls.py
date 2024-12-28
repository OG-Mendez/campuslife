from django.urls import path
from . import views
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


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
    path('api/create_rating/', views.create_rating, name='create_rating_api'),
    path('api/create_review/', views.create_review, name='create_review_api'),
    path('api/reviews/', views.list_reviews, name='list_reviews_api'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/password-reset/', views.password_reset_request, name='password_reset_request'),
    path('api/password-reset-confirm/', views.password_reset_confirm, name='password_reset_confirm'),
]


