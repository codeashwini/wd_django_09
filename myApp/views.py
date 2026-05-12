from django.http import HttpResponse
from django.shortcuts import render
from course.models import Courses
def home(request):
    # data = {
    #     'name':"Naman",
    #     'email':'aman@gmail.com',
    #     'age':10,
    #     'contact':[9876543210, 8765432190]
    # }
    return render(request, "index.html")

def about(request):
    return render(request, "about.html")

def contact(request):

    data = {}
    try:
        if request.method == 'POST':
            email = request.POST.get('email')
            address1 = request.POST.get('address1')

            data = {
                'email':email,
                'address1':address1
            }
    except:
        pass

    return render(request, "contact.html", {'output':data})


def courses(request):

    course = Courses.objects.all().order_by('course_title')
    
    data = {
        'course_details' : course
    }

    return render(request, 'courses.html', {'data':data})
