# Job Portal Application

## Overview

This is a Django-based job portal web application that connects employers with job seekers. The platform allows employers to post job listings (subject to admin approval) and job seekers to browse and apply for positions. The system includes role-based dashboards, application tracking, and an admin interface for managing job postings and applications.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

### Framework & Technology Stack

**Problem:** Need a robust web framework for building a job portal with user authentication, database management, and admin capabilities.

**Solution:** Django 5.2.7 as the core web framework with Python.

**Rationale:** Django provides built-in authentication, ORM, admin interface, and follows the MVT (Model-View-Template) architectural pattern. It accelerates development with batteries-included philosophy while maintaining security best practices.

### Authentication & User Management

**Problem:** Different user types (employers vs job seekers) require distinct permissions and workflows.

**Solution:** Custom User model extending Django's AbstractUser with a `user_type` field to differentiate between employers and job seekers.

**Key Design Decisions:**
- Single user table with role discrimination via `user_type` field (choices: 'employer', 'jobseeker')
- Helper methods (`is_employer()`, `is_jobseeker()`) for role checking
- Additional fields: phone number and company_name (optional, for employers)
- Role-based redirects after login/registration to appropriate dashboards

**Alternatives Considered:** Separate employer and job seeker models were considered but rejected to avoid complexity and maintain simpler authentication flow.

### Application Structure

**Problem:** Organize business logic into maintainable, modular components.

**Solution:** Django apps pattern with two main apps:

1. **accounts app** - Handles user authentication, registration, and login/logout
2. **jobs app** - Manages job postings, applications, and dashboards

**Rationale:** Separation of concerns makes the codebase maintainable. Each app has clearly defined responsibilities and can be developed/tested independently.

### Job Posting Workflow

**Problem:** Need to balance moderation with immediate job visibility.

**Solution:** Auto-approval system with three-state tracking:
- `approved` (default) - Jobs are immediately visible to job seekers upon posting
- `pending` - Can be manually set by admins for review
- `rejected` - Admin-rejected jobs

**Key Features:**
- Jobs are auto-approved by default for immediate visibility
- Only approved jobs appear in public listings and search results
- Employers can view all their postings regardless of status
- Admin bulk actions for managing job status (approve/reject)
- Admin can still moderate jobs post-publication if needed

**Design Change (October 2025):** Changed from pending-first to auto-approval to improve employer experience and reduce friction in job posting workflow.

### Application Management

**Problem:** Track job applications through various stages of the hiring process.

**Solution:** Five-state application status system:
- `submitted` - Initial application state
- `under_review` - Employer reviewing the application
- `shortlisted` - Candidate selected for next round
- `rejected` - Application declined
- `accepted` - Candidate hired

**Workflow:**
- Job seekers submit applications with resume upload and cover letter
- Employers view applicants and update status via dropdown
- Status changes tracked with timestamps
- Prevents duplicate applications (one per job per user)

### Data Models

**User Model:**
- Extends AbstractUser
- Fields: user_type, phone, company_name
- Supports both employer and job seeker profiles

**Job Model:**
- Fields: title, description, location, job_type, category, salary range, requirements, status
- Foreign key to employer (User)
- Timestamps for created_at and updated_at
- Ordered by creation date (newest first)

**Application Model:**
- Foreign keys to Job and User (applicant)
- Resume file upload field
- Cover letter text field
- Status tracking
- Applied timestamp

### Search & Filtering

**Problem:** Job seekers need to find relevant positions quickly.

**Solution:** Multi-criteria search form with:
- Keyword search (title and description)
- Location filter
- Category filter
- Job type filter (full-time, part-time, contract, internship)
- Pagination (10 jobs per page)

**Implementation:** Django Q objects for complex queries with optional filters applied conditionally.

### Frontend Architecture

**Problem:** Create a responsive, user-friendly interface.

**Solution:** Server-side rendered templates with Bootstrap 5.

**Key Components:**
- Base template with navigation (role-aware menu items)
- Enhanced form layouts with clear error display
- Message framework for user feedback
- Responsive design using Bootstrap grid
- Form rendering with helpful placeholders and hints
- Dynamic status badges with color coding

**UI/UX Improvements (October 2025):**
- Registration and login forms enhanced with clear titles ("Create Your Account", "Welcome Back")
- Prominent error display using Bootstrap alert classes
- Field-level validation feedback with `is-invalid` and `invalid-feedback` classes
- Helpful placeholder text and hints for all form fields
- Job posting form redesigned with responsive 2-column layout
- Better visual hierarchy with card shadows and spacing
- novalidate attribute to prevent browser validation conflicts

**Pros:** Simple deployment, no separate frontend build process, works without JavaScript
**Cons:** Limited interactivity, full page reloads for updates

### File Upload Handling

**Problem:** Store and serve resume files securely.

**Solution:** Django's FileField with upload_to='resumes/' configuration.

**Configuration:** Media files served during development via DEBUG mode settings. Production deployments would require proper static file serving (e.g., cloud storage).

### Admin Interface

**Problem:** Provide administrators with tools to manage the platform.

**Solution:** Customized Django admin with:
- Custom UserAdmin for viewing user types and roles
- JobAdmin with bulk approval/rejection actions
- ApplicationAdmin with status update actions
- List filters, search fields, and display customization

### URL Routing

**Structure:**
- `/accounts/` - Authentication routes (login, register, logout)
- `/` - Public job listing and search
- `/job/<id>/` - Job detail pages
- `/apply/<id>/` - Application submission
- `/post-job/` - Job posting form (employers only)
- `/employer-dashboard/` - Employer job management
- `/jobseeker-dashboard/` - Application tracking
- `/job/<id>/applicants/` - View applicants (employers only)
- `/application/<id>/update-status/` - Update application status

### Security Considerations

**Implemented:**
- Django's CSRF protection on all forms
- Login required decorators for protected views
- Role-based access control (employers can't apply, job seekers can't post)
- File upload validation via Django FileField

**Note:** SECRET_KEY is exposed in settings.py (development only). Production deployments require environment variable configuration.

## External Dependencies

### Core Framework
- **Django 5.2.7** - Web framework providing ORM, authentication, admin interface, and template engine

### Frontend
- **Bootstrap 5.3.0** - CSS framework loaded via CDN for responsive UI components
- No JavaScript framework dependencies (vanilla JS only for Bootstrap interactions)

### Database
- **SQLite** - Default Django database (implied by lack of database configuration)
- Database schema managed through Django migrations
- Note: Production deployments typically require PostgreSQL or MySQL

### File Storage
- **Local file system** - Resume storage in media/resumes/ directory
- Configured via Django's MEDIA_ROOT and MEDIA_URL settings

### No External APIs
- No third-party API integrations
- No payment gateways
- No email service configuration (would need SMTP setup for notifications)
- No cloud storage integration (local file storage only)

### Python Dependencies
- Standard Django dependencies (included with Django installation)
- No additional Python packages required beyond Django itself