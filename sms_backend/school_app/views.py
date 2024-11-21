from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from django.contrib.auth import authenticate, login, logout
from .models import User, Teacher, Student, Attendance, Notice
from .serializers import (
    UserSerializer,
    TeacherSerializer,
    StudentSerializer,
    AttendanceSerializer,
    NoticeSerializer
)

# Login View
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            if not user.is_approved:
                return Response({"error": "Account is not approved by the admin."}, status=status.HTTP_403_FORBIDDEN)
            login(request, user)
            return Response({"message": "Login successful", "role": user.role}, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

# Logout View
class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

# Teacher Views
class TeacherApplicationView(APIView):
    def post(self, request):
        serializer = TeacherSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Application submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'teacher' or not request.user.is_approved:
            return Response({"error": "Unauthorized or account not approved"}, status=status.HTTP_403_FORBIDDEN)
        attendance = Attendance.objects.filter(student__teacher=request.user.teacher_profile)
        notices = Notice.objects.filter(published_by=request.user)
        data = {
            "attendance": AttendanceSerializer(attendance, many=True).data,
            "notices": NoticeSerializer(notices, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

# Student Views
class StudentSignupView(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({"message": "Signup submitted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StudentDashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'student' or not request.user.is_approved:
            return Response({"error": "Unauthorized or account not approved"}, status=status.HTTP_403_FORBIDDEN)
        attendance = Attendance.objects.filter(student=request.user.student_profile)
        data = {
            "attendance": AttendanceSerializer(attendance, many=True).data,
        }
        return Response(data, status=status.HTTP_200_OK)

# Admin Views
class AdminApprovalView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        if request.user.role != 'admin':
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        pending_users = User.objects.filter(is_approved=False)
        serializer = UserSerializer(pending_users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, user_id):
        if request.user.role != 'admin':
            return Response({"error": "Unauthorized"}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(id=user_id)
            user.is_approved = True
            user.save()
            return Response({"message": f"{user.username} has been approved!"}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

# Notice Views
class NoticeView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Notice.objects.all()
    serializer_class = NoticeSerializer

    def perform_create(self, serializer):
        serializer.save(published_by=self.request.user)
