from django import forms
from .models import Job, Application

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ['title', 'description', 'location', 'job_type', 'category', 'salary_min', 'salary_max', 'requirements']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
        }

class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={'rows': 5}),
        }

class JobSearchForm(forms.Form):
    search = forms.CharField(required=False, max_length=100, label='Search')
    location = forms.CharField(required=False, max_length=100, label='Location')
    category = forms.CharField(required=False, max_length=100, label='Category')
    job_type = forms.ChoiceField(required=False, choices=[('', 'All Types')] + list(Job.JOB_TYPE_CHOICES))
