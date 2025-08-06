from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages

from .forms import SignUpForm
from .models import Book

User = get_user_model()

# Create your views here.
def home(request):
    books = Book.objects.all()

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user_obj = User.objects.get(username=username)
        except User.DoesNotExist:
            user_obj = None

        if user_obj and not user_obj.is_active:
            messages.error(request, 'Please wait for the admin to verify your account.')
            return redirect('home')

        user = authenticate(request=request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome {user.username}!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
            return redirect('home')
    else:
        return render(request, 'home.html',{'books': books})
    

def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def register_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            form.save()

            #Auth and log in (to be removed later)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            # user = authenticate(username=username, password=password)
            # login(request, user)
            messages.success(request, f'Account created for {username}. Awaiting admin approval.')
            return redirect('home')
        else:
            messages.error(request, 'Error creating account. Please correct the errors below.')
            return render(request, 'register.html', {'form': form})
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})