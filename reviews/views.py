from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReviewForm
from .email_utils import send_student_thank_you, send_admin_notification
from .sentiment_utils import analyze_sentiment
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .google_auth import create_google_flow
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.db.models import Avg, Count, Q
from django.core.paginator import Paginator
from .models import Review
from django.http import JsonResponse
import requests
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

    # Only staff/admin can access
    if not request.user.is_staff:
        logout(request)
        return redirect('admin_login')

    # ==========================================
    # ALL REVIEWS
    # ==========================================

    all_reviews = Review.objects.all().order_by('-created_at')


    # ==========================================
    # DASHBOARD OVERALL STATISTICS
    # ==========================================

    total_reviews = all_reviews.count()

    total_students = (
        all_reviews
        .values('student_email')
        .distinct()
        .count()
    )

    average_rating = all_reviews.aggregate(
        avg_rating=Avg('rating')
    )['avg_rating']

    if average_rating is None:
        average_rating = 0


    # ==========================================
    # SENTIMENT STATISTICS
    # ==========================================

    positive_count = all_reviews.filter(
        sentiment='positive'
    ).count()

    neutral_count = all_reviews.filter(
        sentiment='neutral'
    ).count()

    negative_count = all_reviews.filter(
        sentiment='negative'
    ).count()


    # ==========================================
    # RATING STATISTICS
    # ==========================================

    rating_counts = []

    for rating in range(1, 6):

        count = all_reviews.filter(
            rating=rating
        ).count()

        rating_counts.append(count)


    # ==========================================
    # SEARCH
    # ==========================================

    search_query = request.GET.get(
        'search',
        ''
    ).strip()

    if search_query:

        all_reviews = all_reviews.filter(

            Q(student_name__icontains=search_query)
            |
            Q(student_email__icontains=search_query)
            |
            Q(course__icontains=search_query)
            |
            Q(batch__icontains=search_query)
            |
            Q(feedback__icontains=search_query)

        )


    # ==========================================
    # COURSE FILTER
    # ==========================================

    selected_course = request.GET.get(
        'course',
        ''
    ).strip()

    if selected_course:

        all_reviews = all_reviews.filter(
            course=selected_course
        )


    # ==========================================
    # RATING FILTER
    # ==========================================

    selected_rating = request.GET.get(
        'rating',
        ''
    ).strip()

    if selected_rating:

        all_reviews = all_reviews.filter(
            rating=selected_rating
        )


    # ==========================================
    # SENTIMENT FILTER
    # ==========================================

    selected_sentiment = request.GET.get(
        'sentiment',
        ''
    ).strip()

    if selected_sentiment:

        all_reviews = all_reviews.filter(
            sentiment=selected_sentiment
        )


    # ==========================================
    # COURSE LIST FOR FILTER
    # ==========================================

    courses = (
        Review.objects
        .values_list('course', flat=True)
        .distinct()
        .order_by('course')
    )


    # ==========================================
    # PAGINATION
    # ==========================================

    paginator = Paginator(
        all_reviews,
        10
    )

    page_number = request.GET.get(
        'page'
    )

    reviews_page = paginator.get_page(
        page_number
    )


    # ==========================================
    # CONTEXT
    # ==========================================

    context = {

        # Overall statistics
        'total_reviews': total_reviews,
        'total_students': total_students,
        'average_rating': round(
            average_rating,
            2
        ),

        'positive_count': positive_count,
        'neutral_count': neutral_count,
        'negative_count': negative_count,

        'rating_counts': rating_counts,


        # Reviews
        'recent_reviews': reviews_page,


        # Filters
        'courses': courses,

        'search_query': search_query,

        'selected_course': selected_course,

        'selected_rating': selected_rating,

        'selected_sentiment': selected_sentiment,

    }

    return render(
        request,
        'admin_dashboard.html',
        context
    )
@login_required(login_url='admin_login')
def review_detail(request, review_id):
    if not request.user.is_staff:
        logout(request)
        return redirect('admin_login')

    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        return JsonResponse(
            {'error': 'Review not found.'},
            status=404
        )

    return JsonResponse({
        'id': review.id,
        'student_name': review.student_name,
        'student_email': review.student_email,
        'course': review.course,
        'batch': review.batch,
        'rating': review.rating,
        'teaching_quality': review.teaching_quality,
        'communication': review.communication,
        'practical_knowledge': review.practical_knowledge,
        'doubt_solving': review.doubt_solving,
        'sentiment': review.sentiment,
        'feedback': review.feedback,
        'is_anonymous': review.is_anonymous,
        'created_at': review.created_at.strftime('%d %b %Y, %I:%M %p'),
    })
@login_required(login_url='admin_login')
def review_detail(request, review_id):

    # Only logged-in staff/admin
    if not request.user.is_staff:
        logout(request)
        return redirect('admin_login')

    try:

        review = Review.objects.get(
            id=review_id
        )

    except Review.DoesNotExist:

        return JsonResponse(
            {
                'error': 'Review not found.'
            },
            status=404
        )

    return JsonResponse({

        'id': review.id,

        'student_name':
            review.student_name,

        'student_email':
            review.student_email,

        'course':
            review.course,

        'batch':
            review.batch,

        'rating':
            review.rating,

        'teaching_quality':
            review.teaching_quality,

        'communication':
            review.communication,

        'practical_knowledge':
            review.practical_knowledge,

        'doubt_solving':
            review.doubt_solving,

        'sentiment':
            review.sentiment,

        'feedback':
            review.feedback,

        'is_anonymous':
            review.is_anonymous,

        'created_at':
            review.created_at.strftime(
                '%d %b %Y, %I:%M %p'
            ),

    })
def google_login(request):
    flow = create_google_flow()
    authorization_url, state = flow.authorization_url(
        prompt="select_account",
        access_type="online"
    )
    request.session["google_oauth_state"] = state
    request.session["google_code_verifier"] = flow.code_verifier
    return redirect(authorization_url)
def google_callback(request):

    # Get saved OAuth state
    saved_state = request.session.pop(
        "google_oauth_state",
        None
    )

    # Get saved PKCE verifier
    code_verifier = request.session.pop(
        "google_code_verifier",
        None
    )

    if not saved_state:
        messages.error(
            request,
            "Google authentication session expired. Please try again."
        )
        return redirect("forgot_password")

    if not code_verifier:
        messages.error(
            request,
            "Google security verification failed. Please try again."
        )
        return redirect("forgot_password")

    try:

        # Check OAuth state
        returned_state = request.GET.get("state")

        if returned_state != saved_state:
            raise ValueError("OAuth state mismatch.")

        # Get authorization code
        authorization_code = request.GET.get("code")

        if not authorization_code:
            raise ValueError("Authorization code missing.")

        # Exchange authorization code for Google tokens
        token_response = requests.post(
            "https://oauth2.googleapis.com/token",

            data={
                "code": authorization_code,
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI,
                "grant_type": "authorization_code",
                "code_verifier": code_verifier,
            },

            timeout=20
        )

        print("Google token status:", token_response.status_code)

        if not token_response.ok:
            print("Google token response:", token_response.text)

            raise ValueError(
                "Google token exchange failed."
            )

        token_data = token_response.json()

        # ID token should be present
        google_id_token = token_data.get("id_token")

        if not google_id_token:
            raise ValueError(
                "Google ID token was not returned."
            )

        # Verify ID token
        google_user = id_token.verify_oauth2_token(
            google_id_token,
            google_requests.Request(),
            settings.GOOGLE_CLIENT_ID,
            clock_skew_in_seconds = 60
        )

    except Exception as e:

        print("================================")
        print("GOOGLE AUTH ERROR:", repr(e))
        print("================================")

        messages.error(
            request,
            "Google authentication failed."
        )

        return redirect("forgot_password")

    # Google email
    google_email = google_user.get(
        "email",
        ""
    ).strip().lower()

    # Google email verification
    email_verified = google_user.get(
        "email_verified",
        False
    )

    # Admin email from .env
    admin_email = settings.ADMIN_EMAIL.strip().lower()

    if not email_verified:

        messages.error(
            request,
            "Google email is not verified."
        )

        return redirect("forgot_password")

    # Make sure Google account belongs to admin
    if google_email != admin_email:

        messages.error(
            request,
            "This Google account is not authorized for admin recovery."
        )

        return redirect("forgot_password")

    # Google verification successful
    request.session["google_verified_for_reset"] = True

    return redirect("reset_password")
def forgot_password(request):
    return render(request, 'forgot_password.html')

def reset_password(request):

    if not request.session.get('google_verified_for_reset'):
        messages.error(
            request,
            'Please verify your Google account first.'
        )
        return redirect('forgot_password')

    if request.method == 'POST':

        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if password != confirm_password:
            messages.error(
                request,
                'Passwords do not match.'
            )
            return render(
                request,
                'reset_password.html'
            )

        try:
            validate_password(password)

        except ValidationError as e:
            messages.error(
                request,
                ' '.join(e.messages)
            )
            return render(
                request,
                'reset_password.html'
            )

        try:

            admin_user = User.objects.get(
                email__iexact=settings.ADMIN_EMAIL,
                is_staff=True
            )

            admin_user.set_password(password)
            admin_user.save()

            request.session.pop(
                'google_verified_for_reset',
                None
            )

            messages.success(
                request,
                'Password reset successfully. Please login with your new password.'
            )

            return redirect('admin_login')

        except User.DoesNotExist:

            messages.error(
                request,
                'Admin account not found.'
            )

            return redirect('forgot_password')

    return render(request, 'reset_password.html')