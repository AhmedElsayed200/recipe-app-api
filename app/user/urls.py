from django.urls import path
from user import views

app_name = 'user'

urlpatterns = [
    path('create/', views.UserCreateView.as_view(), name='create'),
    path('token/', views.TokenCreateView.as_view(), name='token'),
    path('myprofile/', views.ManageUserView.as_view(), name='myprofile'),
]
