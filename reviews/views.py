from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReviewForm
from .email_utils import (
    send_student_thank_you,
    send_admin_notification
)
def home(request):
    return render(request, 'home.html')
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
            try:
                send_student_thank_you(review)
                print("Student email sent successfully.")
            except Exception as e:
                print("Student email error:", e)
            try:
                send_admin_notification(review)
                print("Admin notification sent successfully.")
            except Exception as e:
                print("Admin email error:", e)
            return redirect('thank_you')
        messages.error(
            request,
            'Please correct the errors in the form.'
        )
    else:
        form = ReviewForm()
    return render(
        request,
        'review_form.html',
        {'form': form}
    )
def thank_you(request):
    return render(request, 'thank_you.html')