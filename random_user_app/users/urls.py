from django.urls import path

from .views import UserListView, UserDetailView, RandomUserView, trigger_load_users

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('random/', RandomUserView.as_view(), name='random-user'),
    path("load_users/", trigger_load_users, name="load_users"),
]
