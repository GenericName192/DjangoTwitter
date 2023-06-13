from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("profile_list/", views.profileList, name="profileList"),
    path("profile/<int:pk>", views.profile, name="profile"),
    path("login", views.loginUser, name="login"),
    path("logout", views.logoutUser, name="logout"), 
    path("register", views.registerUser, name="register"),
    path("update_user", views.updateUser, name="updateUser"),
    path("meep_like/<int:pk>", views.meepLike, name="meepLike"),  
    path("meep_share/<int:pk>", views.meepShare, name="meepShare"),    
]