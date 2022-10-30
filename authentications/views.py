"""Authentication views file"""
import os
import random
import string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import redirect, render
from django.contrib import messages
from django.core.mail import send_mail
from django.urls import reverse
from authentications.models import Users
from authentications.forms import LoginForm, UserRegistrationForm, UserForgetPassword,UserForgetPasswordConfirm


def generate_random_text(number):
    """Generating random characters to mumble up the reset link sent"""
    characters = string.ascii_letters + string.digits
    results = "".join(random.choice(characters) for _ in range(number))
    return results

# Create your views here.
def user_login(request):
    """Creating the user login view"""
    if request.method =="POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            clean_data = form.cleaned_data
            user = authenticate(request,email_address = clean_data['email_address'],
            password = clean_data["password"])
            if user is not None:
                login(request,user)
                messages.success(request, "Login Success")
                return redirect("shop:shop")
            else:
                messages.error(request, "Invalid Credentials, Try Again")
                return render(request,"authentications/login.html",{"form":form})
    else:
        form = LoginForm()
    return render(request,"authentications/login.html",{"form":form})

def register(request):
    """User registers view"""
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            clean_data  =form.cleaned_data
            new_user = Users.objects.create_user(
                email_address = clean_data["email_address"],
                password = clean_data["password2"],
                first_name=clean_data["first_name"],
                last_name=clean_data["last_name"],
                phone_number = clean_data["phone_number"])
            new_user.save()
            messages.success(request, "Registration Successful, Please Login")
            return redirect("authentications:login")
    else:
        form = UserRegistrationForm()
    return render(request, "authentications/register.html", {"form": form})

def user_logout(request):
    """USer logout view"""
    logout(request)
    return redirect("shop:shop")


def user_forgot_password(request):
    """Forgotten password view"""
    users = Users.objects
    forget_form = UserForgetPassword()
    if request.method=="POST":
        form = UserForgetPassword(request.POST)
        if form.is_valid():
            clean_email = form.cleaned_data["email_address"]
            try:
                user = users.get(email_address = clean_email)
                messages.success(request, "Password reset instructions sent")
                token_generator =PasswordResetTokenGenerator()
                token = token_generator.make_token(user=user)
                send_mail("Password Reset Instructions",
                f"Password resseting link:{os.getenv('PASSWORD_RESET_HOSTNAME')}authentication/forget-password-confirm/?&si={generate_random_text(50)}&iam={user}&com={generate_random_text(50)}&bus={generate_random_text(50)}&def={token}\n\n\nIf you did not trigger this action, please ignore this Email.\n\n\n Do not share this link with anyone.\n This link can only be used once",
                os.getenv("EMAIL_HOST_USER"), [clean_email])
            except Users.DoesNotExist:
                messages.error(request, "User with email does not exist")
            form.clean()
            return render(request, "authentications/forget_password.html",
            {"forget_form":forget_form})
    else:
        form = UserForgetPassword()
        return render(request, "authentications/forget_password.html",{"forget_form":form})


def user_forgot_pass_confirm(request):
    """Confirm token used to access the user object"""
    user = Users.objects.get(email_address=request.GET["iam"])
    token = request.GET["def"]
    token_generator =PasswordResetTokenGenerator()
    if token_generator.check_token(user,token):
        form = UserForgetPasswordConfirm()
        if request.method =="POST":
            form = UserForgetPasswordConfirm(request.POST)
            if form.is_valid():
                clean_data = form.cleaned_data
                user.set_password(clean_data["new_password"])
                user.save()
                messages.success(request,"Password reset done, please login")
                return redirect(reverse('authentications:login'))
            else:
                form = UserForgetPasswordConfirm
                messages.error(request, "Passwords do not match")
                return render(request, "authentications/forgot_password_confirm.html",
                {"pass_conf":form})

        return render(request, "authentications/forgot_password_confirm.html",{"pass_conf":form})

    else:
        messages.error(request,"Password reset link not valid")
        return redirect(reverse('authentications:login'))
