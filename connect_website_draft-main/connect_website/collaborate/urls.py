from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('collaborate/', views.collaborate, name='collaborate'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('contribute/', views.contribute, name='contribute'),
    path('projects/', views.projects, name='projects'),
    path('profile/', views.profile, name='profile'),
    path('share_idea/', views.share_idea, name='share_idea'),
    path('thankyou/', views.thankyou, name='thankyou'),
    path('about/', views.placeholder_view, name='about'),
    path('milestones/', views.placeholder_view, name='milestones'),
    path('contact/', views.placeholder_view, name='contact'),
    path('login_view', views.login_view, name = 'Login'),
    path('signup', views.signup, name = 'signup'),
    path('individual', views.individual, name = 'individual'),
    path('private', views.private, name = 'private'),
    path('individual_view', views.individual_view, name = 'individual_view'),
    path('private_view', views.private_view, name = 'private_view'),
    path('index2', views.index2, name = 'index2'),
]

