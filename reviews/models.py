from django.db import models
class Review(models.Model):
    RATING_CHOICES = [
        (1, '1 - Very Poor'),
        (2, '2 - Poor'),
        (3, '3 - Average'),
        (4, '4 - Good'),
        (5, '5 - Excellent'),
    ]

    SENTIMENT_CHOICES = [
        ('positive', 'Positive'),
        ('neutral', 'Neutral'),
        ('negative', 'Negative'),
    ]

    student_name = models.CharField(max_length=150)

    student_email = models.EmailField()

    course = models.CharField(max_length=150)

    batch = models.CharField(
        max_length=100,
        blank=True
    )

    rating = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    teaching_quality = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    communication = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    practical_knowledge = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    doubt_solving = models.PositiveSmallIntegerField(
        choices=RATING_CHOICES
    )

    feedback = models.TextField()

    sentiment = models.CharField(
        max_length=20,
        choices=SENTIMENT_CHOICES,
        default='neutral'
    )

    is_anonymous = models.BooleanField(
        default=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.student_name} - {self.rating}/5"