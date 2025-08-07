from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.db import models
from django.utils import timezone

from datetime import datetime, timedelta

from .forms import SignUpForm
from .models import Book, Rent

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
    

def search_view(request):
    query = request.GET.get('q', '').strip()
    if not query:
        return redirect('home')
    result = Book.objects.filter(
        models.Q(title__icontains=query) | 
        models.Q(author__icontains=query)
    )
    return render(request, "home.html", {"books": result})


def rentBook_view(request, book_id):
    try:
        book = Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        messages.error(request, 'Book not found.')
        return redirect('home')
    
    if request.method == 'POST':
        rental_period = int(request.POST.get('rental_period'))
        return_date = datetime.now() + timedelta(days=rental_period)

        if book.available_copies <= 0:
            messages.error(request, 'No copies available for rent.')
            return redirect('home')

        user = request.user
        if not user.is_authenticated:
            messages.error(request, 'You must be logged in to rent a book.')
            return redirect('home')

        # Create a Rent object
        Rent.objects.create(
            book=book,
            user=user,
            return_date=return_date
        )

        # Decrease the available copies
        book.available_copies -= 1
        book.save()

        messages.success(request, f'You have successfully rented {book.title}.')
        return redirect('home')

    return render(request, "rentBook.html", {"book": book})


def reports_view(request):
    if not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this page.')
        return redirect('home')

    rented_books = Rent.objects.select_related('book', 'user').all()
    available_books = Book.objects.filter(available_copies__gt=0)
    unavailable_books = Book.objects.filter(available_copies=0)

    return render(request, "reports.html", {
        "rented_books": rented_books,
        "available_books": available_books,
        "unavailable_books": unavailable_books,
        'now': timezone.now()

    })


def myRents_view(request):
    returned_rents = Rent.objects.filter(user=request.user, returned=True).select_related('book')
    active_rents = Rent.objects.filter(user=request.user, returned=False).select_related('book')
    return render(request, "myRents.html", {
        "returned_rents": returned_rents,
        "active_rents": active_rents,
        'now': timezone.now()
    })


def returnBook_view(request, rent_id):
    try:
        rent = Rent.objects.get(id=rent_id, user=request.user, returned=False)
    except Rent.DoesNotExist:
        messages.error(request, 'Rent not found.')
        return redirect('myRents')

    # Mark the book as returned
    rent.returned = True
    rent.returned_at = timezone.now()
    rent.save()

    # Increase the available copies of the book
    book = rent.book
    book.available_copies += 1
    book.save()

    messages.success(request, f'You have successfully returned {book.title}.')
    return redirect('myRents')