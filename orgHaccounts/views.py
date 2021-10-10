from django.shortcuts import render, redirect, HttpResponseRedirect
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth import login as OHlogin, authenticate as OHauthenticate, logout as OHlogout
from .forms import RegisterForm, AuthenticationForm, OHUserUpdateForm, UserDeleteForm, FileUploadForm, UserProfileForm
from django.contrib import messages
from .models import FileUpload, User, ScreenAnswer, UserAvatar, VaccineResponse, NewsPost, Comment, Like 

User= get_user_model()

def index(request):
    form = AuthenticationForm
    context={
        'health_condition': 'Covid-19',
        'required_action': 'self screen and report vaccination status',
        'form': form
    }
    if request.method == 'GET':
        return render(request, 'home.html', context)
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = OHauthenticate(email=email, password=password)
            if user is not None and user.is_active:
                OHlogin(request, user)
                return redirect('/dashboard')
        messages.error(request, 'Entered email and/or password incorrect!')
        context = {'form': form}
        return render(request, 'signin.html', context)
def register(request):
    if request.method == 'GET':
        form  = RegisterForm()
        context = {'form': form}
        return render(request, 'signup.html', context)
    if request.method == 'POST':
        form  = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('email')
            messages.success(request, 'An account was succefully created for ' + user)
            return redirect('/login')
        messages.error(request, 'Errors occured while processing your request')
        context = {'form': form}
        return render(request, 'signup.html', context)
    return render(request, 'signup.html', {})
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = OHauthenticate(email=email, password=password)
            if user is not None and user.is_active:
                OHlogin(request, user)
                return redirect('/dashboard')
        messages.error(request, 'Entered email and/or password incorrect!')
        context = {'form': form}
        return render(request, 'signin.html', context)
    form = AuthenticationForm()
    return render(request,'signin.html', {'form':form })
def logout(request):
    OHlogout(request)
    messages.info(request, "You have been successfully logged-out")
    return redirect("/login")

def dashboard(request):
    context = {
    "Welcome": "Welcome!"
    }
    return render(request, 'dashboard/dash.html', context)

def screen(request):
    context = {
        "yes": "Yes",
        "no": "No",
    }
    return render (request, 'dashboard/screen.html', context)
def screened(request):
    if request.method == "POST":
        answer= request.POST['answer']
        user= request.user
        screenAnswer= ScreenAnswer.objects.create(answer=answer, user=user)
        request.session['screenAnswer_id'] = screenAnswer.id
        if answer == 'No':
            messages.success(request, "You are fit to work today!")
            return redirect("/dashboard")
        if answer != 'No':
            messages.success(request, "DO NOT come to the workplace today. Stay home until you report no symptoms")
            return redirect("/dashboard")
        return redirect("/dashboard")

def vaccine_reporting(request):
    if request.method == "GET":
        r= requests.get("https://www.vaccinespotter.org/api/v0/states/WA.json")
        r=r.json()
        features= r['features']
    context={
        "location":features,
        "pfizer": "Pfizer-BioNTech",
        "moderna": "Moderna",
        "janssen": "Johnson & Johnson’s Janssen",
        "unknown": "Unknown",
        "1st": "1st",
        "2nd": "2nd",
        "3rd": "3rd",
    }
    return render (request, 'dashboard/vaccine_report.html', context)
def vreported(request):
    if request.method== "POST":
        vaccine_type= request.POST['vaccine_type']
        vaccine_dose= request.POST['vaccine_dose']
        vaccine_location= request.POST['vaccine_location']
        vaccine_illness= request.POST['vaccine_illness']
        date_received= request.POST['date_received']
        user= request.user
        vaccineResponse= VaccineResponse.objects.create(vaccine_type=vaccine_type, vaccine_dose=vaccine_dose, date_received=date_received, vaccine_location=vaccine_location, vaccine_illness=vaccine_illness, user=user)
        request.session['vaccineResponse_id'] = vaccineResponse.id
        messages.success(request, "You have successfully submitted your report!")
        return redirect("/dashboard")
def file_upload(request, user_id):
    if request.method == 'GET':
        user= request.user
        form  = FileUploadForm()
        context = {
            'form': form,
            'user': user,
            }
        return render (request, 'dashboard/files.html', context)
    if request.method=="POST":
        user=request.user
        form  = FileUploadForm(request.POST, request.FILES)
        context= {
            "form":form
        }
        if form.is_valid():
            file= FileUpload(file=request.FILES['file'], user=user)
            file.save()
        messages.success(request, "File successfully uploaded!")
        return redirect(f"/file_upload/{ user_id}")
    messages.error(request, 'Errors occured while processing your request')
    form  = FileUploadForm()
    context = {'form': form}
    return render (request, 'dashboard/files.html', context)

def profile(request, user_id):
    user= request.user
    form= UserProfileForm()
    if request.method == "GET":
        context={
            "history": "Personal Information",
            "health_condition": "Covid-19",
            "user": user,
            "form": form
        }
        return render(request, 'dashboard/profile.html', context)
    if request.method=="POST":
        form= UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            updated_avatar = form.clean_avatar.get('avatar')
            user.avatar= updated_avatar
            messages.success(request, 'The picture was successfully updated for ' + user)
            return redirect(f"/profile/{ user_id }")
    messages.error(request, 'Errors occured while processing your request')
    form  = UserProfileForm()
    context = {'form': form}
    return render (request, 'dashboard/profile.html', context)
def profile_update(request, user_id):
    user= request.user
    data = {'email': user.email,'date_of_birth': user.date_of_birth, 'avatar': user.avatar}
    if request.method == 'GET':
        user=user
        form= OHUserUpdateForm(initial=data)
        context = {
            'form': form,
            'user': user
        }
        return render(request, 'dashboard/editPersonalinfo.html', context)
    if request.method=="POST":
        form  = OHUserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            updated_user = form.cleaned_data.get('email')
            user = updated_user
            messages.success(request, 'The account was successfully updated for ' + updated_user)
            return redirect(f"/profile/{ user_id }")
        messages.error(request, 'Errors occured while processing your profile-update request')
        form  = OHUserUpdateForm(initial=data)
        context = {
            'form': form,
        }
        return render(request, 'dashboard/editPersonalinfo.html', context)
    return render(request, 'dashboard/editPersonalinfo.html', {})

def delete_profile(request, user_id):
    if request.method == 'POST':
        form = UserDeleteForm(request.POST)
        user = request.user
        user.delete()
        messages.info(request, 'Your account has been deleted.')
        return redirect('/')
    else:
        form = UserDeleteForm(instance=request.user)
        context = {
            'form': form
        }
        return render(request, 'dashboard/delete_profile.html', context)
def feed(request):
    all_newsPosts= NewsPost.objects.all()
    context={
        "all_newsPosts": all_newsPosts,
    }
    return render(request, 'feed/feedPost.html', context)
def newsPost(request):
    if request.user.is_staff and not None:
        return redirect("/admin/orgHaccounts/newspost/")
    return redirect("/admin/orgHaccounts/newspost/")
def add_newsPost(request):
    if request.session == "POST":
        creator= User.objects.get(id=request.session['user_id'])
        newsPost_description = request.POST['description']
        errors = NewsPost.objects.validate_newsPost(newsPost_description)
        if len(errors) > 0:
            for key, val in errors.items():
                messages.error(request, val)
                return redirect("/newsPost")
        title = request.POST['title']
        intro= request.POST['intro']
        postContent= request.POST['postContent']
        NewsPost.objects.create(intro=intro, title= title, postContent= postContent, description=newsPost_description, creator=creator)
        messages.success(request, "Post successfully created!")
    return redirect ("/feed")
def add_like(request, newsPost_id):
    if request.method == "POST":
        liked_newsPost = NewsPost.objects.get(id=newsPost_id)
        user=request.user
        if user.is_authenticated:
            user_liking = user

            newLike = Like(user=user_liking, newsPost=liked_newsPost)
            newLike.alreadyLiked = True

            liked_newsPost.user_likes.add(user_liking)
            liked_newsPost.likes += 1
            liked_newsPost.save()
            newLike.save()
            return redirect("/feed")
        else:
            messages.success(request, "Signup or login to interact with Updates!")
            return redirect("/login")
    return redirect("/feed")

def add_comment(request, newsPost_id):
    newsPost_comment= request.POST['newsPost_comment']
    user = request.user
    newsPost = NewsPost.objects.get(id=newsPost_id)
    Comment.objects.create(newsPost_comment=newsPost_comment, user=user, newsPost=newsPost)
    return redirect(f'/comments/{ newsPost_id }')

def comments(request, newsPost_id):
    newsPost = NewsPost.objects.get(id=newsPost_id)
    all_comments= Comment.objects.filter(id=newsPost_id)
    context={
        "newsPost": newsPost,
        "all_comments": all_comments,
    }
    return render (request, 'feed/comments.html', context)
def delete_post(request, newsPost_id):
    d = NewsPost.objects.get(id=newsPost_id)
    d.delete()
    return redirect('/feed')
def news_content(request, newsPost_id):
    all_newsPosts = NewsPost.objects.filter(id=newsPost_id)
    context={
        "all_newsPosts": all_newsPosts
    }
    return render(request, 'feed/newsContent.html', context)