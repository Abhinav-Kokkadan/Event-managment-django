from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import EventList

# DRF Router setup for API URLs
router = DefaultRouter()
router.register(r'events', views.EventViewSet)
router.register(r'attendees', views.AttendeeViewSet)

urlpatterns = [
    # HTML views URLs
    path('', views.event_list, name='event_list'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('event/new/', views.event_create, name='event_create'),
    path('event/<int:pk>/edit/', views.event_update, name='event_update'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),
    path('event/<int:pk>/register/', views.register, name='register'),
    path('', include(router.urls)),
    path('api/events/', EventList.as_view(), name='event-list'),

    # API URLs
    path('api/', include(router.urls)),
    path('api-auth/', include('rest_framework.urls')),

    # Updated route for date_sort function with optional date parameter
    path('api/date_sort/', views.date_sort, name='date_sort'),
    path('api/date_sort/<str:date>/', views.date_sort, name='date_sort_with_date'),
]
