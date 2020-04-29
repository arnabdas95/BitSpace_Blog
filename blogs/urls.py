from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name='blogs'
urlpatterns = [

    #homepage list of articale
    path('', views.IndexView.as_view(), name='index'),

    #user register,login,logout
    path('signup/', views.signup, name='signup'),
    path('user_logout/', views.user_logout, name='logout'),
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True, template_name='blogs/login.html'),
         name='login'),

    #users can update their account details
    path('account_update/', views.user_profile_Update, name='account_update'),

    #user create delete update post (user specific)
    path('create/', views.ArticleCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.ArticleUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.ArticleDeleteView.as_view(), name='delete'),


    #anybody can view post detail user detail
    path('detail/<int:pk>/', views.ArticleDetailView.as_view(), name='detail'),
    path('user_profile/<int:pk>/', views.UserProfileDetailView.as_view(), name='user_profile'),

    path('search/', views.search, name='search'),


]