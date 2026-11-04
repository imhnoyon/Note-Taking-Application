from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Note, User
from .permissions import IsAdminRole, IsUserRole
from .serializers import *
from rest_framework.pagination import PageNumberPagination

class UserListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class RegisterView(APIView):

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                'success': True,
                'message': 'Registration successful',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            'success': False,
            'message': 'Registration failed',
            'errors': serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)



class LoginView(APIView):

    def post(self, request):

        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({
                'success': False,
                'message': 'Username and password are required'
            }, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(
            username=username,
            password=password
        )

        if user is not None:

            refresh = RefreshToken.for_user(user)

            return Response({
                'success': True,
                'message': 'Login successful',
                'data': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'access': str(refresh.access_token),
                    'refresh': str(refresh)
                }
            }, status=status.HTTP_200_OK)

        return Response({
            'success': False,
            'message': 'Invalid username or password'
        }, status=status.HTTP_401_UNAUTHORIZED)


class NoteCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = NoteSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(user=request.user)

            return Response({
                "success": True,
                "message": "Note created successfully.",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, pk):
        try:
            note = Note.objects.get(pk=pk, user=request.user)

        except Note.DoesNotExist:
            return Response({
                "success": False,
                "message": "Note not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(note)

        return Response({
            "success": True,
            "message": "Note retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def patch(self, request, pk):
        try:
            note = Note.objects.get(pk=pk, user=request.user)
        except Note.DoesNotExist:
            return Response({
                "success": False,
                "message": "Note not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(note,data=request.data,partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Note updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            note = Note.objects.get(pk=pk, user=request.user)
        except Note.DoesNotExist:
            return Response({
                "success": False,
                "message": "Note not found."
            }, status=status.HTTP_404_NOT_FOUND)

        note.delete()

        return Response({
            "success": True,
            "message": "Note deleted successfully."
        }, status=status.HTTP_200_OK)



     
class NoteListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notes = Note.objects.filter(user=request.user).order_by('-created_at')

        serializer = NoteSerializer(notes, many=True)

        return Response({
            "success": True,
            "message": "Notes retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)




class UserListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    pagination_class = UserListPagination

    def get(self, request):
        users = User.objects.exclude(
            role=User.Role.ADMIN
        ).order_by('-id')

        paginator = self.pagination_class()
        paginated_users = paginator.paginate_queryset(users, request)

        serializer = UserlistSerializer(paginated_users, many=True)

        return Response({
            "success": True,
            "message": "Users retrieved successfully.",
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)
        serializer = UserlistSerializer(user)
        return Response({
            "success": True,
            "message": "User retrieved successfully.",
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def patch(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = UserlistSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "User updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)  


    def delete(self,request,pk):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({
                "success": False,
                "message": "User not found."
            }, status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response({
            "success": True,
            "message": "User deleted successfully."
        }, status=status.HTTP_200_OK)   




class AdminNoteListAPIView(APIView):
    permission_classes = [IsAuthenticated, IsAdminRole]
    pagination_class = UserListPagination

    def get(self, request):
        notes = Note.objects.all().select_related('user').order_by('-created_at')

        paginator = self.pagination_class()
        paginated_notes = paginator.paginate_queryset(notes, request)

        serializer = NoteSerializer(paginated_notes, many=True)

        return Response({
            "success": True,
            "message": "All notes retrieved successfully.",
            "count": paginator.page.paginator.count,
            "next": paginator.get_next_link(),
            "previous": paginator.get_previous_link(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)


    def patch(self,request,pk):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response({
                "success": False,
                "message": "Note not found."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = NoteSerializer(note,data=request.data,partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Note updated successfully.",
                "data": serializer.data
            }, status=status.HTTP_200_OK)

        return Response({
            "success": False,
            "message": "Validation failed.",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)  

    def delete(self,request,pk):
        try:
            note = Note.objects.get(pk=pk)
        except Note.DoesNotExist:
            return Response({
                "success": False,
                "message": "Note not found."
            }, status=status.HTTP_404_NOT_FOUND)
        note.delete()
        return Response({
            "success": True,
            "message": "Note deleted successfully."
        }, status=status.HTTP_200_OK)   