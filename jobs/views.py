from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Job, Application
from .forms import JobForm, ApplicationForm, JobSearchForm

def home(request):
    form = JobSearchForm(request.GET)
    jobs = Job.objects.filter(status='approved')
    
    if form.is_valid():
        search = form.cleaned_data.get('search')
        location = form.cleaned_data.get('location')
        category = form.cleaned_data.get('category')
        job_type = form.cleaned_data.get('job_type')
        
        if search:
            jobs = jobs.filter(Q(title__icontains=search) | Q(description__icontains=search))
        if location:
            jobs = jobs.filter(location__icontains=location)
        if category:
            jobs = jobs.filter(category__icontains=category)
        if job_type:
            jobs = jobs.filter(job_type=job_type)
    
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'jobs/home.html', {'page_obj': page_obj, 'form': form})

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, status='approved')
    already_applied = False
    if request.user.is_authenticated and request.user.is_jobseeker():
        already_applied = Application.objects.filter(job=job, applicant=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'already_applied': already_applied})

@login_required
def post_job(request):
    if not request.user.is_employer():
        messages.error(request, 'Only employers can post jobs.')
        return redirect('home')
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.employer = request.user
            job.save()
            messages.success(request, 'Job posted successfully! It will be visible after admin approval.')
            return redirect('employer_dashboard')
    else:
        form = JobForm()
    
    return render(request, 'jobs/post_job.html', {'form': form})

@login_required
def apply_job(request, pk):
    if not request.user.is_jobseeker():
        messages.error(request, 'Only job seekers can apply for jobs.')
        return redirect('home')
    
    job = get_object_or_404(Job, pk=pk, status='approved')
    
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.error(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            messages.success(request, 'Application submitted successfully!')
            return redirect('jobseeker_dashboard')
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def employer_dashboard(request):
    if not request.user.is_employer():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    jobs = Job.objects.filter(employer=request.user)
    return render(request, 'jobs/employer_dashboard.html', {'jobs': jobs})

@login_required
def jobseeker_dashboard(request):
    if not request.user.is_jobseeker():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    applications = Application.objects.filter(applicant=request.user)
    return render(request, 'jobs/jobseeker_dashboard.html', {'applications': applications})

@login_required
def view_applicants(request, pk):
    if not request.user.is_employer():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    job = get_object_or_404(Job, pk=pk, employer=request.user)
    applications = Application.objects.filter(job=job)
    return render(request, 'jobs/view_applicants.html', {'job': job, 'applications': applications})

@login_required
def update_application_status(request, pk):
    if not request.user.is_employer():
        messages.error(request, 'Access denied.')
        return redirect('home')
    
    application = get_object_or_404(Application, pk=pk, job__employer=request.user)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Application.STATUS_CHOICES):
            application.status = status
            application.save()
            messages.success(request, 'Application status updated successfully.')
    
    return redirect('view_applicants', pk=application.job.pk)
