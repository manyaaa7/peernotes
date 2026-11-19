from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Count
from .models import Branch, Semester, Course, Note, Rating, MaterialType
from .forms import StudentSignUpForm, NoteUploadForm, CustomCourseForm


def landing_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'notes/landing.html', {
        'total_notes': Note.objects.count(),
        'branches': [b for b in Branch.choices if b[0] != 'COMMON'],
    })


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, f"Welcome to PeerNotes! Branch set to {user.get_branch_display()}.")
            return redirect('dashboard')
    else:
        form = StudentSignUpForm()
    return render(request, 'notes/signup.html', {'form': form})


@login_required
def dashboard(request):
    selected_branch = request.GET.get('branch', request.user.branch)
    selected_sem = request.GET.get('sem', str(request.user.default_semester))
    search_query = request.GET.get('q', '').strip()

    try:
        sem_int = int(selected_sem)
    except ValueError:
        sem_int = request.user.default_semester

    if sem_int in (1, 2):
        courses = Course.objects.filter(
            Q(branch='COMMON') | Q(branch=selected_branch),
            semester=sem_int
        ).annotate(note_count=Count('notes'))
    else:
        courses = Course.objects.filter(
            branch=selected_branch,
            semester=sem_int
        ).annotate(note_count=Count('notes'))

    matching_notes = None
    if search_query:
        matching_notes = Note.objects.filter(
            Q(title__icontains=search_query) |
            Q(tags__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(course__code__icontains=search_query) |
            Q(course__title__icontains=search_query)
        ).select_related('course', 'uploaded_by')

    return render(request, 'notes/dashboard.html', {
        'branches': [b for b in Branch.choices if b[0] != 'COMMON'],
        'semesters': Semester.choices,
        'selected_branch': selected_branch,
        'selected_sem': sem_int,
        'courses': courses,
        'search_query': search_query,
        'matching_notes': matching_notes,
    })


@login_required
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    notes = course.notes.all().select_related('uploaded_by')
    material_filter = request.GET.get('type', '')
    q = request.GET.get('q', '').strip()

    if material_filter:
        notes = notes.filter(material_type=material_filter)
    if q:
        notes = notes.filter(Q(title__icontains=q) | Q(tags__icontains=q) | Q(unit__icontains=q))

    return render(request, 'notes/course_detail.html', {
        'course': course,
        'notes': notes,
        'material_types': MaterialType.choices,
        'selected_type': material_filter,
        'search_query': q,
    })


@login_required
def upload_to_course(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    if request.method == 'POST':
        form = NoteUploadForm(request.POST, request.FILES)
        if form.is_valid():
            note = form.save(commit=False)
            note.course = course
            note.uploaded_by = request.user
            note.save()
            messages.success(request, f"Uploaded to {course.code} - {course.title}!")
            return redirect('course_detail', course_id=course.id)
    else:
        form = NoteUploadForm()
    return render(request, 'notes/upload_note.html', {'form': form, 'course': course})


@login_required
def add_custom_course(request, branch, semester):
    if request.method == 'POST':
        form = CustomCourseForm(request.POST)
        if form.is_valid():
            course, _ = Course.objects.get_or_create(
                code=form.cleaned_data['code'],
                branch=branch,
                semester=semester,
                defaults={'title': form.cleaned_data['title'], 'is_elective': True, 'is_custom': True}
            )
            return redirect('upload_to_course', course_id=course.id)
    else:
        form = CustomCourseForm()
    return render(request, 'notes/add_custom_course.html', {'form': form, 'branch': branch, 'semester': semester})


@login_required
def note_detail(request, note_id):
    note = get_object_or_404(Note.objects.select_related('course', 'uploaded_by'), id=note_id)
    user_rating = Rating.objects.filter(note=note, user=request.user).first()
    is_bookmarked = note.bookmarked_by.filter(id=request.user.id).exists()

    if request.method == 'POST':
        action = request.POST.get('action')
        if action == 'rate':
            score = int(request.POST.get('score', 5))
            if 1 <= score <= 5:
                Rating.objects.update_or_create(note=note, user=request.user, defaults={'score': score})
                messages.success(request, "Rating saved!")
        elif action == 'bookmark':
            if is_bookmarked:
                note.bookmarked_by.remove(request.user)
                messages.info(request, "Removed from bookmarks.")
            else:
                note.bookmarked_by.add(request.user)
                messages.success(request, "Saved to bookmarks!")
        elif action == 'flag':
            note.is_flagged = True
            note.flag_reason = request.POST.get('reason', 'Flagged by student')[:255]
            note.save()
            messages.warning(request, "Flagged for admin review.")
        return redirect('note_detail', note_id=note.id)

    return render(request, 'notes/note_detail.html', {
        'note': note,
        'user_rating': user_rating.score if user_rating else 0,
        'is_bookmarked': is_bookmarked,
    })


@login_required
def profile_dashboard(request):
    return render(request, 'notes/profile.html', {
        'my_uploads': request.user.uploaded_notes.select_related('course').all(),
        'bookmarks': request.user.bookmarked_notes.select_related('course', 'uploaded_by').all(),
    })


@login_required
def delete_note(request, note_id):
    note = get_object_or_404(Note, id=note_id, uploaded_by=request.user)
    if request.method == 'POST':
        course_id = note.course.id
        note.file.delete(save=False)
        note.delete()
        messages.success(request, "Note deleted.")
        return redirect('course_detail', course_id=course_id)
    return render(request, 'notes/confirm_delete.html', {'note': note})