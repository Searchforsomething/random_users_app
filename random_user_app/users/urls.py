from django.urls import path
from .views import UserListView, UserDetailView, RandomUserView

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<int:id>/', UserDetailView.as_view(), name='user-detail'),
    path('random/', RandomUserView.as_view(), name='random-user'),

]
