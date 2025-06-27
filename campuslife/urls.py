from django.urls import path
from . import views
from drf_spectacular.views import SpectacularSwaggerView, SpectacularAPIView


urlpatterns = [
    path('home', views.picture_list, name='picture_list'),
    path('home/<int:pk>/', views.picture_detail, name='picture_detail'),
    path('signup', views.signup_view, name='signup'),
    path('login', views.login_view, name='login'),
    path('analytics', views.display_accounts, name='analytics')
]

urlpatterns += [
    path('api/pictures/', views.picture_list_api, name='picture_list_api'),
    path('api/pictures/<int:pk>/', views.picture_detail_api, name='picture_detail_api'),
    path('api/signup/', views.signup_view_api, name='signup_view_api'),
    path('api/login/', views.login_view_api, name='login_view_api'),
    path('api/logout/', views.logout_view_api, name='logout'),
    path('api/ratings/', views.ratings, name='rating_api'),
    path('api/create_rating/', views.create_rating, name='create_rating_api'),
    path('api/create_review/', views.create_review, name='create_review_api'),
    path('api/get_room/', views.get_room, name='get_room'),
    path('api/wallet/', views.wallet_balance, name='get_wallet'),
    path('api/fund_account/', views.fund_account, name='fund_account'),
    path('api/make_payment/', views.payment, name='make_payment'),
    path('api/create_agent/', views.create_agent, name='create_agent'),
    path('api/agent_update_vacancy/', views.agent_update_vacancy, name='agent_update_vacancy'),
    path('api/your_rooms/', views.your_rooms, name='your_rooms'),
    path('api/available_rooms/', views.available_rooms, name='available_rooms'),
    path('api/all_rooms/', views.all_rooms, name='all_rooms'),
    path('api/upload_room/', views.upload_room, name='upload_room'),
    path('api/room_earnings/', views.room_earnings, name='room_earnings'),
    path('api/account_details/', views.account_details, name='account_details'),
    path('api/withdraw/', views.withdraw, name='agent_withdraw'),
    path('api/payout_history/', views.payout_history, name='payout_history'),
    path('api/reviews/', views.list_reviews, name='list_reviews_api'),
    path('api/like_review/', views.like_dislike_review, name='like_dislike_review'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/password-reset/', views.password_reset_request, name='password_reset_request'),
    path('api/password-reset-confirm/', views.password_reset_confirm, name='password_reset_confirm'),
    path('api/average_rating/', views.average_rating_for_lodge, name="average_rating")
]


