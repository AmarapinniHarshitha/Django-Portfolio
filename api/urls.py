from django.urls import path
from .views import ProjectListAPIView, ProjectDetailAPIView, ContactCreateAPIView

urlpatterns = [
    path('projects/', ProjectListAPIView.as_view(), name='api-projects'),
    path('projects/<slug:slug>/', ProjectDetailAPIView.as_view(), name='api-project-detail'),
    path('contact/', ContactCreateAPIView.as_view(), name='api-contact'),
]
