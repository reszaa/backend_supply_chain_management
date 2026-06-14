from rest_framework import serializers
from django.contrib.auth.models import User
from .models import ProfilStaff

class ProfilStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilStaff
        fields = ['id_staff', 'nama_lengkap', 'role', 'no_telp', 'foto_profil', 'is_active']

class UserDataSerializer(serializers.ModelSerializer):
    profil = ProfilStaffSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'profil']