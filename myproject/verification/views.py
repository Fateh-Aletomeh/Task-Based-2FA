from django.shortcuts import render

# Create your views here.
def task_verification(request):
    return render(request, "verification/task_verification.html")