# from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from course.models import Courses
from notifications.models import NotificationModel
from contact.models import Contact
from UserReg.models import RegUser
from django.contrib.auth.hashers import make_password,check_password
import uuid
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta
from django.conf import settings
import requests

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
                request.session['user_image'] = (user.profile_image.url if user.profile_image else None)

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
    
    user  = RegUser.objects.get(id=request.session['user_id'])

    if request.method == 'POST':
        if request.FILES.get('profile_image'):
            user.profile_image = request.FILES['profile_image']
           
            user.save()
            request.session["user_image"] = user.profile_image.url

    completion_percent = calculate_profile_completion(user)

    return render(request, "profile.html", {'user':user, 'completion':completion_percent})

def logout(request):
    request.session.flush()
    return redirect('/login/')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email')
        captcha_response = request.POST.get('g-recaptcha-response')

        if not captcha_response:
            return render(request, 'forgot_password.html', {
                'error':'Please verify that you are not a robot',
                'site_key':settings.RECAPTCHA_SITE_KEY
            })
        
        captcha_verify_url = 'https://www.google.com/recaptcha/api/siteverify'
        captcha_data = {
            'secret':settings.RECAPTCHA_SECRET_KEY,
            'response':captcha_response
        }

        captcha_result = requests.post(captcha_verify_url, data=captcha_data).json()

        if not captcha_result.get('success'):
            return render(request, 'forgot_password.html', {
                'error':'CAPTCHA verification failed. Try again.',
                'site_key':settings.RECAPTCHA_SITE_KEY
            })

        try:
            user =RegUser.objects.get(email=email)
            now = timezone.now()

            if user.last_reset_request:
                time_diff = now - user.last_reset_request

                if time_diff < timedelta(minutes=30):
                    if user.reset_request_count >=3:
                       return render(request, 'forgot_password.html', {'error':'Too many reset requests. Please try again after 30 minutes'})
                else:
                    user.reset_request_count = 0 

            token = str(uuid.uuid4())
            user.reset_token = token
            user.token_created_at = timezone.now()

            user.reset_request_count += 1
            user.last_reset_request = now

            user.save()

            reset_link = f"http://127.0.0.1:8000/reset-password/{token}"

            send_mail(
                subject ='Password Reset',
                message = f"Click the link to reset your password\n {reset_link}",
                from_email = "av01097@gmail.com",
                recipient_list=[email]
            )

            return render(request, 'forgot_password.html', {'msg':'Password reset link sent to your gmail', 'site_key':settings.RECAPTCHA_SITE_KEY})

        except Exception as e:
            return render(request, 'forgot_password.html', {'error':'Email not  registered', 'site_key':settings.RECAPTCHA_SITE_KEY})
        
    return render(request, 'forgot_password.html', {'site_key':settings.RECAPTCHA_SITE_KEY})


def reset_passsword(request, token):


    try:
        user = RegUser.objects.get(reset_token = token)
        expiry_time = user.token_created_at + timedelta(minutes=15)

        if timezone.now() > expiry_time:
            return render(request, 'reset_password.html', {'error':'Reset link has expired'})

        if request.method == "POST":
            password = request.POST.get('password')
            confirm_password = request.POST.get('confirm_password')

            if password != confirm_password:
                return render(request, 'reset_password.html', {'error':'Passwords do not match'})
            
            user.password = make_password(password)
            user.reset_token = None
            user.token_created_at = None
            user.save()

        return render(request, 'reset_password.html')
    except Exception as e:
        return redirect('/login/')
    

def edit_profile(request):
    if 'user_id' not in request.session:
        return redirect('/login/')
    
    user = RegUser.objects.get(id=request.session['user_id'])

    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')

        if RegUser.objects.filter(email = email).exclude(id=user.id).exists():
            return render(request, 'edit_profile.html', {
                'user':user,
                'error':'Email already in use'
            })
        user.name = name
        user.email = email
        user.save()

        request.session['user_name'] = user.name
        return redirect('/profile/')
    
    return render(request, 'edit_profile.html', {'user':user})

def change_password(request):
    if 'user_id' not in request.session:
        return redirect('/login/')
    
    user = RegUser.objects.get(id=request.session['user_id'])

    if request.method == "POST":
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if not check_password(current_password, user.password):
            return render(request, 'change_password.html', {'error':'Current Password is incorrect'})
        
        if new_password != confirm_password:
            return render(request, 'change_password.html', {'error':'Password and Confirm Password are not same'})
        
        if check_password(new_password,user.password):
            return render(request, 'change_password.html', {'error':'New Password must be different from old password'})
        
        user.password = make_password(new_password)
        user.save()

        return render(request, 'change_password.html', {'success':'Password Changed Successfully'})
    return render(request, 'change_password.html')


def calculate_profile_completion(user):

    fields = [
        user.name,
        user.email,
        user.profile_image,
        user.phone,
    ]

    filled  = sum(1 for field in fields if field)
    total = len(fields)

    return int((filled/total) * 100)
