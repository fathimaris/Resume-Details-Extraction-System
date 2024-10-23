import re
import pdfplumber  # For PDF files
from docx import Document  # For Word documents


def extract_text_from_resume(file):
    """Extracts text from a PDF or Word document."""
    if file.name.endswith('.pdf'):
        text = ''
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + '\n'
        return text.strip()
    elif file.name.endswith('.docx'):
        doc = Document(file)
        text = '\n'.join([para.text for para in doc.paragraphs])
        return text.strip()
    else:
        raise ValueError("Unsupported file format. Please upload a PDF or Word document.")


def extract_name(resume_text):
    """Extracts the name from the resume text."""
    name_pattern = r'(?:(?:Name\s*[:\-]?\s*|\b)([A-Z][a-zA-Z]*(?:\s+[A-Z][a-zA-Z]*)*))'
    name_match = re.search(name_pattern, resume_text)
    return name_match.group(1).strip() if name_match else 'No name detected'


def extract_phone(resume_text):
    """Extracts the phone number from the resume text."""
    phone_pattern = r'\+?\d[\d -]{9,14}'
    phone_match = re.search(phone_pattern, resume_text)
    return phone_match.group(0).strip() if phone_match else 'No phone detected'


def extract_email(resume_text):
    """Extracts the email from the resume text."""
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    email_match = re.search(email_pattern, resume_text)
    return email_match.group(0).strip() if email_match else 'No email detected'


def extract_skills(resume_text):
    """Extracts skills from the resume text."""
    skills_pattern = r'\b(?:Python|Django|React|JavaScript|HTML|CSS|Java|C\+\+|SQL|PHP|Cybersecurity|MongoDB|Bootstrap|C|jQuery|Visual Studio Code)\b'
    skills_match = re.findall(skills_pattern, resume_text)
    return list(set(skills_match)) if skills_match else ['No skills detected']


import re

import re

import re

import re


def extract_experience(resume_text):
    """Extracts experience titles from the resume text."""

    # Improved pattern to capture the experience section more robustly
    experience_pattern = r'(?i)(?:EXPERIENCE|WORK EXPERIENCE|PROFESSIONAL EXPERIENCE)\s*[:\-]?\s*([\s\S]*?)(?:EDUCATION|PROJECTS|\Z)'

    experience_titles = []

    experience_match = re.search(experience_pattern, resume_text)
    if experience_match:
        exp_text = experience_match.group(1).strip()  # Get the captured group and strip whitespace

        # Debug: Print extracted experience text
        print(f"Extracted Experience Text:\n{exp_text}\n")

        # Split the experience text into lines for individual checks
        exp_lines = exp_text.splitlines()

        # Check for job titles or roles
        for line in exp_lines:
            line = line.strip()
            # Debug: print each line being checked
            print(f"Checking line: '{line}'")
            # Check if the line contains a job title
            if re.search(r'(?i)\b(intern|full stack|developer|engineer|manager)\b', line):
                experience_titles.append(line)

    return experience_titles if experience_titles else ['No experience detected']


# Sample resume text for testing
sample_resume_text = """
College of engineering Cherthala
B. Tech (CSE) - 6.56
2019 - 2023
St Pauls HSS Veliyanad
Higher Secondry - 75%
2017 - 2019
St Pauls HSS Veliyanad
Class 10 - 96%
2016
EDUCATION
OBJECTIVE
Highly motivated and technically skilled Computer Science Engineering graduate, equipped with
strong analytical skills, creativity, and a forward-thinking approach. Seeking to leverage my
academic knowledge, programming skills, and practical experience to contribute to innovative
projects in various fields.
ASHMI P K
+919562489566 ashmipk379@gmail.com in www.linkedin.com/in/ashmi-pk
PROJECTS
Duration : Ongoing Team : Individual
BLOOD BANK
Developed a web-based blood bank management system that connects patients
needing blood transfusions with compatible donors.
This system is designed to significantly reduce wait times in critical situations,
potentially saving lives.
platform: Django, Visual studio
Duration : 8 Months Team : Four
FOOD CALORIE DETECTION- Major Project
This Project sought to determine the calorie intake by the users..
Assisted in coding, testing and debugging applications
platform: YOLOv8, Roboflow, Pycharm
EXPERIENCE
- Acquired a strong foundation in full-stack web development through practical
experience with Python frameworks like Django for backend development
and front-end technologies for user interface creation.
- Actively contributed to the development of independent projects, including a
to-do list and a blood bank management system, demonstrating
strong problem-solving and technical skills.
Technovalley software india pvt ltd Jul 2023 - present
PYTHON FULL STACK INTERN
Arduino, IoT & Raspberry Pi - Quolabs
Foundations of User Experience (UX) Design - Coursera
Crash Course on Python - Coursera
Foundations of Cybersecurity - Coursera
Reverse Coding Competition - IEEE Kochi Hub
Programming Fundamentals - Coursera
INTERNSHIP & CERTIFICATIONS
NSS Volunteer(2020-2022)
IEEE Volunteer(2020-2021)
Actively participated in various college based community service
initiatives organized by NSS and IEEE
EXTRACURRICULAR ACTIVITIES
Dr. Jaya V L - Principal
College of engineering Cherthala
principal@cectl.ac.in
Dr. Priya S - HOD
College of engineering Cherthala
priya@cectl.ac.in
REFERENCE
Duration : 2 Months Team : Four
ONLINE AUCTION SYSTEM- Mini Project
Implementation of Online auction and bidding system for various items.
Worked on the integration of the front-end system.
Platform : MongoDB, Express, Node JS, React JS
Duration : 2 Months Team : Four
MULTIPLE FILE EXTENSION VIEWER- Mini Project
This is an android application designed to open file extensions such as pdf, jpeg, mp3, and so on..
The project focuses on concentrating on enhancement of space efficiency.
Platform: Java, Android Studio
Python
Django
C
ReactJS
Html
CSS
Javascript
MongoDB
SQL
Visual Studio Code
SKILLS
PHP
Bootstrap
jQuery
"""

# Call the function with the sample text
experience_details = extract_experience(sample_resume_text)
print("Experience Details:", experience_details)


def extract_resume_details(resume_text):
    """Extract details from the resume text."""
    return {
        'name': extract_name(resume_text),
        'phone': extract_phone(resume_text),
        'email': extract_email(resume_text),
        'skills': extract_skills(resume_text),
        'experience': extract_experience(resume_text)
    }
