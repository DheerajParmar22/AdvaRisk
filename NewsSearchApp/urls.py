from django.urls import path
from . import views

urlpatterns = [

    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    path('delete_search/<int:search_id>/', views.delete_search, name='delete_search'),


    path('', views.search, name='search'),
    path('results/<int:search_id>/', views.search_results, name='search_results'),
    path('refresh/', views.refresh_results, name='refresh_results'),
]

