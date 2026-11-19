from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StudentUser, Course, Note, Rating

@admin.register(StudentUser)
class StudentUserAdmin(UserAdmin):
    list_display = ('email', 'username', 'branch', 'joining_year', 'is_staff')
    list_filter = ('branch', 'joining_year')

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'branch', 'semester', 'is_custom')
    list_filter = ('branch', 'semester', 'is_custom')
    search_fields = ('code', 'title')

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'material_type', 'uploaded_by', 'uploaded_at', 'is_flagged')
    list_filter = ('is_flagged', 'material_type', 'course__branch', 'course__semester')

admin.site.register(Rating)
