from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ReviewForm
def home(request):
    return render(request, 'home.html')
def submit_review(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save()
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