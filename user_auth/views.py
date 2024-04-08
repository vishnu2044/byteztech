from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout
from .models import UserDetails, UploadedFile
from django.contrib import messages
from django.http import JsonResponse
import jwt
from django.conf import settings
from .forms import UploadForm
import os

def generate_jwt_token(user):
    payload = {
        'user_id': user.id,
        'username': user.username,
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return {'token': token} 


def login(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = User.objects.filter(email=email).first()
        if user:
            user = authenticate(username=user.username, password=password)
            
            if user:
                token = generate_jwt_token(user)    
                return JsonResponse(token, status=200)  
            else:
                return JsonResponse({'message': 'Invalid email or password'}, status=401)
        else:
            return JsonResponse({'message': 'User does not exist'}, status=404)

    return render(request, 'login.html')


def validate_token(request):
    if request.method == "POST":
        token = request.POST.get('token')
        if token:
            user = validate_jwt_token(token)
            if user:
                return JsonResponse({'message': 'Token is valid'}, status=200)
            else:
                return JsonResponse({'message': 'Invalid token'}, status=401)
        else:
            return JsonResponse({'message': 'Token not provided'}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=400)


def validate_jwt_token(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        user_id = payload['user_id']
        user = User.objects.get(id=user_id)
        return user
    except jwt.ExpiredSignatureError:
        return None
    except (jwt.InvalidTokenError, User.DoesNotExist):
        return None


def profile(request):
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        return render(request, 'profile.html')
    else:
        return render(request, 'profile.html', {'error_message': 'Token missing or invalid'})


def get_profile_details(request):
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
        user = validate_jwt_token(token)
        if user:
            full_name = f"{user.first_name} {user.last_name}"
            context = {
                'username': user.username,
                'fullname': full_name,
                'email': user.email
            }
            return JsonResponse(context)
        else:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
    else:
        return JsonResponse({'error': 'Authorization token missing or invalid'}, status=401)


def upload_page(request):
    form = UploadForm(request.POST or None, request.FILES or None)
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        token = request.headers.get('Authorization').split(' ')[1]
        file_data = request.FILES.get('file')
        print("Token:", token) 
        user = validate_jwt_token(token)
        if file_data:
            file_extension = os.path.splitext(file_data.name)[1].lower()

            file_size = file_data.size
            print("File size:", file_size, "bytes")

            if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                file_type = 'image'
            elif file_extension in ['.mp4', '.avi', '.mov', '.mkv']:
                file_type = 'video'
            elif file_extension in ['.pdf', '.doc', '.docx', '.txt']:
                file_type = 'document'
            else:
                file_type = 'unknown'

            UploadedFile.objects.create(user = user, file=file_data, file_type=file_type, file_size=file_size)

            print("File type:", file_type)
            print("File data:", file_data)

    return render(request, 'file_upload.html')


from django.http import JsonResponse

def get_all_files(request):
    token = request.headers.get('Authorization')
    if token and token.startswith('Bearer '):
        token = token.split(' ')[1]
        user = validate_jwt_token(token)
        if user:
            user_files = UploadedFile.objects.filter(user=user)
            files_data = [
                {
                    'filename': file.file.name[8::],
                    'file_type': file.file_type,
                    'file_size': file.file_size
                }
                for file in user_files
            ]
            return JsonResponse({'files_data': files_data})
        else:
            return JsonResponse({'error': 'Invalid or expired token'}, status=401)
    else:
        return JsonResponse({'error': 'Authorization token missing or invalid'}, status=401)

    
def signup(request):

    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        
        if not all([username, email, first_name, last_name, password, phoneno]):
            return JsonResponse({'message': 'Please fill in all the fields.'}, status=400)
        
        if User.objects.filter(username=username).exists():
            return JsonResponse({'message': 'Username already exists.'}, status=400)
            
        user = User.objects.create_user(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            password=password
        )
        UserDetails.objects.create(user=user, phone_no=phoneno)
        
        messages.success(request, 'Account created successfully. Please login.')
        return JsonResponse({'redirect': '/login'})
    
    return render(request, 'signup.html')


def user_logout(request):
    try:
        print("function si calling::::::::::::::::::")
        if request.user.is_authenticated:
            logout(request)
            return redirect('login')
        else:
            messages.error(request, 'You need to login first')
            return redirect('login')
    except:
        return redirect('login')