from django.shortcuts import render, get_object_or_404


# Create your views here.
def index(request):
    return render(request, 'index.html')



#----------------------------------------------------------------------------------------------------------------------------


# Job Seeker Registration View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import RegisterForm, LoginForm, JobSeekerForm
from .models import CustomUser, JobSeeker


# Unified Registration View
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

# Unified Login View (for both HR and Job Seeker)
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.role == 'jobseeker':
                    return redirect('jobseeker_dashboard')  # Redirect to Job Seeker dashboard
                elif user.role == 'hr':
                    return redirect('hr_dashboard')  # Redirect to HR dashboard
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid credentials'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})




from django.contrib.auth import logout
from django.shortcuts import redirect

# Logout view
def logout_view(request):
    logout(request)
    return redirect('index')  # After logout, redirect to login page





#---------------------------------------------------------------------------------------------------------------

def jobseeker_dashboard(request):
    return render(request, 'jobseeker_dashboard.html')

from django.contrib.auth.decorators import login_required
from django.shortcuts import render

@login_required
def hr_dashboard(request):
    # Ensure the user is an HR user
    if request.user.role != 'hr':
        return redirect('career')  # Redirect if not an HR user

    return render(request, 'hr_dashboard.html')






#------------------------------------------careerpageview-----------------------------------------------------------



from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages

# Dummy data for open positions
open_positions = [
    {'title': 'Python Developer', 'location': 'Kochi', 'description': 'We are looking for a skilled Python developer to join our team.'},
    {'title': 'Full Stack Developer', 'location': 'Chennai', 'description': 'Looking for a full stack developer with knowledge of React and Django.'},
]

@login_required
def career(request):
    # Check if the user is HR
    if request.user.role == 'hr':
        messages.info(request, "As an HR, you can view the job positions below, but you cannot apply.")
        return render(request, 'open_positions.html', {'positions': open_positions, 'can_apply': False})

    # If the user is a job seeker, render with apply links enabled
    return render(request, 'open_positions.html', {'positions': open_positions, 'can_apply': True})



#---------------------apply----------------------------------------------------------------------------------------
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import JobSeekerForm
from .utils import extract_text_from_resume, \
    extract_resume_details  # Assuming these are utility functions for resume parsing


@login_required
def apply(request):
    if request.user.role == 'hr':
        # Show an error message if the user is an HR and tries to apply
        messages.error(request, "HR users cannot apply for jobs.")
        return redirect('career')

    elif request.user.role == 'jobseeker':
        if request.method == 'POST':
            form = JobSeekerForm(request.POST, request.FILES)
            if form.is_valid():
                job_seeker = form.save(commit=False)
                job_seeker.user = request.user
                job_seeker.applied_position = request.POST.get('applied_position')

                # Get the uploaded resume
                resume = request.FILES.get('resume')
                if resume:
                    # Try to extract text and details from the resume
                    try:
                        resume_text = extract_text_from_resume(resume)  # Read resume content as text
                        extracted_details = extract_resume_details(resume_text)  # Extract details using regex

                        # Populate job seeker model with form and extracted details
                        job_seeker.full_name = request.POST.get('full_name')  # From form
                        job_seeker.email = extracted_details.get("email")  # From regex extraction
                        job_seeker.phone = extracted_details.get("phone")  # From regex extraction
                        job_seeker.skills = ', '.join(extracted_details.get("skills", []))  # From regex extraction
                        job_seeker.experience = extracted_details.get("experience")  # From regex extraction

                        # Save the job seeker details to the database
                        job_seeker.save()

                        # Show a success message
                        messages.success(request, "Your application has been submitted successfully.")
                        return redirect('jobseeker_dashboard')

                    except Exception as e:
                        # Show an error message if there's an issue processing the resume
                        messages.error(request, f"An error occurred while processing the resume: {str(e)}")
                else:
                    # Show an error message if no resume is uploaded
                    messages.error(request, "Please upload a resume.")
        else:
            # If not POST, create an empty form
            form = JobSeekerForm()

        # Render the form page with any messages (success or error)
        return render(request, 'apply.html', {'form': form})


#-------------------------------------hr dashboard candidate--------------------------------------------------------




@login_required
def candidates(request):
    # Check if the user is HR
    if request.user.role != 'hr':
        return redirect('career')  # Redirect if not an HR user

    # Fetch all candidates from the database
    candidates_list = JobSeeker.objects.all()

    return render(request, 'candidates.html', {'candidates': candidates_list})


#--------------------------------------------regex--------------------------------------------------------------

from .models import JobSeeker
from .utils import extract_resume_details, extract_text_from_resume  # Ensure this matches your file structure
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required


@login_required
def candidate_detail(request, candidate_id):
    candidate = get_object_or_404(JobSeeker, id=candidate_id)

    # Check if the candidate has uploaded a resume
    if candidate.resume:
        # Read the resume file content
        resume_text = extract_text_from_resume(candidate.resume)

        # Extract details using regex
        resume_details = extract_resume_details(resume_text)  # Pass the extracted text to the regex function
    else:
        resume_details = {
            'name': 'No name detected',
            'phone': 'No phone detected',
            'email': 'No email detected',
            'skills': ['No skills detected'],
            'experience': ['No experience detected']
        }

    return render(request, 'candidate_detail.html', {
        'candidate': candidate,
        'resume_details': resume_details
    })
