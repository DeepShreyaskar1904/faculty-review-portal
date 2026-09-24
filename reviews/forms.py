from django import forms
from .models import Review
class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = [
            'student_name',
            'student_email',
            'course',
            'batch',
            'rating',
            'teaching_quality',
            'communication',
            'practical_knowledge',
            'doubt_solving',
            'feedback',
            'is_anonymous',
        ]
        widgets = {
            'student_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name'
            }),
            'student_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email'
            }),
            'course': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Python / AI & ML'
            }),
            'batch': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. Morning Batch'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-select'
            }),
            'teaching_quality': forms.Select(attrs={
                'class': 'form-select'
            }),
            'communication': forms.Select(attrs={
                'class': 'form-select'
            }),
            'practical_knowledge': forms.Select(attrs={
                'class': 'form-select'
            }),
            'doubt_solving': forms.Select(attrs={
                'class': 'form-select'
            }),
            'feedback': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your honest feedback here...',
                'rows': 5
            }),
            'is_anonymous': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
        }