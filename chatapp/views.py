from django.shortcuts import render
from .models import ChatRoom,ChatMessage
# Create your views here.
def index(request):
    chatrooms = ChatRoom.objects.all()

    return render(request,'chatapp/index.html',{'chatrooms':chatrooms})
def chatroom(request,slug):
    chatroom = ChatRoom.objects.get(slug = slug)
    historyMessage = ChatMessage.objects.filter(room = chatroom)
    return render(request,'chatapp/room.html',{'chatroom':chatroom,'messages':historyMessage})
