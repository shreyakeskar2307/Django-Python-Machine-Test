from rest_framework import serializers
from .models import Client, Project
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class ProjectSerializer(serializers.ModelSerializer):
    client = serializers.StringRelatedField()
    users = UserSerializer(many=True, read_only=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'client', 'users', 'start_date', 'end_date']

class ProjectCreateSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), many=True)

    class Meta:
        model = Project
        fields = ['id', 'name', 'client', 'users', 'assigned_to', 'start_date', 'end_date']

class ClientSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    created_by_username = serializers.StringRelatedField(source='created_by', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'name', 'email', 'created_by', 'created_by_username']

class ClientDetailSerializer(serializers.ModelSerializer):
    projects = serializers.SerializerMethodField()
    created_by = serializers.CharField(source='created_by.username')

    class Meta:
        model = Client
        fields = ['id', 'name', 'projects', 'email', 'created_at', 'updated_at', 'created_by']

    def get_projects(self, obj):
        projects = Project.objects.filter(client=obj)
        return ProjectSerializer(projects, many=True).data
    