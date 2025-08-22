from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import RegisterForm, UserProfileForm
from .models import UserProfile
from submissions.models import Submission

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'🎉 Your account "{user.username}" has been created successfully! Welcome to Online Judge!')
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, 'Please fix the errors below.')
    else:
        form = RegisterForm()
    return render(request, "registration/register.html", {"form": form})

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