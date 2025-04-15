from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import pusher
from django.conf import settings
from django.shortcuts import render
from .models import Message,ChatRequest

# Initialize Pusher
pusher_client = pusher.Pusher(
    app_id=settings.PUSHER_APP_ID,
    key=settings.PUSHER_KEY,
    secret=settings.PUSHER_SECRET,
    cluster=settings.PUSHER_CLUSTER,
    ssl=True
)

@csrf_exempt
def send_message(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        room_name = data.get('room')
        message_text = data.get('message')
        sender_username = data.get('sender')

        # Get the sender user object
        sender = CustomUser.objects.get(username=sender_username)

        # Find the chat request associated with the room
        chat_request = ChatRequest.objects.get(room_name=room_name)

        # Save the message to the database
        message = Message.objects.create(
            chat_request=chat_request,
            sender=sender,
            message=message_text
        )

        # Trigger a Pusher event for real-time updates
        pusher_client.trigger(f'chat-{room_name}', 'new_message', {
            'message': message_text,
            'sender': sender_username
        })

        # Trigger a Pusher event to update the chat requests table
        pusher_client.trigger('chat-requests', 'new_user_message', {
            'room_name': room_name,
            'user_id': chat_request.user.id,
            'username': chat_request.user.username
        })

        return JsonResponse({'status': 'Message sent'})
    
def chat_room(request, room_name, username):
    # Fetch the chat request associated with the room
    chat_request = get_object_or_404(ChatRequest, room_name=room_name)

    # Fetch all messages for the chat request
    messages = Message.objects.filter(chat_request=chat_request).order_by('timestamp')

    return render(request, 'chat/room.html', {
        'room_name': room_name,
        'username': username,
        'messages': messages  # Pass the chat history to the template
    })


from django.shortcuts import get_object_or_404, redirect
from common.models import CustomUser
from .models import ChatRequest
import uuid

def create_chat_request(request, engineer_id):
    engineer = get_object_or_404(CustomUser, id=engineer_id)
    user = request.user

    # Check if a chat request already exists
    chat_request, created = ChatRequest.objects.get_or_create(
        user=user,
        engineer=engineer,
        defaults={'room_name': f'room_{uuid.uuid4().hex}'}
    )

    # Redirect to the chat room
    return redirect('chat_room', room_name=chat_request.room_name, username=user.username)


from django.shortcuts import render
from .models import ChatRequest
from django.db.models import Count, Q,F


def engineer_chat_requests(request):
    engineer = request.user
    chat_requests = ChatRequest.objects.filter(engineer=engineer).annotate(
        user_message_count=Count('messages', filter=Q(messages__sender=F('user')))
    )
    return render(request, 'engineer/chat.html', {'chat_requests': chat_requests})



