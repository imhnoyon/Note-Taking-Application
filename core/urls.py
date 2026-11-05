from django.contrib import admin
from django.urls import path
from .views import *         

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('getme/', ProfileAPIView.as_view(), name='getme'),
    path('create/note/', NoteCreateAPIView.as_view(), name='create-note'),
    path('notes/<str:pk>/', NoteCreateAPIView.as_view(), name='note-detail'),
    path('update/note/<str:pk>/', NoteCreateAPIView.as_view(), name='update-note'),
    path('note-list/', NoteListAPIView.as_view(), name='note-list'),

    # admin 
    path('user-list/', UserListAPIView.as_view(), name='user-list'),
    path('user/<str:pk>/', UserRetrieveUpdateAPIView.as_view(), name='user'),
    path('note-lists/', AdminNoteListAPIView.as_view(), name='notes-list'),
    path('admin/updates/note/<str:pk>/', AdminNoteListAPIView.as_view(), name='notes-update'),
    path('admin/delete/note/<str:pk>/', AdminNoteListAPIView.as_view(), name='delete-notes'),
    path('admin/users/grouped-by-interests/', UserGroupedByInterestsAPIView.as_view(), name='users-grouped-by-interests'),
    path("users/<str:user_id>/posts/",UserPostsAPIView.as_view(),name="user-posts"),
]
