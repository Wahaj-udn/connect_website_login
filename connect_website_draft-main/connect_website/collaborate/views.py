from django.http import HttpResponse, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegistrationForm, IdeaForm, UserProfileForm
from .models import Idea, UserProfile
from django.contrib.auth.models import User
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from .models import IndividualProfile, BusinessProfile


def home(request):
    return render(request, 'collaborate/index.html')


#@login_required
def collaborate(request):
    ideas = Idea.objects.all()
    filter_keyword = request.GET.get('filter', '')

    if filter_keyword:
        ideas = ideas.filter(title__icontains=filter_keyword)

    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)
            idea.user = request.user
            idea.save()
            return redirect('collaborate')
    else:
        form = IdeaForm()

    return render(request, 'collaborate/collaborate.html', {
        'form': form,
        'ideas': ideas,
        'filter': filter_keyword
    })


#@login_required
def share_idea(request):
    if request.method == 'POST':
        form = IdeaForm(request.POST, request.FILES)
        if form.is_valid():
            idea = form.save(commit=False)  # Create an Idea object but don't save to the database yet
            idea.user = request.user  # Assign the currently logged-in user
            idea.save()  # Now save it
            return redirect('contribute')  # Redirect to your contribution page or success page
    else:
        form = IdeaForm()

    return render(request, 'collaborate\idea.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('collaborate')
        else:
            messages.error(request, "Registration failed. Please try again.")
    else:
        form = UserRegistrationForm()
    return render(request, 'collaborate/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('collaborate')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'collaborate/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'collaborate/profile.html', {'form': form})


#@login_required
def contribute(request):
    ideas = Idea.objects.all()
    return render(request, 'collaborate/contribute.html', {'ideas': ideas})


def projects(request):
    return render(request, 'collaborate/projects.html')


def placeholder_view(request):
    return HttpResponse("<h1>Page Coming Soon!</h1>")


def thankyou(request):
    return render(request, 'collaborate/thankyou.html')


@csrf_exempt
def login_view(request):
    if request.method == "POST":
        user_id = request.POST.get('user-id')
        password = request.POST.get('password')
        role = request.POST.get('role')

        user = authenticate(request, username=user_id, password=password)

        if user is not None:
            # Check if the user has the correct profile based on the role selected
            if role == 'individual':
                if not hasattr(user, 'individualprofile'):
                    messages.error(request, "Invalid role selected for this user.")
                    return redirect('Login')

            elif role == 'business':
                if not hasattr(user, 'businessprofile'):
                    messages.error(request, "Invalid role selected for this user.")
                    return redirect('Login')

            # Log the user in and redirect to the appropriate portal
            login(request, user)
            if role == 'individual':
                return redirect(reverse('individual_view'))
            elif role == 'business':
                return redirect(reverse('private'))

        else:
            messages.error(request, "Invalid username or password.")
            return redirect('Login')

    return render(request, 'registration/login.html')


@csrf_exempt
def signup(request):
    if request.method == "POST":
        account_type = request.POST.get('account-type')
        username = request.POST.get('userid')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if User.objects.filter(username=username).exists():
            messages.error(request, "User ID already exists.")
            return redirect(reverse('signup'))

        # Create user and save profile based on account type
        try:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()

            if account_type == 'individual':
                name = request.POST.get('name')
                age = request.POST.get('age')
                occupation = request.POST.get('occupation')

                # Save Individual profile
                IndividualProfile.objects.create(
                    user=user,
                    name=name,
                    age=age,
                    occupation=occupation
                )
            
            elif account_type == 'business':
                company_name = request.POST.get('companyname')
                sector = request.POST.get('sector')
                location = request.POST.get('location')
                contact = request.POST.get('contact')

                # Save Business profile
                BusinessProfile.objects.create(
                    user=user,
                    company_name=company_name,
                    sector=sector,
                    location=location,
                    contact_info=contact
                )

            messages.success(request, "Account created successfully. Please log in.")
            return redirect(reverse('Login'))
        except Exception as e:
            messages.error(request, "There was an error creating your account.")
            print(e)  # Log the error for debugging

    return render(request, 'registration/signup.html')


def individual(request):
    # Page for individual users
    return render(request, 'registration/individual.html')

def individual_view(request):
    user = request.user
    individual_profile = None
    business_profile = None

    # Check if the user has a profile
    if hasattr(user, 'individualprofile'):
        individual_profile = user.individualprofile
    elif hasattr(user, 'businessprofile'):
        business_profile = user.businessprofile

    # Prepare context data
    context = {
        'user': user,
        'individual_profile': individual_profile,
    }
    return render(request, 'registration/individual.html', context)

def private(request):
    # Page for business owners
    return render(request, 'registration/private.html')

def private_view(request):
    user = request.user
    business_profile = getattr(user, 'businessprofile', None)

    if business_profile is None:
        messages.error(request, "No business profile found for this user.")
        return redirect('Login')

    # Prepare context data
    context = {
        'user': user,
        'business_profile': business_profile,
    }
    return render(request, 'registration/private.html', context)

def index2(request):
    return render(request, 'collaborate/index2.html')