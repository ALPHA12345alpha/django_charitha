from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import RegisterForm, UserProfileForm, SimpleLoginForm
from .models import UserProfile
from submissions.models import Submission

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Create user profile automatically
                UserProfile.objects.get_or_create(user=user)
                messages.success(request, f'🎉 Welcome {user.username}! Your account is ready!')
                login(request, user)
                return redirect("home")
            except Exception as e:
                messages.error(request, 'Something went wrong. Please try again.')
        else:
            # Simplify error messages
            for field, errors in form.errors.items():
                for error in errors:
                    if 'password' in field.lower():
                        messages.error(request, 'Password issue: Make sure both passwords match and are at least 4 characters.')
                    elif 'username' in field.lower():
                        messages.error(request, 'Username issue: Pick a different username (this one might be taken).')
                    elif 'email' in field.lower():
                        messages.error(request, 'Email issue: Please enter a valid email address.')
                    else:
                        messages.error(request, f'{error}')
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

def simple_login(request):
    if request.method == 'POST':
        form = SimpleLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.username}! 🎉')
                return redirect('home')
            else:
                messages.error(request, 'Wrong username or password. Try again!')
    else:
        form = SimpleLoginForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    try:
        profile = user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user)
    
    # Get user statistics
    submissions = Submission.objects.filter(user=user)
    solved_problems = submissions.filter(status='AC').values('problem').distinct().count()
    total_submissions = submissions.count()
    
    recent_submissions = submissions.order_by('-created_at')[:10]
    
    context = {
        'profile_user': user,
        'profile': profile,
        'solved_problems': solved_problems,
        'total_submissions': total_submissions,
        'recent_submissions': recent_submissions,
        'is_own_profile': user == request.user
    }
    
    return render(request, 'users/profile.html', context)

@login_required
def edit_profile(request):
    try:
        profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user)
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, '✅ Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'users/edit_profile.html', {'form': form})

def leaderboard(request):
    users = User.objects.annotate(
        solved_count=Count('submission', filter=Q(submission__status='AC'))
    ).order_by('-solved_count', 'username')[:50]
    
    return render(request, 'users/leaderboard.html', {'users': users})

@login_required
@csrf_exempt
def toggle_theme(request):
    if request.method == 'POST':
        try:
            profile = request.user.userprofile
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=request.user)
        
        data = json.loads(request.body)
        theme = data.get('theme', 'light')
        profile.theme = theme
        profile.save()
        
        return JsonResponse({'success': True})
    return JsonResponse({'success': False})