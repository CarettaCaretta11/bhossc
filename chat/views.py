import re
from django.http.response import HttpResponse, HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import User
from chat.models import PmMessages


def index(request):
    return render(request, 'chat/index.html')


def get_group_name(user1, user2):
    return 'chat-{}-{}'.format(*sorted([user1.id, user2.id]))


def room(request, room_name):
    room_name_pattern = re.compile(r'chat_\d{1,9999999}_\d{1,9999999}')
    number_pattern = re.compile(r'\d+')
    legit_id_1, legit_id_2 = number_pattern.findall(room_name)
    legit_user_1 = get_object_or_404(User, id=int(legit_id_1))
    legit_user_2 = get_object_or_404(User, id=int(legit_id_2))
    if request.user != legit_user_1 and request.user != legit_user_2:
        return HttpResponseForbidden()
    if not room_name_pattern.findall(room_name):
        return HttpResponse('No such chat room!')

    if legit_user_2 not in legit_user_1.friends.all():
        return HttpResponse('You\'re not friends and hence you cannot have a private chat room!')
    messagess = []
    for message in PmMessages.objects.filter(room=room_name).reverse()[0:25]:
        messagess.append(message)
        print(type(message.sender))
    messagess.reverse()
    return render(request, 'chat/room.html', {'room_name': room_name, 'messagess': messagess, 'legit_user_1': legit_user_1, 'legit_user_2': legit_user_2})


@login_required(login_url='/login/')
def delete_pm_message(request, pk):  # pk = primary key
    pm_message = pm_messages.objects.get(id=pk)
    if request.user != pm_message.sender:
        return HttpResponseNotAllowed()
    # means submitting the input (in this case : 'Confirm')
    if request.method == 'POST':
        pm_message.delete()
    # value is accessed by the name of the key in the template.
    return render(request, 'core/delete.html', {'obj': pm_message})

# def chatt(request, room_name):
#     if request.is_ajax and request.method == 'POST':
#         msg = request.POST.get('msg')
#         msg_user = User.objects.get(id=request.POST.get('msg_user_id'))
#         pm_messages.objects.create(
#             body=msg,
#             sender=msg_user,
#             room=f'chat_{room_name}',
#         )
#         JsonResponse({
#             'saved': True
#         })
