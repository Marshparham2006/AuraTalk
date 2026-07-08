import json
import base64
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, AnonymousUser, Reaction, PrivateChatRoom, PrivateMessage
from django.core.files.base import ContentFile

STICKERS = {
    '😊': '😊',
    '😂': '😂',
    '❤️': '❤️',
    '🔥': '🔥',
    '👍': '👍',
    '👏': '👏',
    '💀': '💀',
    '🎉': '🎉',
    '🤔': '🤔',
    '😍': '😍',
}

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'chat_{self.room_id}'
        
        query_string = self.scope['query_string'].decode()
        self.username = 'Anonymous'
        if 'username=' in query_string:
            self.username = query_string.split('username=')[-1]

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

        await self.send_previous_messages()

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'👋 {self.username} joined the room!',
                'sender': 'System',
                'is_system': True,
            }
        )

    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'👋 {self.username} left the room.',
                'sender': 'System',
                'is_system': True,
            }
        )

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        
        if data.get('type') == 'typing':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'typing_status',
                    'sender': data.get('sender', 'Anonymous'),
                    'is_typing': data.get('is_typing', True),
                }
            )
            return
        
        if data.get('type') == 'sticker':
            sticker_code = data.get('sticker', '😊')
            sender = data.get('sender', 'Anonymous')
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': sticker_code,
                    'sender': sender,
                    'is_system': False,
                    'is_sticker': True,
                }
            )
            return
        
        if data.get('type') == 'delete':
            message_id = data.get('message_id')
            sender = data.get('sender')
            deleted = await self.delete_message(message_id, sender)
            
            if deleted:
                await self.channel_layer.group_send(
                    self.room_group_name,
                    {
                        'type': 'delete',
                        'message_id': message_id,
                        'sender': sender,
                    }
                )
            return
        
        if data.get('type') == 'reaction':
            message_id = data.get('message_id')
            emoji = data.get('emoji')
            sender = data.get('sender')
            
            await self.save_reaction(message_id, sender, emoji)
            
            reactions = await self.get_reactions_count(message_id)
            
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'reaction',
                    'message_id': message_id,
                    'emoji': emoji,
                    'sender': sender,
                    'reactions': reactions,
                }
            )
            return
        
        message = data.get('message', '')
        sender = data.get('sender', 'Anonymous')
        file_data = data.get('file', None)
        file_name = data.get('file_name', None)
        file_type = data.get('file_type', 'text')
        
        await self.add_karma(sender)
        
        saved_message = await self.save_message(
            self.room_id, sender, message, file_data, file_name, file_type
        )
        
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'is_system': False,
                'is_sticker': False,
                'file_url': saved_message.file.url if saved_message.file else None,
                'file_type': file_type,
                'file_name': file_name,
                'message_id': saved_message.id,
            }
        )

    async def chat_message(self, event):
        from datetime import datetime
        time = datetime.now().strftime('%H:%M')
        
        await self.send(text_data=json.dumps({
            'type': 'message',
            'message': event.get('message', ''),
            'sender': event.get('sender', 'Anonymous'),
            'is_system': event.get('is_system', False),
            'is_sticker': event.get('is_sticker', False),
            'time': time,
            'file_url': event.get('file_url', None),
            'file_type': event.get('file_type', 'text'),
            'file_name': event.get('file_name', None),
            'message_id': event.get('message_id', None),
        }))

    async def typing_status(self, event):
        await self.send(text_data=json.dumps({
            'type': 'typing',
            'sender': event['sender'],
            'is_typing': event['is_typing'],
        }))

    async def delete(self, event):
        await self.send(text_data=json.dumps({
            'type': 'delete',
            'message_id': event['message_id'],
            'sender': event['sender'],
        }))

    async def reaction(self, event):
        await self.send(text_data=json.dumps({
            'type': 'reaction_update',
            'message_id': event['message_id'],
            'emoji': event['emoji'],
            'sender': event['sender'],
            'reactions': event.get('reactions', {}),
        }))

    @database_sync_to_async
    def save_message(self, room_id, sender, message, file_data=None, file_name=None, file_type='text'):
        if file_data and file_name:
            try:
                format, imgstr = file_data.split(';base64,')
                ext = file_name.split('.')[-1]
                file_content = ContentFile(base64.b64decode(imgstr), name=file_name)
                
                return ChatMessage.objects.create(
                    room_id=room_id,
                    sender=sender,
                    message=message or '',
                    file=file_content,
                    file_type=file_type,
                    is_system=False
                )
            except Exception as e:
                print(f"Error saving file: {e}")
                return ChatMessage.objects.create(
                    room_id=room_id,
                    sender=sender,
                    message=message,
                    is_system=False
                )
        else:
            return ChatMessage.objects.create(
                room_id=room_id,
                sender=sender,
                message=message,
                is_system=False
            )

    @database_sync_to_async
    def delete_message(self, message_id, sender):
        try:
            msg = ChatMessage.objects.get(id=message_id)
            if msg.sender == sender or sender == 'System':
                msg.delete()
                return True
        except ChatMessage.DoesNotExist:
            pass
        return False

    @database_sync_to_async
    def save_reaction(self, message_id, user, emoji):
        try:
            msg = ChatMessage.objects.get(id=message_id)
            reaction, created = Reaction.objects.get_or_create(
                message=msg,
                user=user,
                emoji=emoji
            )
            if not created:
                reaction.delete()
                return False
            return True
        except:
            return False

    @database_sync_to_async
    def get_reactions_count(self, message_id):
        try:
            msg = ChatMessage.objects.get(id=message_id)
            reactions = msg.reactions.all()
            result = {}
            for r in reactions:
                result[r.emoji] = result.get(r.emoji, 0) + 1
            return result
        except:
            return {}

    @database_sync_to_async
    def get_previous_messages(self):
        return list(ChatMessage.objects.filter(
            room_id=self.room_id
        ).order_by('created_at'))

    async def send_previous_messages(self):
        messages = await self.get_previous_messages()
        for msg in messages:
            reactions = await self.get_reactions_count(msg.id)
            await self.send(text_data=json.dumps({
                'type': 'history',
                'message': msg.message or '',
                'sender': msg.sender,
                'is_system': msg.is_system,
                'time': msg.created_at.strftime('%H:%M'),
                'file_url': msg.file.url if msg.file else None,
                'file_type': msg.file_type,
                'file_name': msg.file.name.split('/')[-1] if msg.file else None,
                'message_id': msg.id,
                'reactions': reactions,
            }))

    @database_sync_to_async
    def add_karma(self, sender):
        try:
            user = AnonymousUser.objects.get(display_name=sender)
            user.karma += 1
            user.save()
        except AnonymousUser.DoesNotExist:
            pass


# ==========================================
# WebSocket برای چت خصوصی
# ==========================================

class PrivateChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_id = self.scope['url_route']['kwargs']['room_id']
        self.room_group_name = f'private_chat_{self.room_id}'
        
        query_string = self.scope['query_string'].decode()
        self.username = 'Anonymous'
        if 'username=' in query_string:
            self.username = query_string.split('username=')[-1]

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data.get('message', '')
        sender = data.get('sender', 'Anonymous')
        room_id = data.get('room_id')

        # ذخیره پیام در دیتابیس
        await self.save_private_message(room_id, sender, message)

        # ارسال پیام به گروه
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'private_message',
                'message': message,
                'sender': sender,
            }
        )

    async def private_message(self, event):
        from datetime import datetime
        time = datetime.now().strftime('%H:%M')
        
        await self.send(text_data=json.dumps({
            'type': 'message',
            'content': event['message'],
            'sender': event['sender'],
            'time': time,
        }))

    @database_sync_to_async
    def save_private_message(self, room_id, sender, message):
        try:
            room = PrivateChatRoom.objects.get(id=room_id)
            user = AnonymousUser.objects.get(display_name=sender)
            PrivateMessage.objects.create(
                room=room,
                sender=user,
                content=message
            )
        except Exception as e:
            print(f"Error saving private message: {e}")