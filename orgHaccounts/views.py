from django.shortcuts import render, redirect, HttpResponseRedirect
import requests
from django.contrib.auth import get_user_model
from django.contrib.auth import login as OHlogin, authenticate as OHauthenticate, logout as OHlogout
from .forms import RegisterForm, AuthenticationForm
from django.contrib import messages
from .models import FileUpload, User, ScreenAnswer, VaccineResponse

User= get_user_model()

def index(request):
    context={
        'health_condition': 'Covid-19',
        'required_action': 'self screen and report your vaccine status'
    }
    return render(request, 'home.html', context)
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
                # if user.is_active:
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
    return redirect("/")

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
        user= request.user
        vaccineResponse= VaccineResponse.objects.create(vaccine_type=vaccine_type, vaccine_dose=vaccine_dose, vaccine_location=vaccine_location, vaccine_illness=vaccine_illness, user=user)
        request.session['vaccineResponse_id'] = vaccineResponse.id
        messages.success(request, "You have successfully submitted your report!")
        return redirect("/dashboard")
        
def files(request, user_id):
    user= request.user
    all_fileUploads= FileUpload.objects.filter(id=user_id)
    context= {
        "user":user,
        "all_fileUploads":all_fileUploads,
    }
    return render (request, 'dashboard/files.html', context)
def file_upload(request, user_id):
    if request.method=="POST":
        if request.FILES == None:
            messages.info (request, "No docs uploaded!")
        user= request.user
        new_file= FileUpload(file=request.FILES['doc'], user=user)
        request.session['file_id'] = new_file.id
        new_file.save()
        messages.success(request, "File successfully uploaded!")
        return redirect(f"/files/{ user_id}")
    return redirect(f"/files/{ user_id}")

def profile(request, user_id):
    user= request.user
    all_vaccineResponses= VaccineResponse.objects.filter(id=user_id)
    all_screenAnswers= ScreenAnswer.objects.filter(id=user_id)
    context={
        "history": "Personal Information",
        "health_condition": "Covid-19",
        "user": user,
        "all_vaccineResponses": all_vaccineResponses,
        "all_screenAnswers": all_screenAnswers,
    }
    return render(request, 'dashboard/profile.html', context)
def edit_personalInfo(request, user_id):
    user=request.user
    context={
        "user":user
    }
    return render(request, 'dashboard/editPersonalinfo.html', context)
def edited_personalInfo(request, user_id):
    edit_user = request.user
    edit_user.birth_date = request.POST['birth_date']
    edit_user.email = request.POST['email']
    edit_user.save()
    messages.success(request, "Your personal information was successfully updated")
    return redirect(f"/profile/{ user_id }")
def delete_profile(request, user_id):
    d = User.objects.get(id=user_id)
    d.delete()
    return redirect('/')
