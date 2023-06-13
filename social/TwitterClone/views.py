from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Profile, Meeps
from .forms import MeepFrom, SignUpForm, ProfilePicForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


# Create your views here.
def home(request):
    if request.user.is_authenticated:
        follows = [x.id for x in (request.user.profile.follows.all())]
        form = MeepFrom(request.POST or None)
        if request.method == "POST":
            if form.is_valid():
                meep = form.save(commit=False)
                meep.user = request.user
                meep.save()
                messages.success(request, ("Meep posted"))
                return redirect("home")
        meeps = Meeps.objects.all().order_by("-createdAt")
        return render(request, "TwitterClone/home.html", {"meeps": meeps, "form": form, "followsList": follows})
    else:
        return render(request, "TwitterClone/home.html", {})

def profileList(request):
    if request.user.is_authenticated:
        profiles = Profile.objects.exclude(user=request.user) # everyone but the user making the request
        return render(request, "TwitterClone/profileList.html", {"profiles": profiles})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("login")
    
def profile(request, pk):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user_id=pk)
        meeps = Meeps.objects.filter(user_id=pk).order_by("-createdAt")

        if request.method == "POST":
            currentUserProfile = request.user.profile
            action = request.POST["follow"]
            if action == "unfollow":
                currentUserProfile.follows.remove(profile)
            elif action == "follow":
                currentUserProfile.follows.add(profile)
            currentUserProfile.save()
        return render(request, "TwitterClone/profile.html", {"profile": profile, "meeps": meeps})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect(login)  


def loginUser(request):
    if request.user.is_authenticated:
        messages.success(request, ("You are already logged in"))
        return redirect("home")
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username = username, password = password)
        if user is not None:
            login(request, user)
            messages.success(request, ("Login successful"))
            return redirect("home")
        else:
            messages.success(request, ("Login failed, please try again"))
            return redirect("login")
    else:
        return render(request, "TwitterClone/login.html", {})


def logoutUser(request):
    logout(request)
    messages.success(request, ("You have been logged out"))
    return redirect("home")


def registerUser(request):
    form = SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password1"]
            user = authenticate(username = username, password = password)
            login(request,user)
            messages.success(request, ("Account created successfully"))
            return redirect("home")

    return render(request, "TwitterClone/register.html", {"form": form})


def updateUser(request):
    if request.user.is_authenticated:
        currentUser = User.objects.get(id=request.user.id)
        profileUser = Profile.objects.get(user_id = request.user.id)
        profileForm = ProfilePicForm(request.POST or None, request.FILES or None, instance=profileUser)
        userForm = SignUpForm(request.POST or None, request.FILES or None, instance=currentUser) # instance is giving the form all of the data from the user
        if userForm.is_valid() and profileForm.is_valid():
            userForm.save()
            profileForm.save()
            login(request, currentUser)
            messages.success(request, ("User updated"))
            return redirect("home")
        return render(request, "TwitterClone/updateUser.html", {"userForm": userForm, "profileForm": profileForm})
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("login")
    
def meepLike(request, pk):
    if request.user.is_authenticated:
        meep = get_object_or_404(Meeps, id=pk)
        if meep.likes.filter(id = request.user.id):
            meep.likes.remove(request.user)
        else:
            meep.likes.add(request.user)
        return redirect(request.META.get("HTTP_REFERER"))
    else:
        messages.success(request, ("You must be logged in to view this page"))
        return redirect("login")
    

def meepShare(request, pk):
        if request.user.is_authenticated:
            meep = get_object_or_404(Meeps, id=pk)
            if meep:
                return render(request, "TwitterClone/shareMeep.html", {"meep": meep})
        else:
            messages.success(request, ("You must be logged in to view this page"))
            return redirect("login")
    