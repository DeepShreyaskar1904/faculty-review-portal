from django import forms
from .models import *
from django.forms import inlineformset_factory
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

        class FacultyProfileForm(forms.ModelForm):
            class Meta:
                model = FacultyProfile

                fields = [
                    "name",
                    "designation",
                    "profile_image",
                    "short_intro",
                    "about",
                    "location",
                    "email",
                    "students_trained",
                    "teaching_approach",
                    "quote",
                ]

                widgets = {
                    "name": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Enter your name",
                    }),

                    "designation": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Example: AI/ML Educator & Developer",
                    }),

                    "profile_image": forms.ClearableFileInput(attrs={
                        "class": "form-control",
                        "accept": "image/*",
                    }),

                    "short_intro": forms.Textarea(attrs={
                        "class": "form-control",
                        "rows": 3,
                        "placeholder": "Write a short introduction...",
                    }),

                    "about": forms.Textarea(attrs={
                        "class": "form-control",
                        "rows": 5,
                        "placeholder": "Tell students about yourself...",
                    }),

                    "location": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Example: Gujarat, India",
                    }),

                    "email": forms.EmailInput(attrs={
                        "class": "form-control",
                        "placeholder": "Enter your email",
                    }),

                    "students_trained": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Example: 700+",
                    }),

                    "teaching_approach": forms.TextInput(attrs={
                        "class": "form-control",
                        "placeholder": "Example: Learn → Try → Build → Improve",
                    }),

                    "quote": forms.Textarea(attrs={
                        "class": "form-control",
                        "rows": 3,
                        "placeholder": "Enter your quote...",
                    }),
                }
class FacultyProfileForm(forms.ModelForm):

    class Meta:
        model = FacultyProfile

        fields = [
            "name",
            "designation",
            "profile_image",
            "short_intro",
            "about",
            "location",
            "email",
            "students_trained",
            "teaching_approach",
            "quote",
        ]

        widgets = {
            "name": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your name",
            }),

            "designation": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "AI/ML Educator & Developer",
            }),

            "profile_image": forms.ClearableFileInput(attrs={
                "class": "form-control",
                "accept": "image/*",
            }),

            "short_intro": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Write a short introduction...",
            }),

            "about": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5,
                "placeholder": "Tell students about yourself...",
            }),

            "location": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Gujarat, India",
            }),

            "email": forms.EmailInput(attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }),

            "students_trained": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "700+",
            }),

            "teaching_approach": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Learn → Try → Build → Improve",
            }),

            "quote": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 3,
                "placeholder": "Enter your quote...",
            }),
        }
# =========================================================
# EDUCATION FORM
# =========================================================

class EducationForm(forms.ModelForm):

    class Meta:

        model = Education

        fields = [
            "degree",
            "field_of_study",
            "institution",
            "status",
            "start_year",
            "end_year",
            "display_order",
        ]

        widgets = {

            "degree": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "B.Tech / M.Tech / Ph.D."
                }
            ),

            "field_of_study": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "AI & Data Science"
                }
            ),

            "institution": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Institution / University"
                }
            ),

            "status": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Completed / Pursuing"
                }
            ),

            "start_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "2022",
                    "min": "1900",
                    "max": "2100"
                }
            ),

            "end_year": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "2026",
                    "min": "1900",
                    "max": "2100"
                }
            ),

            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "1",
                    "min": "0"
                }
            ),
        }


# =========================================================
# SKILL FORM
# =========================================================

class FacultySkillForm(forms.ModelForm):

    class Meta:

        model = FacultySkill

        fields = [
            "name",
            "display_order",
        ]

        widgets = {

            "name": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Python"
                }
            ),

            "display_order": forms.NumberInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "1",
                    "min": "0"
                }
            ),
        }


# =========================================================
# EDUCATION FORMSET
# =========================================================

EducationFormSet = inlineformset_factory(
    FacultyProfile,
    Education,
    form=EducationForm,
    extra=1,
    can_delete=True
)


# =========================================================
# SKILL FORMSET
# =========================================================

SkillFormSet = inlineformset_factory(
    FacultyProfile,
    FacultySkill,
    form=FacultySkillForm,
    extra=1,
    can_delete=True
)