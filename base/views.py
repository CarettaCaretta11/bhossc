import re
# from select import select
import sqlite3
# from tarfile import DEFAULT_FORMAT
# from django.conf import settings
# from django.template import loader
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.http import HttpResponse
from .models import Message, Photos, Room, Topic, User
from .forms import RoomForm, UserForm, MyUserCreationForm
from django.db.models import Q
# from django.contrib.auth.signals import user_logged_in
from django.utils import timezone
# import django.contrib.auth.
from django.core.mail import send_mail
import datetime
from django.utils.timezone import now
from math import floor
from django.utils.timezone import utc
from yoyo1.settings import DEFAULT_FROM_EMAIL
import time, exrex
from django.views.generic import View
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm

def page_not_found_view(request):
    return render(request, 'base/404.html')

def std(sec): # sec_to_days
    w = floor(sec/(3600*24*7))  # weeks
    d = floor((sec - 3600*24*7*w)/(3600*24))  # days
    a = floor((sec - 3600*24*7*w-3600*24*d)/3600)  # hours
    b = floor((sec - 3600*24*7*w-3600*24*d-3600*a)/60)  # minutes
    if sec < 60:
        return "just now"
    elif sec < 3600:
        return f'{b} minutes'
    elif sec < 24*3600:
        return f'{a} hours, {b} minutes' if b != 0 else f'{a} hours'
    elif sec < 24*3600*7:
        return f'{d} days'
    else:
        return f'{w} weeks, {d} days' if d != 0 else f'{w} weeks'

def stds(sec): # sec_to_days_status
    w = floor(sec/(3600*24*7))  # weeks
    d = floor((sec - 3600*24*7*w)/(3600*24))  # days
    a = floor((sec - 3600*24*7*w-3600*24*d)/3600)  # hours
    b = floor((sec - 3600*24*7*w-3600*24*d-3600*a)/60)  # minutes
    if sec < 60:
        return f"{floor(sec)} seconds"
    elif sec < 3600:
        return f'{b} minutes'
    elif sec < 24*3600:
        return f'{a} hours, {b} minutes' if b != 0 else f'{a} hours'
    elif sec < 24*3600*7:
        return f'{d} days'
    else:
        return f'{w} weeks, {d} days' if d != 0 else f'{w} weeks'


# TESTING TESTING TESTING TESTING        
class AjaxHandlerView(View):
    def get(self, request):
        text = request.GET.get('button_text')
        if request.is_ajax():
            t = time.time()
            return JsonResponse({'seconds' : t}, status=200)
        return render(request, 'base/ajax-testing.html')
    def post(self, request):
        card_text = request.POST.get('text')
        if request.is_ajax():
            return JsonResponse({'text' : card_text}, status=200)
        return render(request, 'base/ajax-testing.html')

# class RoomAjaxHandlerView(View):
#     def get(self, request):
#         return render(request, 'base/room.html')
#     def post(self, request):
#         message = Message(user=request.user, room=request.GET.get('room'), body=request.POST.get('body'))
#         message.save()
#         return render(request, 'base/room.html')



# def friendship_alert(request):
#     sender = request.GET.get('sender', None)
#     receiver = request.GET.get('receiver', None)
#     friendship_data = {
#         'sender' : sender,
#         'receiver' : receiver
#     }
#     return JsonResponse(friendship_data)
    
def loginpage(request):
    page = 'az' # just to distinguish this with register_user as both are connected to login_register.html, neither its name nor its value matter
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST': # request.POST - Contains parameters added as part of a POST request. Parameters are enclosed as a django.http.request.QueryDict instance.
        email = request.POST.get('email').strip().lower() # request.POST.get('name',default=None) Gets the value of the name parameter in a POST request or gets None if the parameter is not present. Note default can be overridden with a custom value.
        password = request.POST.get('password')
        if email:
            try:
                user = User.objects.get(email=email)
            except:
                messages.error(request, 'User does not exist !')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            nextt = request.GET.get('next')
            if nextt:
                return redirect(nextt)
            else: return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password!')
    context = {'page': page}
    return render(request, 'base/login_register.html', context)

# a = open('C:\\Users\\kamra\\registration-links.csv')
# b = csv.reader(a)
# c = list(b)

reg = '(\d|[a-z]|[A-Z]){6}(\d|[a-z]|[A-Z]){9}(\d){5}([A-Z]|[a-z]){5}[a-z]{3}(\d|[A-Z]|[a-z]){4}'

generated_links = sqlite3.connect('base/reg_links.sqlite', check_same_thread=False)

def register_user_preliminary(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = str(request.POST.get('email1')).strip()
        if User.objects.filter(email=email).exists():
            return render(request, 'base/httpresponse.html', {'reg_mes': 'A user with this email is already registered!'})
        elif not email.endswith('@bhos.edu.az'):
            return render(request, 'base/httpresponse.html', {'invalid_email':'heyy'})
        else:
            reg_link = f'https://bhossc.onrender.com/{email}' + exrex.getone(reg)
            try:
                generated_links.execute(f"INSERT INTO Reglinks VALUES (?, ?)", (email, reg_link)) # we'll access this link later using the email as a unique key
                generated_links.commit()
                send_mail(subject='Registration', message="Here is your registration link:", from_email=DEFAULT_FROM_EMAIL, recipient_list=[f'{email}'], html_message=f'''
                <p>Here is your registration link:</p><br><a href={reg_link} style="text-decoration:none;display:inline-block;white-space:nowrap;word-break:keep-all;overflow:hidden;text-overflow:ellipsis;background-image:linear-gradient(#05b8ff,#05b8ff);color:#000000;font-size:18px;font-weight:bold;text-align:center;padding:12px 14px;border-radius:48px;background-color:#05b8ff!important">Register</a><br><strong>Do not share it with anyone.</strong>''', fail_silently=False)
                return render(request, 'base/httpresponse.html', {'reg_mes': 'A registration link has been sent to your email address.'})                
            except:
                generated_links.execute(f"UPDATE Reglinks SET reg_link = ? WHERE email = ?", (reg_link, email))
                generated_links.commit()
                send_mail(subject='Registration', message="Here is your registration link:", from_email=DEFAULT_FROM_EMAIL, recipient_list=[f'{email}'], html_message=f'''
                <p>Here is your registration link:</p><br><a href={reg_link} style="text-decoration:none;display:inline-block;white-space:nowrap;word-break:keep-all;overflow:hidden;text-overflow:ellipsis;background-image:linear-gradient(#05b8ff,#05b8ff);color:#000000;font-size:18px;font-weight:bold;text-align:center;padding:12px 14px;border-radius:48px;background-color:#05b8ff!important">Register</a><br><strong>Do not share it with anyone.</strong>''', fail_silently=False)
                return render(request, 'base/httpresponse.html', {'reg_mes': 'A registration link has been sent to your email address.'})
    return render(request, 'base/reg_email.html')

def register_user(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('home')
    abs_path = request.build_absolute_uri()
    email = re.findall(r'.*@bhos.edu.az', abs_path)[0][29:] # if it's https

    the_link = generated_links.execute(f" SELECT reg_link from Reglinks WHERE email = ? ", (email,)).fetchall()[0][0] # CHANGE THIS, THERE'S A MORE EFFICIENT WAY OF PLACING VARIABLES INTO QUERIES

    if abs_path != the_link:
        return render(request, 'base/404.html')
    
    form = MyUserCreationForm()
    if request.method == 'POST':
        if request.build_absolute_uri() != the_link:
            return render(request, 'base/404.html')
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = email.lower()
            user.save()
            login(request, user)
            generated_links.execute("UPDATE Reglinks SET reg_link = '' WHERE email = ?", (email, ))
            generated_links.commit()
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'base/login_register.html', {'form':form})

# def validate_username(request):
#     username = request.GET.get('username', None)
#     data = {
#         'is_taken': User.objects.filter(username__iexact=username).exists()
#     }
#     return JsonResponse(data)

def logout_view(request):
    logout(request)
    return redirect('home')
    
def photocloudinary(request):
    photo = Photos.objects.all()
    return render(request, 'base/photos.html', {'photo': photo})

def home(request):
    # if not request.user.is_authenticated:
    #     return redirect('login')
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    q = request.GET.get('q').strip() if request.GET.get('q') != None else ''
    topics = Topic.objects.all()[0:4]
    lst = 0
    if Topic.objects.filter(name__icontains='Lost items').count() > 0:
        lst = Topic.objects.get(name__icontains='Lost items').room_set.all().count()
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | # if the topic name contains the 'q' input (i in icontains makes it case insensitive : a, A are considered the same)
        Q(name__icontains=q) |
        Q(host__username=q) |
        Q(description__icontains=q))[0:5]
    room_count = Room.objects.filter(
        Q(topic__name__icontains=q) | # if the topic name contains the 'q' input (i in icontains makes it case insensitive : a, A are considered the same)
        Q(name__icontains=q) |
        Q(description__icontains=q)).count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))[0:5]
    context = {'rooms' : rooms, 'topics':topics, 'room_count':room_count, 'room_messages' : room_messages, 'now' : now, 'lst' : lst}
    return render(request, 'base/home.html', context)

@login_required(login_url='/login/')
def room(request, pk):
    try:
        room = Room.objects.get(id=int(pk))
    except:
        return render(request, 'base/404.html')
    room_messages = room.message_set.all().order_by('-created') # room.message_set.all() gives all instances of Messages model (Messages = messages, as it's case insensitive) that belong to this room object 
    participants = room.participants.all()
    if request.method == 'POST' and str(request.POST.get("body")).strip() == '':
        return redirect('room', pk=pk)
    elif request.method == 'POST':
        # if not request.user.confirmed:
        #         return render(request, 'base/httpresponse.html', {'http_response' : 'Your account has not been confirmed!', 'confirm_link' : '1'})
        try:
            form = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body') # see name="body" inside <input> in room.html
            )
            room.participants.add(request.user)
            return redirect('room', pk=pk)
        except ValueError:
            return redirect('login')
    context = {'room' : room, 'room_messages' : room_messages, 
               'participants' : participants}
    return render(request, 'base/room.html', context)

def get_group_name(user1, user2):
    a = 'chat_{}_{}'.format(*sorted([user1.id, user2.id]))
    return str(a)


@login_required(login_url='/login/')
def status_checker(request):
    if request.GET.get('st'):
        User.objects.filter(id=request.user.id).update(last_time_visited = now())
        return JsonResponse({
            'last_time_visited': request.user.last_time_visited,
            'get_time_difference': request.user.get_time_diff(),
            'get_time_difference_minutes': std(request.user.get_time_diff()),
        })

@login_required(login_url='/login/')
def profile_status(request, pk):
    user = User.objects.get(id=pk)
    gtd = user.get_time_diff() # this is being updated by status_checker() every x seconds
    if request.GET.get('a'):
        if gtd <= 30:
            data = {
                'status': 'Online'
            }
        else:
            data = {
                'status': f"{stds(gtd)} ago"
            }
        return JsonResponse(data)

# @login_required(login_url='/login/')
# def friendship_functionalities(request, pk): # covers sending/retracting requests
#     user = User.objects.get(id=pk) # the user who receives the friendship request
#     if request.is_ajax and request.GET.get('a'):
#         if request.user not in user.pending_invs.all():
#             user.pending_invs.add(request.user)
#             data = {
#                 'added': '1'
#             }
#         else:
#             user.pending_invs.remove(request.user)
#             data = {
#                 'added': '2'
#             }
#         return JsonResponse(data)
        

# @login_required(login_url='/login/')
# def retract_friendship_r(request, pk):
#     user = User.objects.get(id=pk) # the user who receives the friendship request
#     if request.is_ajax and request.GET.get('a'):
#         if request.user in user.pending_invs.all():
#             user.pending_invs.remove(request.user)
#             data = {
#                 'added': '2'
#             }
#             return JsonResponse(data)

@login_required(login_url='/login/')
def userprofile(request, pk):
    a = 1
    try:
        user = User.objects.get(id=pk)
    except:
        return redirect('home')
    pm_link = str(get_group_name(request.user, user))
    ltv = user.last_time_visited
    gtd = user.get_time_diff()
    rooms = user.room_set.all()
    room_messages = user.message_set.all()[0:5]
    topics = Topic.objects.all()
    context = {'user': user, 'rooms': rooms, 'topics': topics, 'room_messages' : room_messages, 'ltv': ltv, 'gtd': gtd, 'a' : a, 'pm_link' : pm_link}
    return render(request, 'base/profile.html', context)

# @login_required(login_url='/login/')
# def pm_my_friend(request, pk):
#     user = User.objects.get(id=pk)
#     pm_link = str(get_group_name(request.user, user))
#     return render(request, 'base/profile.html', {})

@login_required(login_url='/login/')
def friends_list(request, pk):
    # if not request.user.confirmed:
    #     return render(request, 'base/httpresponse.html', {'http_response' : 'Your account has not been confirmed!', 'confirm_link' : '1'})
    user = User.objects.get(id=pk)
    frr = user.friends.all()
    a = [get_group_name(user, x) for x in frr]
    zipp = zip(frr, a)
    if request.user not in user.friends.all() and request.user != user:
        return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})
    return render(request, 'base/friends-1.html', {'user' : user, 'zipp' : zipp, 'frr': frr})

@login_required(login_url='/login/')
def friends_list_mobile(request, pk):
    # if not request.user.confirmed:
    #     return render(request, 'base/httpresponse.html', {'http_response' : 'Your account has not been confirmed!', 'confirm_link' : '1'})
    user = User.objects.get(id=pk)
    frr = user.friends.all()[0:9]
    a = [get_group_name(user, x) for x in frr]
    zipp = zip(frr, a)
    if request.user not in user.friends.all() and request.user != user:
        return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})
    return render(request, 'base/friends_mobile.html', {'user' : user, 'zipp' : zipp})

# @login_required(login_url='/login/')
# def sndc(request, pk):
#     user = User.objects.get(id=pk)
#     if request.user == user:
#         if not user.confirmed:
#             send_mail(
#                 'Account verification',
#                 f'Here\'s your verification link\nhttp://{ALLOWED_HOSTS[1]}/request-box/{user.id}/activate/AGiauTDF2D27FT8Vaq76dfHDFu63dfdshs783dtSV63f',
#                 f'{EMAIL_HOST_USER}',
#                 [f'{user.email}'],
#                 fail_silently=False,
#             )
#             return render(request, 'base/httpresponse.html', {'http_response' : f'Check {user.email} for the verification link!'})
#     return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})

# @login_required(login_url='/login/')
# def confirm_a(request, pk):
#     user = User.objects.get(id=pk)
#     if request.user != user:
#         return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})
#     # if user.confirmed:
#     #     return render(request, 'base/httpresponse.html', {'http_response' : 'Your account has already been confirmed!'})
#     user.confirmed = True
#     user.save()
#     return redirect('userprofile', pk=pk)

@login_required(login_url='/login/')
def createroom(request):
    # if not request.user.confirmed:
    #     return render(request, 'base/httpresponse.html', {'http_response' : 'Your account has not been confirmed!', 'confirm_link' : '1'})
    form = RoomForm()
    topics = Topic.objects.all()

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        thumbnail = request.POST.get('thumbnail')
        topic, created = Topic.objects.get_or_create(name=topic_name) # get_or_create() returns a tuple of (object, created), where object is the retrieved or created object and created is a boolean specifying whether a new object was created.
        room = Room(
            host = request.user,
            topic = topic,
            name = request.POST.get('name'),
            description = request.POST.get('description'),
            thumbnail = thumbnail
        )
        room.save()
        return redirect('room', pk=room.id)
             
    context = {'form' : form, 'topics' : topics} # we just need the value part (form in this case, as above: room) {'form':form} means the form variable is recognized as 'form' (without quotation marks) in the template : base/room_form.html
    return render(request, 'base/room_form.html', context)

@login_required(login_url='/login/')
def updateroom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room) # fills the form (actually creates a new form) with the parameters a room already has -- which allows us to edit them and 're-submit'.
    topics = Topic.objects.all()
    if request.user != room.host:
        return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        thumbnail = request.FILES.get("thumbnail")
        if thumbnail:
            room.thumbnail = thumbnail
        room.description = request.POST.get('description')
        room.save()
        return redirect('room', pk=room.id)
    context = {'form' : form, 'topics' : topics, 'room' : room}
    return render(request, 'base/update-room.html', context)

# @login_required(login_url='/login/')
# def updateroom(request, pk):
#     room = Room.objects.get(id=pk)
#     topics = Topic.objects.all()
#     if request.user != room.host:
#         return HttpResponse('Not allowed!')
#     form = RoomForm(instance=room)
#     if request.method == 'POST':
#         form = RoomForm(request.POST, request.FILES, instance=room)
#         if form.is_valid():
#             form.save()
#             return redirect('room', pk=room.id)
#     return render(request, 'base/update-room.html', {'form' : form, 'topics' : topics, 'room' : room})

@login_required(login_url='/login/')
def deleteroom(request, pk): # pk = primary key
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})

    if request.method == 'POST': # means submitting the input (in this case : 'Confirm')
        if Room.objects.filter(topic=room.topic).count() == 1:
            room.topic.delete()
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room}) # value is accessed by the name of the key in the template.

@login_required(login_url='/login/')
def request_box(request, pk):
    user0 = User.objects.get(id=pk)
    common_friends = len([x for x in user0.friends.all() if x in request.user.friends.all()])
    if request.user != user0:
        return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})
    user0.pending_invs.add()
    candidates = [x for x in user0.pending_invs.all()]
    return render(request, 'base/request_box.html', {'user0' : user0, 'common_friends': common_friends, 'candidates': candidates})

def validate_username(request):
    username = request.GET.get('username', None)
    username = username.strip()
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)

# @login_required(login_url='/login/')
# def alert_friendship(request):
#     sender = request.GET.get('sender')
#     receiver = request.GET.get('receiver')
#     fdata = {'sender' : sender, 'receiver' : sender}
#     if sender in receiver.pending_invs.all():
#         return JsonResponse(fdata)
#     return redirect('home')

def loadmore(request): # 2 rooms at each click => two separate appends {when there's more than a room left (visible and visible+1), when there's exactly one room left (visible)}
    dataa = {}
    visible = int(request.GET.get('visible', None))
    q = request.GET.get('q').strip() if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) | # if the topic name contains the 'q' input (i in icontains makes it case insensitive : a, A are considered the same)
        Q(name__icontains=q) |
        Q(description__icontains=q))
    if len(rooms) <= 4:
        return redirect('home')
    # now = datetime.datetime.now().replace(tzinfo=None)
    now = datetime.datetime.now(timezone.utc)
    # next_two_rooms = Room.objects.filter(
    # Q(topic__name__icontains=q) | # if the topic name contains the 'q' input (i in icontains makes it case insensitive : a, A are considered the same)
    # Q(name__icontains=q) |
    # Q(description__icontains=q))[visible-2 : visible] 
    if visible <= len(rooms)-1:
        room1 = rooms[visible-1]
        room2 = rooms[visible]
        dataa = {"newroomhost" : room1.host.name,
        "newroomhostid" : room1.host.id,
        "newroomhostavatar" : str(room1.host.avatar.url),
        "newroomname" : room1.name,
        "newroomid" : room1.id,
        "newroomdescription" : room1.description,
        "newroomtopic" : str(room1.topic),
        "newroomparticipants" : len(room1.participants.all()),
        "roomgettimedifference" : std(room1.get_time_diffr()),
        "roomcreated" : room1.created,
        "newroomhost1" : room2.host.name,
        "newroomhostid1" : room2.host.id,
        "newroomhostavatar1" : str(room2.host.avatar.url),
        "newroomname1" : room2.name,
        "newroomid1" : room2.id,
        "newroomdescription1" : room2.description,
        "newroomtopic1" : str(room2.topic),
        "newroomparticipants1" : len(room2.participants.all()),
        "roomgettimedifference1" : std(room2.get_time_diffr()),
        "roomcreated1" : room2.created,
        }
    elif visible == len(rooms):
        room1 = rooms[visible-1]
        dataa = {"newroomhost" : room1.host.name,
        "newroomhostid" : room1.host.id,
        "newroomhostavatar" : str(room1.host.avatar.url),
        "newroomname" : room1.name,
        "newroomid" : room1.id,
        "newroomdescription" : room1.description,
        "newroomtopic" : str(room1.topic),
        "newroomparticipants" : len(room1.participants.all()),
        "roomgettimedifference" : std(room1.get_time_diffr()),
        }
    if request.is_ajax():
        return JsonResponse(dataa)

@login_required(login_url='/login/')
def send_friendship(request, pk):
    # if not request.user.confirmed:
    #     return render(request, 'base/httpresponse.html', {'http_response' : 'Your account has not been confirmed!', 'confirm_link' : '1'})
    user = User.objects.get(id=pk)
    if request.user in user.friends.all():
        return render(request, 'base/httpresponse.html', {'http_response' : 'You\'re already friends!'})
    user.pending_invs.add(request.user)
    return redirect('userprofile', pk=pk)

@login_required(login_url='/login/')
def retract_friendship(request, pk):
    user_to_be_taken_back_invitation_from = User.objects.get(id=pk)
    if request.user not in user_to_be_taken_back_invitation_from.pending_invs.all():
        return HttpResponseForbidden()
    user_to_be_taken_back_invitation_from.pending_invs.remove(request.user)
    return redirect('userprofile', pk=pk)

@login_required(login_url='/login/')
def accept_friendship(request, pkk, pk):
    user = User.objects.get(id=pkk)
    if request.user != user:
        return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})
    pending_to_be_accepted = User.objects.get(id=pk)
    if pending_to_be_accepted not in user.pending_invs.all():
        return render(request, 'base/httpresponse.html', {'http_response' : 'You cannot accept this request as the user who made it has taken it back!'})
    user.friends.add(pending_to_be_accepted)
    pending_to_be_accepted.friends.add(user)
    user.pending_invs.remove(pending_to_be_accepted)
    return redirect('request-box', pk=user.id)

@login_required(login_url='/login/')
def ignore_friendship(request, pkk, pk):
    user = User.objects.get(id=pkk)
    if request.user != user:
        return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})
    pending_to_be_accepted = User.objects.get(id=pk)
    user.pending_invs.remove(pending_to_be_accepted)
    return redirect('request-box', pk=user.id)

@login_required(login_url='/login/')
def delete_friendship(request, pkk, pk):
    user = User.objects.get(id=pkk)
    user_to_be_deleted = User.objects.get(id=pk)
    if request.user != user:
        return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})
    if request.method == 'POST':
        user.friends.remove(user_to_be_deleted)
        user_to_be_deleted.friends.remove(user)
        return redirect('friends', pk=request.user.id)
    return render(request, 'base/delete.html', {'obj' : f'@{user_to_be_deleted.username}'})

@login_required(login_url='/login/')
def deletemessage(request, pk): # pk = primary key
    if not request.user.is_authenticated:
        return redirect('login')
    message = Message.objects.get(id=pk)
    room = message.room
    if request.user != message.user:
        return render(request, 'base/httpresponse.html', {'http_response' : 'Not Allowed!'})
    if request.method == 'POST': # means submitting the input (in this case : 'Confirm')
        if len(Message.objects.filter(user=message.user, room=message.room)) == 1:
            room.participants.remove(message.user)
            room.save()

        message.delete()
        return redirect('room', pk=message.room.id)
    return render(request, 'base/delete.html', {'obj':message}) # value is accessed by the name of the key in the template.


@login_required(login_url='/login/')
def updateuser(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofile', pk=user.id)
    return render(request, 'base/update-user.html', {'form' : form})

@login_required(login_url='/login/')
def topicsPage(request):
    q = request.GET.get('q').strip() if request.GET.get('q') != None else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'base/topics.html', {'topics': topics})

@login_required(login_url='/login/')
def ActivityPage(request):
    room_messages = Message.objects.all()[:5]
    return render(request, 'base/activity.html', {'room_messages' : room_messages})
