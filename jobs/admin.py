from django.contrib import admin
from .models import Job, Application

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'employer', 'location', 'job_type', 'status', 'created_at']
    list_filter = ['status', 'job_type', 'category', 'created_at']
    search_fields = ['title', 'description', 'location', 'category']
    actions = ['approve_jobs', 'reject_jobs']
    
    def approve_jobs(self, request, queryset):
        queryset.update(status='approved')
        self.message_user(request, f"{queryset.count()} jobs approved successfully.")
    approve_jobs.short_description = "Approve selected jobs"
    
    def reject_jobs(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} jobs rejected.")
    reject_jobs.short_description = "Reject selected jobs"

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_at']
    list_filter = ['status', 'applied_at']
    search_fields = ['applicant__username', 'job__title']
    actions = ['mark_under_review', 'shortlist_applications', 'reject_applications']
    
    def mark_under_review(self, request, queryset):
        queryset.update(status='under_review')
        self.message_user(request, f"{queryset.count()} applications marked under review.")
    mark_under_review.short_description = "Mark as under review"
    
    def shortlist_applications(self, request, queryset):
        queryset.update(status='shortlisted')
        self.message_user(request, f"{queryset.count()} applications shortlisted.")
    shortlist_applications.short_description = "Shortlist selected applications"
    
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')
        self.message_user(request, f"{queryset.count()} applications rejected.")
    reject_applications.short_description = "Reject selected applications"
