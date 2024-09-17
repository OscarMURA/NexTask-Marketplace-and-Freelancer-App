from django.shortcuts import render

# Create your views here.
def createProject(request):
    return render(request, 'Projects/createProject.html')
