from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from .models import AnonymousUser, ChatMessage, FriendRequest, PrivateChatRoom, PrivateMessage

def home(request):
    return HttpResponse("""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AuraTalk - Anonymous Chat Rooms | Talk Freely</title>
    <meta name="description" content="Join AuraTalk, the best anonymous chat platform. No sign-up, no tracking, just real conversations with people around the world. Free and private.">
    <meta name="keywords" content="anonymous chat, free chat rooms, talk to strangers, private chat, no sign-up chat, online chat">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://auratalk.com/">
    
    <!-- Open Graph -->
    <meta property="og:title" content="AuraTalk - Anonymous Chat Rooms">
    <meta property="og:description" content="Join AuraTalk, the best anonymous chat platform. No sign-up, no tracking, just real conversations.">
    <meta property="og:image" content="https://auratalk.com/static/logo.png">
    <meta property="og:url" content="https://auratalk.com/">
    <meta property="og:type" content="website">
    
    <!-- Twitter Card -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="AuraTalk - Anonymous Chat Rooms">
    <meta name="twitter:description" content="Join AuraTalk, the best anonymous chat platform. No sign-up, no tracking, just real conversations.">
    
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #0f0c29, #302b63, #24243e); min-height: 100vh; display: flex; justify-content: center; align-items: center; color: #fff; margin: 0; padding: 20px; }
        .container { text-align: center; padding: 50px 40px; background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.08); max-width: 650px; width: 100%; animation: fadeIn 1.2s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(30px); } to { opacity: 1; transform: translateY(0); } }
        .logo { font-size: 80px; margin-bottom: 15px; display: inline-block; animation: spin 12s linear infinite; }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        h1 { font-size: 52px; font-weight: 700; background: linear-gradient(135deg, #6C25FF, #0088FF); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 12px; letter-spacing: -1px; }
        .subtitle { color: #aaa; font-size: 18px; line-height: 1.8; margin-bottom: 30px; font-weight: 400; }
        .btn-group { display: flex; gap: 15px; justify-content: center; flex-wrap: wrap; margin-bottom: 15px; }
        .btn-start { display: inline-block; padding: 16px 45px; background: linear-gradient(135deg, #6C25FF, #0088FF); color: #fff; text-decoration: none; border-radius: 50px; font-size: 18px; font-weight: 600; transition: all 0.3s ease; border: none; cursor: pointer; }
        .btn-start:hover { transform: scale(1.05); box-shadow: 0 0 30px rgba(108, 37, 255, 0.5), 0 0 60px rgba(108, 37, 255, 0.2); }
        .btn-explore { display: inline-block; padding: 16px 40px; background: transparent; color: #fff; text-decoration: none; border-radius: 50px; font-size: 18px; font-weight: 600; border: 2px solid rgba(255,255,255,0.15); transition: all 0.3s ease; cursor: pointer; }
        .btn-explore:hover { border-color: #6C25FF; background: rgba(108, 37, 255, 0.1); transform: scale(1.02); }
        .sub-note { font-size: 14px; color: #666; margin-bottom: 30px; font-weight: 400; }
        .features { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 10px; }
        .feature-item { background: rgba(255, 255, 255, 0.04); padding: 18px 12px; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.05); transition: all 0.3s ease; }
        .feature-item:hover { background: rgba(255, 255, 255, 0.08); transform: translateY(-4px); }
        .feature-item span { font-size: 32px; display: block; margin-bottom: 6px; }
        .feature-item p { font-size: 13px; color: #bbb; margin: 0; font-weight: 400; }
        
        /* ===== SEO About Section ===== */
        .seo-about { margin-top: 40px; padding: 25px; background: rgba(255,255,255,0.03); border-radius: 16px; border: 1px solid rgba(255,255,255,0.05); }
        .seo-about h3 { color: #6C25FF; text-align: center; font-size: 20px; margin-bottom: 12px; }
        .seo-about p { color: #888; font-size: 14px; line-height: 1.8; text-align: center; max-width: 500px; margin: 0 auto; }
        .seo-about .seo-tags { display: flex; flex-wrap: wrap; justify-content: center; gap: 8px; margin-top: 15px; }
        .seo-about .seo-tags span { background: rgba(108,37,255,0.15); color: #6C25FF; padding: 4px 14px; border-radius: 50px; font-size: 12px; }
        
        .footer { margin-top: 35px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.06); display: flex; justify-content: center; gap: 25px; flex-wrap: wrap; }
        .footer a { color: #666; text-decoration: none; font-size: 13px; transition: color 0.3s ease; font-weight: 400; }
        .footer a:hover { color: #aaa; }
        
        @media (max-width: 550px) { .container { padding: 30px 20px; } h1 { font-size: 34px; } .logo { font-size: 60px; } .features { grid-template-columns: 1fr; } .btn-start, .btn-explore { width: 100%; } .btn-group { flex-direction: column; } }
    </style>
</head>
<body>
    <div class="container">
        <div class="logo">✨</div>
        <h1>AuraTalk</h1>
        <p class="subtitle">Welcome to the world of anonymous conversations.<br>Here you can be yourself without fear of judgment.</p>
        <div class="btn-group">
            <a href="/choose-username/" class="btn-start">🚀 Get Started</a>
            <a href="#" class="btn-explore">👀 Explore</a>
        </div>
        <p class="sub-note">⚡ No sign-up. No tracking. Just real conversations.</p>
        <div class="features">
            <div class="feature-item"><span>💬</span><p>Live Chat Rooms</p></div>
            <div class="feature-item"><span>👥</span><p>Anonymous Friends</p></div>
            <div class="feature-item"><span>🛡️</span><p>Speak Freely</p></div>
        </div>
        
        <!-- ===== SEO About Section ===== -->
        <div class="seo-about">
            <h3>About AuraTalk</h3>
            <p>AuraTalk is a free anonymous chat platform where you can talk to strangers, make new friends, and express yourself without fear of judgment. No sign-up required. No tracking. Just real conversations.</p>
            <div class="seo-tags">
                <span>anonymous chat</span>
                <span>free chat rooms</span>
                <span>talk to strangers</span>
                <span>private chat</span>
                <span>no sign-up</span>
            </div>
        </div>
        
        <div class="footer"><a href="#">About</a><a href="#">Privacy</a><a href="#">Terms</a></div>
    </div>
</body>
</html>
""")

def choose_username(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        if username and len(username.strip()) > 0:
            username = username.strip()
            request.session['username'] = username
            request.session['display_name'] = username
            
            user, created = AnonymousUser.objects.get_or_create(
                display_name=username,
                defaults={
                    'user_id': AnonymousUser.generate_id(),
                    'ip_address': request.META.get('REMOTE_ADDR'),
                    'user_agent': request.META.get('HTTP_USER_AGENT', ''),
                    'bio': 'Just a soul wandering through anonymous conversations.'
                }
            )
            request.session['user_id'] = user.user_id
            
            return redirect('/chat/')
    
    return render(request, 'choose_username.html')

def chat_rooms(request):
    if not request.session.get('username'):
        return redirect('/choose-username/')
    
    default_rooms = [
        {'id': 1, 'name': 'General', 'icon': '💬', 'members': 12, 'hot': False, 'recommended': True, 'last_message': '👋 Welcome everyone!'},
        {'id': 2, 'name': 'Technology', 'icon': '💻', 'members': 8, 'hot': True, 'recommended': False, 'last_message': '🤖 AI is the future...'},
        {'id': 3, 'name': 'Art & Design', 'icon': '🎨', 'members': 5, 'hot': False, 'recommended': False, 'last_message': '🖌️ Check out my new sketch!'},
        {'id': 4, 'name': 'Gaming', 'icon': '🎮', 'members': 15, 'hot': True, 'recommended': False, 'last_message': '🎯 New game release today!'},
        {'id': 5, 'name': 'Music', 'icon': '🎵', 'members': 6, 'hot': False, 'recommended': False, 'last_message': '🎶 What are you listening to?'},
        {'id': 6, 'name': 'Random', 'icon': '🌀', 'members': 20, 'hot': False, 'recommended': True, 'last_message': '😂 Did you see that meme?'},
    ]
    
    user_rooms = request.session.get('rooms', [])
    all_rooms = default_rooms + user_rooms
    
    context = {
        'username': request.session.get('username'),
        'rooms': all_rooms,
    }
    return render(request, 'chat_rooms.html', context)

def profile(request):
    if not request.session.get('username'):
        return redirect('/choose-username/')
    
    user = None
    if request.session.get('user_id'):
        try:
            user = AnonymousUser.objects.get(user_id=request.session.get('user_id'))
        except AnonymousUser.DoesNotExist:
            pass
    
    if not user:
        username = request.session.get('username')
        try:
            user = AnonymousUser.objects.get(display_name=username)
        except AnonymousUser.DoesNotExist:
            user = AnonymousUser.objects.create(
                user_id=AnonymousUser.generate_id(),
                display_name=username,
                ip_address=request.META.get('REMOTE_ADDR'),
                user_agent=request.META.get('HTTP_USER_AGENT', ''),
                bio='Just a soul wandering through anonymous conversations.'
            )
            request.session['user_id'] = user.user_id
    
    context = {
        'username': user.display_name,
        'display_name': user.display_name,
        'user_id': user.user_id,
        'bio': user.bio,
        'avatar': user.get_avatar_url() if user.avatar else None,
        'join_date': user.created_at.strftime('%B %Y'),
        'messages_count': 0,
        'friends_count': 0,
        'rooms_created': 0,
        'karma': user.karma,
    }
    return render(request, 'profile.html', context)

def update_profile(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=400)
    
    username = request.session.get('username')
    if not username:
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    try:
        user = AnonymousUser.objects.get(display_name=username)
    except AnonymousUser.DoesNotExist:
        user = AnonymousUser.objects.create(
            user_id=AnonymousUser.generate_id(),
            display_name=username,
            ip_address=request.META.get('REMOTE_ADDR'),
            user_agent=request.META.get('HTTP_USER_AGENT', ''),
            bio='Just a soul wandering through anonymous conversations.'
        )
        request.session['user_id'] = user.user_id
    
    display_name = request.POST.get('display_name')
    bio = request.POST.get('bio')
    
    if display_name:
        user.display_name = display_name
        request.session['username'] = display_name
        request.session['display_name'] = display_name
    if bio:
        user.bio = bio
        request.session['bio'] = bio
    
    user.save()
    
    return JsonResponse({'success': True})

def update_avatar(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=400)
    
    username = request.session.get('username')
    if not username:
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    try:
        user = AnonymousUser.objects.get(display_name=username)
    except AnonymousUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    if request.FILES.get('avatar'):
        user.avatar = request.FILES['avatar']
        user.save()
        return JsonResponse({'success': True, 'avatar_url': user.avatar.url})
    
    return JsonResponse({'error': 'No file provided'}, status=400)

def create_room(request):
    if not request.session.get('username'):
        return redirect('/choose-username/')
    
    if request.method == 'POST':
        room_name = request.POST.get('room_name', '').strip()
        room_icon = request.POST.get('room_icon', '💬')
        
        if room_name:
            if 'rooms' not in request.session:
                request.session['rooms'] = []
            
            rooms = request.session['rooms']
            new_id = max([room['id'] for room in rooms] + [0]) + 1 if rooms else 1
            
            rooms.append({
                'id': new_id,
                'name': room_name,
                'icon': room_icon,
                'members': 0,
                'created_by': request.session.get('username'),
            })
            request.session['rooms'] = rooms
            request.session.modified = True
            
            return redirect('/chat/')
    
    return redirect('/chat/')

def chat_room(request, room_id):
    if not request.session.get('username'):
        return redirect('/choose-username/')
    
    room = None
    default_rooms = [
        {'id': 1, 'name': 'General', 'icon': '💬'},
        {'id': 2, 'name': 'Technology', 'icon': '💻'},
        {'id': 3, 'name': 'Art & Design', 'icon': '🎨'},
        {'id': 4, 'name': 'Gaming', 'icon': '🎮'},
        {'id': 5, 'name': 'Music', 'icon': '🎵'},
        {'id': 6, 'name': 'Random', 'icon': '🌀'},
    ]
    user_rooms = request.session.get('rooms', [])
    all_rooms = default_rooms + user_rooms
    
    for r in all_rooms:
        if r['id'] == room_id:
            room = r
            break
    
    if not room:
        return redirect('/chat/')
    
    context = {
        'username': request.session.get('username'),
        'room': room,
    }
    return render(request, 'chat_room.html', context)

# ===== Sitemap =====
def sitemap(request):
    xml = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>https://127.0.0.1:8000/</loc>
        <changefreq>daily</changefreq>
        <priority>1.0</priority>
    </url>
    <url>
        <loc>https://127.0.0.1:8000/chat/</loc>
        <changefreq>hourly</changefreq>
        <priority>0.9</priority>
    </url>
    <url>
        <loc>https://127.0.0.1:8000/choose-username/</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>
</urlset>"""
    return HttpResponse(xml, content_type='application/xml')

# ===== Admin Panel =====
def admin_panel(request):
    if request.META.get('REMOTE_ADDR') != '127.0.0.1':
        return redirect('/')
    
    users = AnonymousUser.objects.all()
    messages = ChatMessage.objects.all().order_by('-created_at')[:20]
    
    context = {
        'users': users,
        'messages': messages,
    }
    return render(request, 'admin_panel.html', context)

# ==========================================
# Google Search Console Verification
# ==========================================

def google_verification(request):
    return HttpResponse("""
    <!DOCTYPE html>
    <html>
    <head>
        <meta name="google-site-verification" content="SWq2tKZQ33oqwYC0-3TMdxG_Jt2pXWe3L9GR8eAgDlw" />
    </head>
    <body>
        Google Search Console verification
    </body>
    </html>
    """)

# ==========================================
# سیستم دوست‌یابی
# ==========================================

def friend_list(request):
    """لیست دوستان کاربر"""
    if not request.session.get('username'):
        return redirect('/choose-username/')
    
    username = request.session.get('username')
    try:
        user = AnonymousUser.objects.get(display_name=username)
    except AnonymousUser.DoesNotExist:
        return redirect('/choose-username/')
    
    # پیدا کردن دوستان (درخواست‌های پذیرفته شده)
    friends = []
    sent_accepted = FriendRequest.objects.filter(from_user=user, status='accepted').select_related('to_user')
    received_accepted = FriendRequest.objects.filter(to_user=user, status='accepted').select_related('from_user')
    
    for req in sent_accepted:
        friends.append(req.to_user)
    for req in received_accepted:
        friends.append(req.from_user)
    
    # درخواست‌های ارسال‌شده (در انتظار)
    sent_requests = FriendRequest.objects.filter(from_user=user, status='pending').select_related('to_user')
    
    # درخواست‌های دریافت‌شده (در انتظار)
    received_requests = FriendRequest.objects.filter(to_user=user, status='pending').select_related('from_user')
    
    context = {
        'username': username,
        'user': user,
        'friends': friends,
        'sent_requests': sent_requests,
        'received_requests': received_requests,
    }
    return render(request, 'friend_list.html', context)

def send_friend_request(request):
    """ارسال درخواست دوستی"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=400)
    
    if not request.session.get('username'):
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    username = request.session.get('username')
    target_username = request.POST.get('target_username')
    
    if not target_username:
        return JsonResponse({'error': 'Target username is required'}, status=400)
    
    try:
        from_user = AnonymousUser.objects.get(display_name=username)
        to_user = AnonymousUser.objects.get(display_name=target_username)
    except AnonymousUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    if from_user == to_user:
        return JsonResponse({'error': 'You cannot send a friend request to yourself'}, status=400)
    
    existing, created = FriendRequest.objects.get_or_create(
        from_user=from_user,
        to_user=to_user,
        defaults={'status': 'pending'}
    )
    
    if not created:
        if existing.status == 'pending':
            return JsonResponse({'error': 'Request already sent'}, status=400)
        elif existing.status == 'accepted':
            return JsonResponse({'error': 'Already friends'}, status=400)
        else:
            existing.status = 'pending'
            existing.save()
            return JsonResponse({'success': True, 'message': 'Request resent'})
    
    return JsonResponse({'success': True, 'message': 'Friend request sent'})

def accept_friend_request(request, request_id):
    """پذیرش درخواست دوستی"""
    if not request.session.get('username'):
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    try:
        req = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return JsonResponse({'error': 'Request not found'}, status=404)
    
    username = request.session.get('username')
    if req.to_user.display_name != username:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    req.status = 'accepted'
    req.save()
    
    return JsonResponse({'success': True, 'message': 'Friend request accepted'})

def reject_friend_request(request, request_id):
    """رد درخواست دوستی"""
    if not request.session.get('username'):
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    try:
        req = FriendRequest.objects.get(id=request_id)
    except FriendRequest.DoesNotExist:
        return JsonResponse({'error': 'Request not found'}, status=404)
    
    username = request.session.get('username')
    if req.to_user.display_name != username:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    req.status = 'rejected'
    req.save()
    
    return JsonResponse({'success': True, 'message': 'Friend request rejected'})

def get_or_create_private_room(request):
    """پیدا کردن یا ایجاد چت خصوصی با یک دوست"""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid method'}, status=400)
    
    if not request.session.get('username'):
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    username = request.session.get('username')
    friend_username = request.POST.get('friend_username')
    
    if not friend_username:
        return JsonResponse({'error': 'Friend username is required'}, status=400)
    
    try:
        user = AnonymousUser.objects.get(display_name=username)
        friend = AnonymousUser.objects.get(display_name=friend_username)
    except AnonymousUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    # بررسی دوست بودن
    is_friend = FriendRequest.objects.filter(
        (Q(from_user=user, to_user=friend) | Q(from_user=friend, to_user=user)),
        status='accepted'
    ).exists()
    
    if not is_friend:
        return JsonResponse({'error': 'You are not friends with this user'}, status=403)
    
    # پیدا کردن یا ایجاد چت خصوصی
    room = PrivateChatRoom.objects.filter(
        (Q(user1=user, user2=friend) | Q(user1=friend, user2=user))
    ).first()
    
    if not room:
        room = PrivateChatRoom.objects.create(user1=user, user2=friend)
    
    return JsonResponse({'success': True, 'room_id': room.id})

# ==========================================
# چت خصوصی
# ==========================================

def private_chat_room(request, room_id):
    """نمایش چت خصوصی"""
    if not request.session.get('username'):
        return redirect('/choose-username/')
    
    username = request.session.get('username')
    try:
        user = AnonymousUser.objects.get(display_name=username)
    except AnonymousUser.DoesNotExist:
        return redirect('/choose-username/')
    
    try:
        room = PrivateChatRoom.objects.get(id=room_id)
    except PrivateChatRoom.DoesNotExist:
        return redirect('/friend-list/')
    
    if room.user1 != user and room.user2 != user:
        return redirect('/friend-list/')
    
    other_user = room.get_other_user(user)
    
    context = {
        'username': username,
        'room_id': room_id,
        'other_user': other_user,
        'room': room,
    }
    return render(request, 'private_chat.html', context)

def get_private_rooms(request):
    """دریافت لیست چت‌های خصوصی کاربر"""
    if not request.session.get('username'):
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    username = request.session.get('username')
    try:
        user = AnonymousUser.objects.get(display_name=username)
    except AnonymousUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    rooms = PrivateChatRoom.objects.filter(user1=user) | PrivateChatRoom.objects.filter(user2=user)
    
    data = []
    for room in rooms:
        other = room.get_other_user(user)
        last_msg = room.messages.order_by('-created_at').first()
        unread = room.messages.filter(is_read=False).exclude(sender=user).count()
        
        data.append({
            'id': room.id,
            'other_user': other.display_name,
            'last_message': last_msg.content[:50] if last_msg else 'No messages yet',
            'last_time': last_msg.created_at.strftime('%H:%M') if last_msg else '',
            'unread': unread,
        })
    
    return JsonResponse({'rooms': data})

def get_private_messages(request, room_id):
    """دریافت پیام‌های چت خصوصی"""
    if not request.session.get('username'):
        return JsonResponse({'error': 'Not logged in'}, status=401)
    
    username = request.session.get('username')
    try:
        user = AnonymousUser.objects.get(display_name=username)
    except AnonymousUser.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)
    
    try:
        room = PrivateChatRoom.objects.get(id=room_id)
    except PrivateChatRoom.DoesNotExist:
        return JsonResponse({'error': 'Room not found'}, status=404)
    
    if room.user1 != user and room.user2 != user:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    messages = room.messages.all()
    messages.filter(is_read=False).exclude(sender=user).update(is_read=True)
    
    data = []
    for msg in messages:
        data.append({
            'id': msg.id,
            'sender': msg.sender.display_name,
            'content': msg.content,
            'is_self': msg.sender == user,
            'created_at': msg.created_at.strftime('%H:%M'),
        })
    
    return JsonResponse({'messages': data})
