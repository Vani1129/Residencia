from django.shortcuts import render, redirect


def home(request):
    return render(request, "home/cms/dashboard.html")

# def home(request):
#     return render(request, "templates/cms/includes/main_content.html")
