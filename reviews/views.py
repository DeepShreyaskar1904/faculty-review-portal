from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReviewForm
from .email_utils import send_student_thank_you, send_admin_notification
from .sentiment_utils import analyze_sentiment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
def home(request):
    return render(request, 'home.html')
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            # Create review object without saving yet
            review = form.save(commit=False)
            # Analyze student's written feedback
            review.sentiment = analyze_sentiment(
                review.feedback
            )
            # Save review with sentiment
            review.save()
            print(f"Sentiment detected: {review.sentiment}")
            # Send email to student
            try:
                send_student_thank_you(review)
                print("Student email sent successfully.")
            except Exception as e:
                print("Student email error:", e)
            # Send notification to admin
            try:
                send_admin_notification(review)
                print("Admin notification sent successfully.")
            except Exception as e:
                print("Admin email error:", e)
            # Redirect after successful submission
            return redirect('thank_you')
        else:
            messages.error(
                request,
                'Please correct the errors in the form.'
            )
    else:
        form = ReviewForm()
    return render(request,'review_form.html',{'form': form})
def thank_you(request):
    return render(request, 'thank_you.html')
def admin_login(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin_dashboard')
        logout(request)
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_dashboard')
        messages.error(request,'Invalid admin credentials.')
    return render(request,'admin_login.html')
@login_required(login_url='admin_login')
def admin_logout(request):
    logout(request)
    return redirect('admin_login')
@login_required(login_url='admin_login')
def admin_dashboard(request):
    if not request.user.is_staff:
        logout(request)
        return redirect('admin_login')
    return render(request,'admin_dashboard.html')