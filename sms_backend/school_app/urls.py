from rest_framework.routers import DefaultRouter
from .views import *
from django.urls import path, include
from school_app import views
router = DefaultRouter()
router.register(r'class', ClassroomViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('students/', views.StudentView.as_view()),
    path('teachers/', views.TeacherView.as_view()),
    path('subjects/', views.SubjectView.as_view()),
]
