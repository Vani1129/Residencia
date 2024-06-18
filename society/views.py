from django.http import HttpResponse
from django.shortcuts import render, redirect
# from django.contrib.auth import login
# from django.contrib import messages
# from django.contrib.auth import get_user_model
# from django.db import IntegrityError
# from .forms import UserForm, OTPForm
# from .utils import generate_otp
# # import random
# # import string


def home(request):
   return HttpResponse("Welcome to the Society Home Page")

# def register(request):
#     if request.method == 'POST':
#         form = UserForm(request.POST)
#         if form.is_valid():
#             full_name = form.cleaned_data.get('full_name')
#             phone_number = form.cleaned_data.get('phone_number')
#             email = form.cleaned_data.get('email')
#             password = form.cleaned_data.get('password')
#             address = form.cleaned_data.get('address')
#             society_name = form.cleaned_data.get('society_name')
#             type = form.cleaned_data.get('type')
#             UserModel = get_user_model()
#             if UserModel.objects.filter(email=email).exists():
#                 messages.error(request, 'Email already exists. Please use a different email address.')
#             elif UserModel.objects.filter(phone_number=phone_number).exists():
#                 messages.error(request, 'Phone number already exists. Please use a different phone number.')
#             else:
#                 try:
#                     user = UserModel.objects.create_user(
#                         full_name=full_name,
#                         phone_number=phone_number,
#                         email=email,
#                         password=password,
#                         address=address,
#                         society_name=society_name,
#                         type=type,
#                     )
#                     messages.success(request, 'Registration successful. You can now login.')
#                     return redirect('login')
#                 except IntegrityError as e:
#                     print(str(e))  # Print the error message
#                     error_message = str(e)
#                     messages.error(request, f'An error occurred: {error_message}')
#         else:
#             messages.error(request, 'Invalid form data. Please check the provided information.')
#     else:
#         form = UserForm()
#     return render(request, 'registration/register.html', {'form': form})




# def login_view(request):
#     if request.method == 'POST':
#         form = OTPForm(request.POST)
#         if form.is_valid():
#             identifier = form.cleaned_data.get('identifier')
#             otp = form.cleaned_data.get('otp')
            
#             stored_otp = request.session.get('otp')
#             if stored_otp and stored_otp == otp:
#                 UserModel = get_user_model()
#                 try:
#                     user = UserModel.objects.get(email=identifier)
#                 except UserModel.DoesNotExist:
#                     try:
#                         user = UserModel.objects.get(phone_number=identifier)
#                     except UserModel.DoesNotExist:
#                         user = None

#                 if user:
#                     user.backend = 'django.contrib.auth.backends.ModelBackend'
#                     login(request, user)
#                     messages.success(request, 'OTP verification successful.')
#                     return redirect('home')
#                 else:
#                     messages.error(request, 'User not found.')
#             else:
#                 messages.error(request, 'Invalid OTP. Please try again.')
#         else:
#             messages.error(request, 'Invalid form data. Please check the provided information.')
#     else:
#         form = OTPForm()

#     return render(request, 'registration/login.html', {'form': form})

# def admin_dashboard(request):
#     return render(request, 'dashboard.html')

# def send_otp_view(request):
#     if request.method == 'POST':
#         identifier = request.POST.get('identifier')
#         UserModel = get_user_model()
#         try:
#             user = UserModel.objects.get(email=identifier)
#         except UserModel.DoesNotExist:
#             try:
#                 user = UserModel.objects.get(phone_number=identifier)
#             except UserModel.DoesNotExist:
#                 user = None

#         if user:
#             otp = generate_otp()
#             request.session['otp'] = otp
#             # Here, you should send the OTP via email/SMS. For example, you can use Django's send_mail function or an SMS API.
#             print(f"Generated OTP: {otp}")  # Debugging line, should be removed in production
#             messages.success(request, 'OTP sent successfully')
#             return redirect('otp_verify')
#         else:
#             messages.error(request, 'User not found.')
#     return render(request, 'registration/send_otp.html')

# def otp_verify(request):
#     if request.method == 'POST':
#         form = OTPForm(request.POST)
#         if form.is_valid():
#             otp = form.cleaned_data.get('otp')
#             stored_otp = request.session.get('otp')
#             if stored_otp and stored_otp == otp:
#                 messages.success(request, 'OTP verification successful.')
#                 return redirect('registration/login')
#             else:
#                 messages.error(request, 'Invalid OTP. Please try again.')
#         else:
#             messages.error(request, 'Invalid form data. Please check the provided information.')
#     else:
#         form = OTPForm()
#     return render(request, 'registration/otp_verify.html', {'form': form})

