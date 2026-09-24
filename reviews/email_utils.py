from django.conf import settings
from django.core.mail import send_mail
def send_student_thank_you(review):

    subject = "Thank You for Your Feedback"

    message = f"""
Hello {review.student_name},

Thank you for taking the time to share your feedback.

Your feedback has been successfully received and will help improve
the teaching and learning experience.

Course: {review.course}
Rating: {review.rating}/5

Thank you again for your valuable response.

Regards,
Deep Shreyaskar
AI/ML Educator & Developer
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[review.student_email],
        fail_silently=False,
    )


def send_admin_notification(review):

    subject = "New Faculty Feedback Received"

    message = f"""
A new student feedback has been submitted.

Student: {review.student_name}
Email: {review.student_email}
Course: {review.course}
Batch: {review.batch}

Overall Rating: {review.rating}/5
Teaching Quality: {review.teaching_quality}/5
Communication: {review.communication}/5
Practical Knowledge: {review.practical_knowledge}/5
Doubt Solving: {review.doubt_solving}/5

Sentiment: {review.sentiment}

Feedback:
{review.feedback}

Submitted:
{review.created_at}

Please login to the Faculty Review Portal to view the complete feedback.
"""

    send_mail(
        subject=subject,
        message=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        fail_silently=False,
    )