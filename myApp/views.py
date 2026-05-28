# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from course.models import Courses
from notifications.models import NotificationModel
from contact.models import Contact
from UserReg.models import RegUser
from django.contrib.auth.hashers import make_password,check_password
import uuid
from django.core.mail import send_mail

def home(request):

    if 'user_id' not in request.session:
        return redirect("/login/")
    else:
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
    # if 'user_id' not in request.session:
    #     return redirect("/login/")
    # else:
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
        return redirect("/")

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

def user_login(request):

    if request.method == 'POST':
        e = request.POST.get('email') 
        p = request.POST.get('password')
        r = request.POST.get('remember')

        try :
            user = RegUser.objects.get(email = e)
            if check_password(p, user.password):
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name
                if r:
                    request.session.set_expiry(30*24*60*60)
                else:
                    request.session.set_expiry(0)
                if user is not None:
                    return redirect('/profile/')
        except Exception as e:
                return redirect('/login/')  

    return render(request, "login.html")

def user_register(request):

    if request.method == 'POST':
        n = request.POST.get('name')
        e = request.POST.get('email')
        p = request.POST.get('phone')
        c = request.POST.get('course')
        pas = make_password(request.POST.get('password'))
        c_pas = make_password(request.POST.get('confirm_pass'))
        t = request.POST.get('terms')

        u = RegUser(name=n, email=e, course = c, phone=p, password = pas, confirm_pass = c_pas, terms = t)

        u.save()

        return redirect('/login/')

    return render(request, "register.html")

def profile(request):
    if 'user_id' not in request.session:
        return redirect('/login/')
    return render(request, "profile.html")

def logout(request):
    request.session.flush()
    return redirect('/login/')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')

        try:
            user =RegUser.objects.get(email=email)

            token = str(uuid.uuid4())
            user.reset_token = token
            user.save()

            reset_link = f"http://127.0.0.1:8000/reset-password/{token}"

            send_mail(
                subject ='Password Reset',
                message = f"Click the link to reset your password\n {reset_link}",
                from_email = "av01097@gmail.com",
                recipient_list=[email]
            )

            return render(request, 'forgot_password.html', {'msg':'Password reset link sent to your gmail'})

        except Exception as e:
            return render(request, 'forgot_password.html', {'error':'Email not  registered'})
        
    return render(request, 'forgot_password.html')


def reset_passsword(request, token):
    try:
        user = RegUser.objects.get(reset_token = token)

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                return render(request, 'reset_password.html', {'error':'Passwords do not match'})
            
            user.password = make_password(password)
            user.reset_token = None

            user.save()

        return render(request, 'reset_password.html')
    except Exception as e:
        return redirect('/login/')