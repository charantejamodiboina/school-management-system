from django.urls import path
from .views import (
    LoginView, LogoutView,
    TeacherApplicationView, TeacherDashboardView,
    StudentSignupView, StudentDashboardView,
    AdminApprovalView, NoticeView
)

urlpatterns = [
    # Login/Logout URLs
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Teacher URLs
    path('teacher/apply/', TeacherApplicationView.as_view(), name='teacher-apply'),
    path('teacher/dashboard/', TeacherDashboardView.as_view(), name='teacher-dashboard'),

    # Student URLs
    path('student/signup/', StudentSignupView.as_view(), name='student-signup'),
    path('student/dashboard/', StudentDashboardView.as_view(), name='student-dashboard'),

    # Admin URLs
    path('admin/approvals/', AdminApprovalView.as_view(), name='admin-approvals'),
    path('admin/approve/<int:user_id>/', AdminApprovalView.as_view(), name='admin-approve-user'),

    # Notice URLs
    path('notices/', NoticeView.as_view(), name='notices'),
]
