from django.db import models
from django.contrib.auth.models import User
import uuid

# ===== مدل پیام برای چت =====
class ChatMessage(models.Model):
    room_id = models.IntegerField()
    sender = models.CharField(max_length=100)
    message = models.TextField(blank=True, null=True)  # می‌تونه خالی باشه
    file = models.FileField(upload_to='chat_files/%Y/%m/%d/', null=True, blank=True)  # فایل
    file_type = models.CharField(max_length=50, default='text')  # text, image, video, audio, file
    is_system = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        if self.file:
            return f"{self.sender}: 📎 {self.file.name.split('/')[-1]}"
        return f"{self.sender}: {self.message[:30]}"


# ===== مدل کاربر ناشناس با پروفایل =====
class AnonymousUser(models.Model):
    # ===== اطلاعات پایه =====
    user_id = models.CharField(max_length=20, unique=True)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField(blank=True)
    
    # ===== اطلاعات پروفایل =====
    display_name = models.CharField(max_length=100, blank=True)  # اسم نمایشی
    bio = models.TextField(max_length=500, blank=True)  # بیوگرافی
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)  # عکس پروفایل
    
    # ===== آمار و اعتبار =====
    reputation = models.IntegerField(default=0)
    karma = models.IntegerField(default=0)  # <-- فیلد کارما اضافه شد
    trust_score = models.IntegerField(default=50)
    posts_count = models.PositiveIntegerField(default=0)
    
    # ===== وضعیت =====
    is_banned = models.BooleanField(default=False)
    ban_reason = models.TextField(blank=True)
    ban_expires_at = models.DateTimeField(null=True, blank=True)
    
    # ===== زمان‌ها =====
    created_at = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.display_name:
            return f"{self.display_name} ({self.user_id[:8]})"
        return f"Anon-{self.user_id[:8]}"
    
    @classmethod
    def generate_id(cls):
        return f"ANON_{uuid.uuid4().hex[:10].upper()}"
    
    def get_avatar_url(self):
        if self.avatar:
            return self.avatar.url
        return None
    
class Reaction(models.Model):
    message = models.ForeignKey(ChatMessage, on_delete=models.CASCADE, related_name='reactions')
    user = models.CharField(max_length=100)
    emoji = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['message', 'user', 'emoji']

# ===== مدل دوست‌یابی =====
class FriendRequest(models.Model):
    from_user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, related_name='sent_requests')
    to_user = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, related_name='received_requests')
    status = models.CharField(max_length=20, choices=[
        ('pending', 'در انتظار'),
        ('accepted', 'پذیرفته شده'),
        ('rejected', 'رد شده')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['from_user', 'to_user']  # هر کاربر فقط یه بار می‌تونه به دیگری درخواست بده

    def __str__(self):
        return f"{self.from_user.display_name} -> {self.to_user.display_name} ({self.status})"

# ===== مدل چت خصوصی =====
class PrivateChatRoom(models.Model):
    user1 = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, related_name='private_rooms1')
    user2 = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE, related_name='private_rooms2')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Private chat between {self.user1.display_name} and {self.user2.display_name}"

    def get_other_user(self, user):
        """دریافت کاربر مقابل در چت خصوصی"""
        return self.user2 if self.user1 == user else self.user1

class PrivateMessage(models.Model):
    room = models.ForeignKey(PrivateChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(AnonymousUser, on_delete=models.CASCADE)
    content = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.sender.display_name}: {self.content[:30]}"