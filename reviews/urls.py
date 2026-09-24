from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('review/',views.submit_review,name='submit_review'),
    path('thank-you/',views.thank_you,name='thank_you'),
    path('admin-login/',views.admin_login,name='admin_login'),
    path('admin-logout/',views.admin_logout,name='admin_logout'),
    path('admin-dashboard/',views.admin_dashboard,name='admin_dashboard'),
]