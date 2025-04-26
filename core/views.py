from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated
from .models import Client, Project
from .serializers import (
    ClientSerializer, ClientDetailSerializer,
    ProjectSerializer, ProjectCreateSerializer
)

# ViewSet for Client

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ClientDetailSerializer
        return ClientSerializer

    def perform_create(self, serializer):
        # This allows either passing 'created_by' manually or defaulting to the current user
        if not serializer.validated_data.get('created_by'):
            serializer.save(created_by=self.request.user)
        else:
            serializer.save()
# ViewSet for Project
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ProjectCreateSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user.username)

# API view for listing projects for the authenticated user
class UserProjectListAPIView(generics.ListAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Project.objects.filter(users=self.request.user)

# API view for deleting a client
class ClientDeleteAPIView(generics.DestroyAPIView):
    queryset = Client.objects.all()
    permission_classes = [IsAuthenticated]

# API view for deleting a project
class ProjectDeleteAPIView(generics.DestroyAPIView):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated]

# Detail view for a specific client
class ClientDetailView(generics.RetrieveAPIView):
    queryset = Client.objects.all()
    serializer_class = ClientDetailSerializer
    permission_classes = [IsAuthenticated]
