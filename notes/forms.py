import os
import re
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import StudentUser, Branch, Course, Note

CHANAKYA_EMAIL_REGEX = re.compile(
    r'^[a-z0-9._-]+\.([a-z]{3,5})(\d{2})@chanakyauniversity\.edu\.in$'
)

EMAIL_CODE_TO_BRANCH = {
    'ecs': Branch.EECS, 'eecs': Branch.EECS,
    'cse': Branch.CSE, 'cs': Branch.CSE,
    'csai': Branch.CSAI, 'eai': Branch.CSAI, 'cai': Branch.CSAI,
    'vlsi': Branch.VLSI, 'eve': Branch.VLSI,
    'ece': Branch.ECE,
    'ema': Branch.MECH, 'mae': Branch.MECH, 'mech': Branch.MECH,
    'ecv': Branch.CIVIL, 'ecc': Branch.CIVIL, 'civ': Branch.CIVIL, 'civil': Branch.CIVIL,
    'era': Branch.ROBOTICS, 'rai': Branch.ROBOTICS, 'rob': Branch.ROBOTICS,
    'ebt': Branch.BIOTECH, 'bio': Branch.BIOTECH,
}

BLOCKED_EXTENSIONS = {'.exe', '.bat', '.cmd', '.sh', '.msi', '.scr', '.php', '.cgi', '.dll', '.vbs'}
MAX_UPLOAD_MB = 50


class StudentSignUpForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': 'e.g., manyasreegi.ecs25@chanakyauniversity.edu.in'})
    )
    branch = forms.ChoiceField(
        choices=[c for c in Branch.choices if c[0] != 'COMMON'],
        required=False,
        help_text="Auto-detected from your email (or pick manually if needed)."
    )

    class Meta(UserCreationForm.Meta):
        model = StudentUser
        fields = ('username', 'email', 'registration_id', 'branch')

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        match = CHANAKYA_EMAIL_REGEX.match(email)
        if not match:
            raise forms.ValidationError(
                "Use your official Chanakya University email (e.g., yourname.ecs25@chanakyauniversity.edu.in)."
            )
        branch_code, year_two_digits = match.groups()
        self.parsed_joining_year = 2000 + int(year_two_digits)
        self.detected_branch = EMAIL_CODE_TO_BRANCH.get(branch_code)
        return email

    def clean(self):
        cleaned_data = super().clean()
        detected = getattr(self, 'detected_branch', None)
        chosen = cleaned_data.get('branch')
        if detected:
            cleaned_data['branch'] = detected
        elif not chosen:
            self.add_error('branch', "Please select your branch from the dropdown.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.branch = self.cleaned_data['branch']
        user.joining_year = self.parsed_joining_year
        if commit:
            user.save()
        return user


class NoteUploadForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['title', 'unit', 'material_type', 'tags', 'description', 'file']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Unit 2 Complete Lecture Notes'}),
            'unit': forms.TextInput(attrs={'placeholder': 'e.g., Unit 1 & 2, or All Units'}),
            'tags': forms.TextInput(attrs={'placeholder': 'Optional topics: AVL trees, Dijkstra, sorting'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Brief summary of what this file covers...'}),
        }

    def clean_file(self):
        uploaded_file = self.cleaned_data.get('file')
        if not uploaded_file:
            return uploaded_file
        ext = os.path.splitext(uploaded_file.name)[1].lower()
        if ext in BLOCKED_EXTENSIONS:
            raise forms.ValidationError(f"Executable files ('{ext}') are blocked. Compress into a .zip if sharing code.")
        if uploaded_file.size > MAX_UPLOAD_MB * 1024 * 1024:
            raise forms.ValidationError(f"Maximum file size is {MAX_UPLOAD_MB} MB.")
        return uploaded_file


class CustomCourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['code', 'title']
        widgets = {
            'code': forms.TextInput(attrs={'placeholder': 'e.g., EOE201'}),
            'title': forms.TextInput(attrs={'placeholder': 'e.g., Open Elective Course Title'}),
        }

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()