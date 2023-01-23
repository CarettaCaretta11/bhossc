import os
import re
import sqlite3
import datetime
import rstr
from math import floor

from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Q
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.timezone import now
from django.utils.timezone import utc

from bhossc.settings import DEFAULT_FROM_EMAIL
from .models import Message, Room, Topic, User, Reglink
from .forms import RoomForm, UserForm, MyUserCreationForm


def page_not_found_view(request):
    return render(request, 'core/404.html')


def wdhm(sec):  # weeks-days-hours-minutes
    w = floor(sec / (3600 * 24 * 7))
    d = floor((sec - 3600 * 24 * 7 * w) / (3600 * 24))
    h = floor((sec - 3600 * 24 * 7 * w - 3600 * 24 * d) / 3600)
    m = floor((sec - 3600 * 24 * 7 * w - 3600 *
               24 * d - 3600 * h) / 60)

    return w, d, h, m


def std(sec):  # sec_to_days
    w, d, h, m = wdhm(sec)
    if sec < 60:
        return "just now"
    elif sec < 3600:
        return f'{m} minutes'
    elif sec < 24 * 3600:
        return f'{h} hours, {m} minutes' if m != 0 else f'{h} hours'
    elif sec < 24 * 3600 * 7:
        return f'{d} days'
    else:
        return f'{w} weeks, {d} days' if d != 0 else f'{w} weeks'


def stds(sec):  # sec_to_days_status
    w, d, h, m = wdhm(sec)
    if sec < 60:
        return f"{floor(sec)} seconds"
    elif sec < 3600:
        return f'{m} minutes'
    elif sec < 24 * 3600:
        return f'{h} hours, {m} minutes' if m != 0 else f'{h} hours'
    elif sec < 24 * 3600 * 7:
        return f'{d} days'
    else:
        return f'{w} weeks, {d} days' if d != 0 else f'{w} weeks'


def login_page(request):
    page = 'az'  # just to distinguish this with register_user as both are connected to login_register.html
    # neither its name nor its value matter
    if request.user.is_authenticated:
        return redirect('home')
    # request.POST - Contains parameters added as part of a POST request.
    # Parameters are enclosed as a django.http.request.QueryDict instance.
    if request.method == 'POST':
        # request.POST.get('name',default=None) Gets the value of the name parameter in a POST request
        # or gets None if the parameter is not present. Note default can be overridden with a custom value.
        email = request.POST.get('email').strip().lower()
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user:
            login(request, user)
            nextt = request.GET.get('next')
            if nextt:
                return redirect(nextt)
            else:
                return redirect('home')
        else:
            messages.error(request, 'Incorrect username or password!')
    context = {'page': page}
    return render(request, 'core/login_register.html', context)


reg = r'(\d|[a-z]|[A-Z]){6}(\d|[a-z]|[A-Z]){9}(\d){5}([A-Z]|[a-z]){5}[a-z]{3}(\d|[A-Z]|[a-z]){4}'
dns = os.environ.get("BHOSSC_ROOT_URL")


def register_user_preliminary(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('home')
    elif request.method == 'POST':
        email = str(request.POST.get('email1')).strip()
        if User.objects.filter(email=email).exists():
            return render(request, 'core/httpresponse.html',
                          {'reg_mes': 'A user with this email is already registered!'})
        elif not email.endswith('@bhos.edu.az'):
            return render(request, 'core/httpresponse.html', {'invalid_email': 'heyy'})
        else:
            reglink = f'{dns}{email}{rstr.xeger(reg)}'
            try:
                Reglink.objects.create(email=email, reglink=reglink)
                send_mail(
                    subject='Registration',
                    message="Here is your registration link:",
                    from_email=DEFAULT_FROM_EMAIL,
                    recipient_list=[f'{email}'],
                    html_message=f'''
                    <p>Here is your registration link:</p><br><a href={reglink} style="text-decoration:
                    none;display:inline-block;white-space:nowrap;word-break:keep-all;overflow:hidden;text-overflow:
                    ellipsis;background-image:linear-gradient(#05b8ff,#05b8ff);color:#000000;font-size:18px;
                    font-weight:bold;text-align:center;padding:12px 14px;border-radius:48px;background-color:
                    #05b8ff!important">Register</a><br><strong>Do not share it with anyone.</strong>''',
                    fail_silently=False
                )
            except IntegrityError:
                return render(
                    request,
                    'core/httpresponse.html',
                    {
                        'http_response': '''A registration link has already been sent to the given email address.
                                            Please contact the admin in case you need a new link.'''
                    },
                )
    return render(request, 'core/reg_email.html')


def register_user(request, *args, **kwargs):
    if request.user.is_authenticated:
        return redirect('home')
    abs_path = request.build_absolute_uri()
    email = re.findall(r'.*@bhos.edu.az', abs_path)[0][len(dns):]
    the_link = get_object_or_404(Reglink, email=email).reglink

    if abs_path != the_link:
        return render(request, 'core/404.html')

    form = MyUserCreationForm()
    if request.method == 'POST':
        if request.build_absolute_uri() != the_link:
            return render(request, 'core/404.html')
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.email = email.lower()
            user.save()
            login(request, user)
            Reglink.objects.get(email=email).delete()
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')
    return render(request, 'core/login_register.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


def home(request):
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    q = request.GET.get('q').strip() if request.GET.get('q') else ''
    topics = Topic.objects.all()[0:4]
    lst = 0
    if Topic.objects.filter(name__icontains='Lost items').count() > 0:
        lst = Topic.objects.get(
            name__icontains='Lost items').room_set.all().count()
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(host__username=q) |
        Q(description__icontains=q))[0:5]
    room_count = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q)).count()
    room_messages = Message.objects.filter(
        Q(room__topic__name__icontains=q))[0:5]
    context = {'rooms': rooms, 'topics': topics, 'room_count': room_count,
               'room_messages': room_messages, 'now': now, 'lst': lst}
    return render(request, 'core/home.html', context)


@login_required(login_url='/login/')
def room(request, pk):
    room = get_object_or_404(Room, id=int(pk))
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST' and str(request.POST.get("body")).strip() == '':
        return redirect('room', pk=pk)
    elif request.method == 'POST':
        try:
            Message.objects.create(
                user=request.user,
                room=room,
                body=request.POST.get('body')
            )
            room.participants.add(request.user)
            return redirect('room', pk=pk)
        except ValueError:
            return redirect('login')
    context = {'room': room, 'room_messages': room_messages,
               'participants': participants}
    return render(request, 'core/room.html', context)


def get_group_name(user1, user2):
    a = 'chat_{}_{}'.format(*sorted([user1.id, user2.id]))
    return str(a)


@login_required(login_url='/login/')
def status_checker(request):
    if request.GET.get('st'):
        User.objects.filter(id=request.user.id).update(last_time_visited=now())
        return JsonResponse({
            'last_time_visited': request.user.last_time_visited,
            'get_time_difference': request.user.get_time_diff(),
            'get_time_difference_minutes': std(request.user.get_time_diff()),
        })


@login_required(login_url='/login/')
def profile_status(request, pk):
    user = User.objects.get(id=pk)
    gtd = user.get_time_diff()
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
def user_profile(request, pk):
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
    context = {'user': user, 'rooms': rooms, 'topics': topics,
               'room_messages': room_messages, 'ltv': ltv, 'gtd': gtd, 'a': a, 'pm_link': pm_link}
    return render(request, 'core/profile.html', context)


@login_required(login_url='/login/')
def friends_list(request, pk):
    user = User.objects.get(id=pk)
    frr = user.friends.all()
    a = [get_group_name(user, x) for x in frr]
    zipp = zip(frr, a)
    if request.user not in user.friends.all() and request.user != user:
        return render(request, 'core/httpresponse.html', {'http_response': 'Not Allowed!'})
    return render(request, 'core/friends-1.html', {'user': user, 'zipp': zipp, 'frr': frr})


@login_required(login_url='/login/')
def friends_list_mobile(request, pk):
    user = User.objects.get(id=pk)
    frr = user.friends.all()[0:9]
    a = [get_group_name(user, x) for x in frr]
    zipp = zip(frr, a)
    if request.user not in user.friends.all() and request.user != user:
        return render(request, 'core/httpresponse.html', {'http_response': 'Not Allowed!'})
    return render(request, 'core/friends_mobile.html', {'user': user, 'zipp': zipp})


@login_required(login_url='/login/')
def create_room(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        thumbnail = request.POST.get('thumbnail')
        # get_or_create() returns a tuple of ($object, $created), where $object is the
        # retrieved or created object, and $created is a boolean specifying whether a new object was created.
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room = Room(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            thumbnail=thumbnail
        )
        room.save()
        return redirect('room', pk=room.id)

    # we just need the value part (form in this case, as above: room)
    # {'form':form} means the form variable is recognized as 'form' (without quotation marks
    # in the template : core/room_form.html
    context = {'form': form, 'topics': topics}
    return render(request, 'core/room_form.html', context)


@login_required(login_url='/login/')
def update_room(request, pk):
    room = Room.objects.get(id=pk)
    # fills the form (actually creates a new form) with the parameters a room already has
    # which allows us to edit them and 're-submit'.
    form = RoomForm(instance=room)
    topics = Topic.objects.all()
    if request.user != room.host:
        return render(request, 'core/httpresponse.html', {'http_response': 'Not Allowed!'})
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
    context = {'form': form, 'topics': topics, 'room': room}
    return render(request, 'core/update-room.html', context)


@login_required(login_url='/login/')
def delete_room(request, pk):  # pk = primary key
    room = Room.objects.get(id=pk)

    if request.user != room.host:
        return render(request, 'core/httpresponse.html', {'http_response': 'Not Allowed!'})

    # means submitting the input (in this case : 'Confirm')
    if request.method == 'POST':
        if Room.objects.filter(topic=room.topic).count() == 1:
            room.topic.delete()
        room.delete()
        return redirect('home')
    # value is accessed by the name of the key in the template.
    return render(request, 'core/delete.html', {'obj': room})


@login_required(login_url='/login/')
def request_box(request, pk):
    user0 = User.objects.get(id=pk)
    common_friends = len([x for x in user0.friends.all()
                          if x in request.user.friends.all()])
    if request.user != user0:
        return render(request, 'core/httpresponse.html', {'http_response': 'Not Allowed!'})
    user0.pending_invs.add()
    candidates = [x for x in user0.pending_invs.all()]
    return render(request, 'core/request_box.html',
                  {'user0': user0, 'common_friends': common_friends, 'candidates': candidates})


def validate_username(request):
    username = request.GET.get('username', None)
    username = username.strip()
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)


# 2 rooms per click:
# two separate appends {when there's more than a room left (visible and visible+1),
# when there's exactly one room left (visible)}
def load_more(request):
    dataa = {}
    visible = int(request.GET.get('visible', None))
    q = request.GET.get('q').strip() if request.GET.get('q') else ''
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q))
    if len(rooms) < 5:
        return redirect('home')
    if visible <= len(rooms) - 1:
        room1 = rooms[visible - 1]
        room2 = rooms[visible]
        dataa = {
            "newroomhost": room1.host.name,
            "newroomhostid": room1.host.id,
            "newroomhostavatar": str(room1.host.avatar.url),
            "newroomname": room1.name,
            "newroomid": room1.id,
            "newroomdescription": room1.description,
            "newroomtopic": str(room1.topic),
            "newroomparticipants": len(room1.participants.all()),
            "roomgettimedifference": std(room1.get_time_diffr()),
            "roomcreated": room1.created,
            "newroomhost1": room2.host.name,
            "newroomhostid1": room2.host.id,
            "newroomhostavatar1": str(room2.host.avatar.url),
            "newroomname1": room2.name,
            "newroomid1": room2.id,
            "newroomdescription1": room2.description,
            "newroomtopic1": str(room2.topic),
            "newroomparticipants1": len(room2.participants.all()),
            "roomgettimedifference1": std(room2.get_time_diffr()),
            "roomcreated1": room2.created,
        }
    elif visible == len(rooms):
        room1 = rooms[visible - 1]
        dataa = {
            "newroomhost": room1.host.name,
            "newroomhostid": room1.host.id,
            "newroomhostavatar": str(room1.host.avatar.url),
            "newroomname": room1.name,
            "newroomid": room1.id,
            "newroomdescription": room1.description,
            "newroomtopic": str(room1.topic),
            "newroomparticipants": len(room1.participants.all()),
            "roomgettimedifference": std(room1.get_time_diffr()),
        }
    if request.is_ajax():
        return JsonResponse(dataa)


@login_required(login_url='/login/')
def send_friendship(request, pk):
    user = User.objects.get(id=pk)
    if request.user in user.friends.all():
        return render(request, 'core/httpresponse.html', {'http_response': 'You\'re already friends!'})
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
        return render(request, 'core/httpresponse.html', {'http_response': 'Not Allowed!'})
    pending_to_be_accepted = User.objects.get(id=pk)
    if pending_to_be_accepted not in user.pending_invs.all():
        return render(request, 'core/httpresponse.html',
                      {'http_response': 'You cannot accept this request as the user who made it has taken it back!'})
    user.friends.add(pending_to_be_accepted)
    pending_to_be_accepted.friends.add(user)
    user.pending_invs.remove(pending_to_be_accepted)
    return redirect('request-box', pk=user.id)


@login_required(login_url='/login/')
def ignore_friendship(request, pkk, pk):
    user = User.objects.get(id=pkk)
    if request.user != user:
        return render(request, 'core/httpresponse.html', {'http_response': 'Not Allowed!'})
    pending_to_be_accepted = User.objects.get(id=pk)
    user.pending_invs.remove(pending_to_be_accepted)
    return redirect('request-box', pk=user.id)


@login_required(login_url='/login/')
def delete_friendship(request, pkk, pk):
    user = User.objects.get(id=pkk)
    user_to_be_deleted = User.objects.get(id=pk)
    if request.user != user:
        return render(request, 'core/httpresponse.html', {'http_response': 'Not Allowed!'})
    if request.method == 'POST':
        user.friends.remove(user_to_be_deleted)
        user_to_be_deleted.friends.remove(user)
        return redirect('friends', pk=request.user.id)
    return render(request, 'core/delete.html', {'obj': f'@{user_to_be_deleted.username}'})


@login_required(login_url='/login/')
def delete_message(request, pk):  # pk = primary key
    if not request.user.is_authenticated:
        return redirect('login')
    message = Message.objects.get(id=pk)
    room = message.room
    if request.user != message.user:
        return render(request, 'core/httpresponse.html', {'http_response': 'Not Allowed!'})
    # means submitting the input (in this case : 'Confirm')
    if request.method == 'POST':
        if len(Message.objects.filter(user=message.user, room=message.room)) == 1:
            room.participants.remove(message.user)
            room.save()
        message.delete()
        return redirect('room', pk=message.room.id)
    # value is accessed by the name of the key in the template.
    return render(request, 'core/delete.html', {'obj': message})


@login_required(login_url='/login/')
def update_user(request):
    user = request.user
    form = UserForm(instance=user)
    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('userprofile', pk=user.id)
    return render(request, 'core/update-user.html', {'form': form})


@login_required(login_url='/login/')
def topics_page(request):
    q = request.GET.get('q').strip() if request.GET.get('q') else ''
    topics = Topic.objects.filter(name__icontains=q)
    return render(request, 'core/topics.html', {'topics': topics})


@login_required(login_url='/login/')
def activity_page(request):
    room_messages = Message.objects.all()[:5]
    return render(request, 'core/activity.html', {'room_messages': room_messages})
