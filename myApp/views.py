from django.http import HttpResponse
from django.shortcuts import render
from course.models import Courses
from notifications.models import NotificationModel
def home(request):
    data = Courses.objects.all()
    print("This is added")
    # data = {
    #     'name':"Naman",
    #     'email':'aman@gmail.com',
    #     'age':10,
    #     'contact':[9876543210, 8765432190]
    # }
    return render(request, "index.html", {'data':data})

def about(request):
    notifications = NotificationModel.objects.all()
    return render(request, "about.html", {'notifications':notifications})

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


def courseDetail(request, slug):

    courseDetail = Courses.objects.get(course_slug=slug)

    data = {
        'courseDetail':courseDetail
    }

    return render(request, "courseDetail.html", data)


def notification_display(request, slug):

    notificationDetails = NotificationModel.objects.get(notification_slug = slug)

    data = {
        "notificationDetail":notificationDetails
    }

    return render(request, "notification_detail.html",data)