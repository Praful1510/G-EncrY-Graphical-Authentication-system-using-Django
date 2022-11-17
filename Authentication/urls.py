from django.urls import path
from . import views
urlpatterns = [
    path('',views.home),
    path('join',views.sign),
    path('save-cren',views.save_user_cre),
    path('register',views.register),
    path('sendotp',views.sendotp),
    path('logout',views.logout),
    path('set-password',views.password_redirect),
]