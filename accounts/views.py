from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from projects.models import Project  # Import Project model
from contact.models import ContactMessage  # Import ContactMessage model
from django.utils import timezone
from datetime import timedelta

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, 'Logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already exists')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'Account created successfully! Please login.')
                return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'accounts/signup.html')

def logout_view(request):
    logout(request)
    messages.success(request, 'Logged out successfully!')
    return redirect('home')

@login_required
def dashboard(request):
    # Get real data from database
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='active').count()
    draft_projects = Project.objects.filter(status='draft').count()
    
    # Get recent projects (last 5)
    recent_projects = Project.objects.order_by('-created_date')[:5]
    
    # Get total views across all projects
    total_views = 0
    for project in Project.objects.all():
        total_views += project.views
    
    # Get recent activity (projects updated in last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_activity = Project.objects.filter(updated_at__gte=week_ago).order_by('-updated_at')[:5]
    
    # Get unread contact messages count
    unread_messages = ContactMessage.objects.filter(is_read=False).count()
    
    # Get popular projects (most viewed)
    popular_projects = Project.objects.order_by('-views')[:3]
    
    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'draft_projects': draft_projects,
        'recent_projects': recent_projects,
        'total_views': total_views,
        'recent_activity': recent_activity,
        'unread_messages': unread_messages,
        'popular_projects': popular_projects,
    }
    
    return render(request, 'accounts/dashboard.html', context)

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render

def home(request):
    return render(request, "base.html")