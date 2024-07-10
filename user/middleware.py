# # middleware.py
# from django.shortcuts import redirect

# class AuthMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response

#     def __call__(self, request):
#         if not request.user.is_authenticated:
#             return redirect('login')  # Redirect to the login page if the user is not logged in
#         response = self.get_response(request)
#         return response
