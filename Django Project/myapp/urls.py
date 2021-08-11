from django.urls import path
from . import views

urlpatterns=[
	path("", views.index, name="index"),
	path("signup/", views.signup, name="signup"),
	path("contact/", views.contact, name="contact"),
	path("login/", views.login, name="login"),
	path("logout/", views.logout, name="logout"),
	path("change_password/", views.change_password, name="change_password"),
	path("forgot_password/", views.forgot_password, name="forgot_password"),
	path("verify_otp/", views.verify_otp, name="verify_otp"),
	path("new_password/", views.new_password, name="new_password"),
	path("profile/", views.profile, name="profile")
]