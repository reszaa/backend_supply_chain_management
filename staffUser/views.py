# --- IMPORT WAJIB DJANGO REST FRAMEWORK ---
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import ProfilStaff
from .serializers import UserDataSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def login_staff(request):
    username = request.data.get('username')
    password = request.data.get('password')

    user = authenticate(username=username, password=password)
    
    if user is not None:
        if not user.is_active:
            return Response({'success': False, 'message': 'Akun dinonaktifkan oleh Admin.'}, status=status.HTTP_403_FORBIDDEN)
            
        token, created = Token.objects.get_or_create(user=user)
        serializer = UserDataSerializer(user)
        
        return Response({
            'success': True,
            'message': 'Login berhasil!',
            'token': token.key,
            'data': serializer.data
        }, status=status.HTTP_200_OK)
        
    return Response({'success': False, 'message': 'Username atau password salah!'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@permission_classes([AllowAny]) 
def kelola_staff(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email', '')
    
    id_staff = request.data.get('id_staff')
    nama_lengkap = request.data.get('nama_lengkap')
    role = request.data.get('role', 'WAREHOUSE')
    no_telp = request.data.get('no_telp', '')

    if not username or not password or not id_staff or not nama_lengkap:
        return Response({
            'success': False, 
            'message': 'Username, password, ID Staff, dan Nama Lengkap wajib diisi!'
        }, status=status.HTTP_400_BAD_REQUEST)

    if User.objects.filter(username=username).exists():
        return Response({'success': False, 'message': 'Username sudah digunakan oleh staf lain.'}, status=status.HTTP_400_BAD_REQUEST)
    
    if ProfilStaff.objects.filter(id_staff=id_staff).exists():
        return Response({'success': False, 'message': 'ID Staff sudah terdaftar di sistem.'}, status=status.HTTP_400_BAD_REQUEST)

    try:
        user = User.objects.create_user(username=username, email=email, password=password)
        
        ProfilStaff.objects.create(
            user=user,
            id_staff=id_staff,
            nama_lengkap=nama_lengkap,
            role=role,
            no_telp=no_telp
        )
        
        return Response({
            'success': True, 
            'message': f'Akun untuk {nama_lengkap} berhasil dibuat!'
        }, status=status.HTTP_201_CREATED)
        
    except Exception as e:
        return Response({'success': False, 'message': f'Terjadi kesalahan: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cek_profil_saya(request):
    user = request.user
    
    if not hasattr(user, 'profil'):
        return Response({
            "success": False,
            "message": "Akun ini tidak memiliki Profil Staff Pracindo."
        }, status=status.HTTP_403_FORBIDDEN)

    serializer = UserDataSerializer(user)
    
    return Response({
        "success": True,
        "data": serializer.data
    }, status=status.HTTP_200_OK)