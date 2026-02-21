from django import forms
from .models import Project

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description', 'tech_stack', 'github_link', 
                 'image', 'created_date', 'is_featured', 'status']
        # REMOVED: full_description, live_demo_link
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-400 focus:outline-none text-white', 'placeholder': 'Enter project title'}),
            'description': forms.Textarea(attrs={'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-400 focus:outline-none text-white', 'rows': 4, 'placeholder': 'Describe your project...'}),
            'tech_stack': forms.TextInput(attrs={'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-400 focus:outline-none text-white', 'placeholder': 'e.g., Python, Django, React'}),
            'github_link': forms.URLInput(attrs={'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-400 focus:outline-none text-white', 'placeholder': 'https://github.com/yourusername/project'}),
            'created_date': forms.DateInput(attrs={'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-400 focus:outline-none text-white', 'type': 'date'}),
            'is_featured': forms.CheckboxInput(attrs={'class': 'h-5 w-5 text-blue-600 bg-gray-700 border-gray-600 rounded'}),
            'status': forms.Select(attrs={'class': 'w-full px-4 py-3 bg-gray-700 border border-gray-600 rounded-lg focus:border-blue-400 focus:outline-none text-white'}),
        }