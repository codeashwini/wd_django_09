from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from course.models import Courses
from notifications.models import NotificationModel
from contact.models import Contact
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

    if request.method == 'POST':
        e = request.POST.get('email')
        a = request.POST.get('address1')
        a2 = request.POST.get('address2')
        p = request.POST.get('password')
        c = request.POST.get('city')
        s = request.POST.get('state')
        z = request.POST.get('zip')
        t = request.POST.get('check')

        c = Contact(email=e, password = p,address=a, address2=a2,city=c, state=s, zip=z, terms=t)

        c.save()
        return HttpResponseRedirect("/")

    return render(request, "contact.html")


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

