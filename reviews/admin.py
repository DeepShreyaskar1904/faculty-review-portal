from django.contrib import admin
from .models import Review
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'student_name',
        'course',
        'rating',
        'sentiment',
        'created_at',
    )
    list_filter = (
        'rating',
        'sentiment',
        'course',
        'created_at',
    )
    search_fields = (
        'student_name',
        'student_email',
        'course',
        'feedback',
    )
    ordering = (
        '-created_at',
    )