from django.shortcuts import render

def portfolio(request):
    """Home page view"""
    return render(request, 'portfolio/home.html')

def about(request):
    """About page view"""
    return render(request, 'portfolio/about.html')

def projects(request):
    """Projects page view"""
    return render(request, 'portfolio/projects.html')

def contact(request):
    """Contact page view"""
    return render(request, 'portfolio/contact.html')