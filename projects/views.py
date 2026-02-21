from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import Http404
from .models import Project
from .forms import ProjectForm

def project_list(request):
    """View all projects"""
    projects = Project.objects.all()
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        projects = projects.filter(status=status)
    
    # Search
    search = request.GET.get('search')
    if search:
        projects = projects.filter(title__icontains=search)
    
    paginator = Paginator(projects, 9)  # Show 9 projects per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'projects': page_obj,
        'status_choices': Project._meta.get_field('status').choices,
    }
    return render(request, 'projects/project_list.html', context)

def project_detail(request, slug):
    """View single project"""
    # This will automatically return 404 if project doesn't exist
    project = get_object_or_404(Project, slug=slug)
    
    # Increment view count
    project.views += 1
    project.save()
    
    # Get related projects
    related_projects = Project.objects.filter(
        status='active'
    ).exclude(id=project.id)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'projects/project_detail.html', context)

@login_required
def project_create(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        print("📝 Form submitted!")  # Debug line

        if form.is_valid():
            project = form.save()
            print(f"✅ PROJECT SAVED! ID: {project.id}, Title: {project.title}")
            print(f"📋 Tech Stack: {project.tech_stack}")
            messages.success(request, f'Project "{project.title}" created successfully!')
            return redirect('project-list')  # CHANGED: Now redirects to project list
        else:
            print("❌ Form errors:", form.errors)
    else:
        form = ProjectForm()

    return render(request, 'projects/project_form.html', {
        'form': form,
        'title': 'Add New Project',
        'button_text': 'Create Project',
    })

@login_required
def project_update(request, slug):
    """Update existing project"""
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            messages.success(request, f'Project "{project.title}" updated successfully!')
            return redirect('project-list')  # Also changed this to redirect to project list
    else:
        form = ProjectForm(instance=project)
    
    context = {
        'form': form,
        'project': project,
        'title': f'Edit: {project.title}',
        'button_text': 'Update Project',
    }
    return render(request, 'projects/project_form.html', context)

@login_required
def project_delete(request, slug):
    """Delete project"""
    project = get_object_or_404(Project, slug=slug)
    
    if request.method == 'POST':
        project_title = project.title
        project.delete()
        messages.success(request, f'Project "{project_title}" deleted successfully!')
        return redirect('project-list')
    
    context = {
        'project': project,
    }
    return render(request, 'projects/project_confirm_delete.html', context)

@login_required
def project_dashboard(request):
    """Project management dashboard"""
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='active').count()
    draft_projects = Project.objects.filter(status='draft').count()
    total_views = Project.objects.aggregate(total_views=models.Sum('views'))['total_views'] or 0
    
    recent_projects = Project.objects.order_by('-created_date')[:5]
    popular_projects = Project.objects.order_by('-views')[:5]
    
    context = {
        'total_projects': total_projects,
        'active_projects': active_projects,
        'draft_projects': draft_projects,
        'total_views': total_views,
        'recent_projects': recent_projects,
        'popular_projects': popular_projects,
    }

    return render(request, 'projects/project_dashboard.html', context)