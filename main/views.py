import re
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User
import bcrypt

# Create your views here.

def index(request):
    return render(request, 'index.html')

#validate and create user
def create_user(request):
    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    #no errors hashpw and create new user with normalized email to all lower
    hashed_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

    new_user = User.objects.create(
        first_name=request.POST['first_name'],
        last_name=request.POST['last_name'],
        email=(request.POST['email']).lower(),
        birth_date=request.POST['birth_date'],
        password=hashed_pw
        )
    request.session['logged_in_user'] = new_user.id
    return redirect('/user_page')

#check for logged in user and render or redirect
def user_page(request):
    if 'logged_in_user' not in request.session:
        return redirect('/')
    
    context = {
    'user': User.objects.get(id=request.session['logged_in_user'])
    }
    return render(request, 'user_page.html', context)

#check for user then confirm password and put user in session
def login(request):
    email=(request.POST['email']).lower()
    users = User.objects.filter(email=email)
    if users:
        logging_user = users[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logging_user.password.encode()):
            request.session['logged_in_user'] = logging_user.id
            return redirect('/user_page')
        else:
            messages.error(request, "Invalid email or password", extra_tags="login")
            return redirect('/')
    messages.error(request, "Invalid email", extra_tags="login")
    return redirect('/')

def logout(request):
    request.session.clear()
    return redirect('/')