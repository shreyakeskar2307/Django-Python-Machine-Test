from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ClientViewSet,
    ProjectViewSet,
    UserProjectListAPIView,
    ClientDeleteAPIView,
    ProjectDeleteAPIView,
    ClientDetailView
)

# Create a router for Client and Project ViewSets
router = DefaultRouter()
router.register(r'clients', ClientViewSet, basename='client')
router.register(r'projects', ProjectViewSet, basename='project')

urlpatterns = [
    # Include all the router URLs for Client and Project ViewSets
    path('', include(router.urls)),

    # Custom API paths for user-specific projects, and deleting clients/projects
    path('my-projects/', UserProjectListAPIView.as_view(), name='user-projects'),
    path('clients/<int:pk>/delete/', ClientDeleteAPIView.as_view(), name='delete-client'),
    path('projects/<int:pk>/delete/', ProjectDeleteAPIView.as_view(), name='delete-project'),

    # Path for client detail view
    path('clients/<int:pk>/', ClientDetailView.as_view(), name='client-detail'),
]
