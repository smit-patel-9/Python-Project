from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Submit, User
from django.conf import settings
from django.core.mail import send_mail
import random


# Create your views here.
def index(request):
	return render(request, "index.html")
	# return HttpResponse("Home")

def contact(request):
	if request.method=="POST":
		Submit.objects.create(
				name=request.POST["name"],
				email=request.POST["email"],
				number=request.POST["number"],
				remarks=request.POST["remarks"]
			)
		contact = Submit.objects.all().order_by('-id')[:5]
		msg="Data Insertion Sucessfully."
		return render(request, "contact.html", {"msg" : msg , "contact" : contact})
	else:
		contact = Submit.objects.all().order_by('-id')[:5]
		return render(request, "contact.html", {"contact" : contact})

def signup(request):
	if request.method=="POST":
		email=request.POST["email"]
		try:
			user=User.objects.get(email=email)
			msg="Email-Id Already Registered"
			return render(request, "signup.html", {"msg": msg})
		except:
			if request.POST["password"] == request.POST["cpassword"]:
				User.objects.create(
						fname=request.POST["fname"],
						lname=request.POST["lname"],
						email=request.POST["email"],
						number=request.POST["number"],
						address=request.POST["address"],
						password=request.POST["password"],
						cpassword=request.POST["cpassword"],
						image=request.FILES["image"]
					)
				msg="Data Saved Sucessful"
				return render(request, "login.html", {"msg": msg})
			else:
				msg="Password And Cinfirm Password Does Not Match"
				return render(request, "signup.html" ,{"msg":msg, "class":"danger"})

	else:
		return render(request, "signup.html")

def login(request, msg=""):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST["email"], password=request.POST["password"])
			request.session["email"]=user.email
			request.session["fname"]=user.fname
			request.session["image"]=user.image.url

			return render(request, "index.html")
		except Exception as e:
			msg="Email And Password Does Not Matched"
			return render(request, "login.html", {"msg" : msg, "class":"danger"})
	else:
		return render(request, "login.html")

def logout(request):
	try:
		del request.session["email"]
		del request.session["fname"]
		del request.session["image"]
		return render(request, "login.html")
	except Exception as e:
		return render(request,"login.html")


def change_password(request):
	if request.method=="POST":
		# email=request.session.email['email']
		user=User.objects.get(email=request.session['email'])
		if user.password == request.POST["old_password"]:
			if request.POST["new_password"]==request.POST["cnew_password"]:
				user.password=request.POST["new_password"]
				user.cpassword=request.POST["new_password"]
				user.save()
				msg="Password Sucessfully Change"
				return redirect("logout")
			else:
				msg="New Password And Confirm New Password Does Not Match"
				return render(request, "change_password.html",{"msg":msg, "class":"danger"})
		else:
			msg="Old Password Is Incorrect"
			return render(request, "change_password.html",{"msg":msg, "class":"danger"})
	else:
		return render(request, "change_password.html")


def forgot_password(request):
	if request.method=="POST":
		try:
			user=User.objects.get(email=request.POST["email"])
			otp=random.randint(1000,9999)
			subject = 'OTP For Forgot Password'
			message = "Hello, "+user.fname+" You OTP For Forgot Password Is "+str(otp)+"."
			email_from = settings.EMAIL_HOST_USER
			recipient_list = [user.email, ]
			send_mail( subject, message, email_from, recipient_list )

			return render(request, "otp.html", {"otp":otp , "email":user.email})

		except:
			msg="Email Does Not Exists"
			return render(request, "forgot_password.html", {"msg":msg, "class":"danger"})

	else:
		return render(request, "forgot_password.html")


def verify_otp(request):
	if request.method=="POST":
		otp=request.POST["otp"]
		email=request.POST["email"]
		eotp=request.POST["eotp"]
		if otp == eotp:
			return render(request, "new_password.html",{"email":email})
		else:
			msg="OTP Does Not Match"
			return render(request, "otp.html", {"msg":msg, "class":"danger", "email":email})
	else:
		return render(request, "otp.html")


def new_password(request):
	if request.method=="POST":
		email=request.POST["email"]
		if request.POST["new_password"]==request.POST["cnew_password"]:
			user=User.objects.get(email=request.POST["email"])
			user.password=request.POST["new_password"]
			user.cpassword=request.POST["cnew_password"]
			user.save()

			return redirect("logout")
		else:
			msg="New Pasword And Confirm New Password Does Not Match"
			return render(request, "new_password.html",{"msg":msg, "class":"danger"})

	else:
		return render(request, "new_password.html")

def profile(request):
	user=User.objects.get(email=request.session["email"])
	if request.method=="POST":
		user.fname=request.POST["fname"]
		user.lname=request.POST["lname"]
		user.number=request.POST["number"]
		user.address=request.POST["address"]
		try:
			user.image=request.FILES["image"]
		except:
			pass

		user.save()	

		request.session["email"]=user.email
		request.session["fname"]=user.fname
		request.session["image"]=user.image.url

		msg="Data Sucessfully Update"
		return render(request, "profile.html",{"user":user, "msg":msg, "class": "success"})
	else:	
		return render(request, "profile.html", {"user":user})