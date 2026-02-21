from django.urls import path
from . import views

urlpatterns = [
    path('', views.project_list, name='projects'),
    path('', views.project_list, name='project-list'),
    path('create/', views.project_create, name='project-create'),
    path('dashboard/', views.project_dashboard, name='project-dashboard'),
    path('<slug:slug>/update/', views.project_update, name='project-update'),
    path('<slug:slug>/delete/', views.project_delete, name='project-delete'),
    path('<slug:slug>/', views.project_detail, name='project-detail'),

]