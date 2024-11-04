from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import get_message, EmployeeListCreateView, CoverShiftDetail, CoverShiftDelete, CreateUserView
# from .views import CreateUserView

urlpatterns = [
    path('message/', get_message),
    path('user/register/', CreateUserView.as_view(), name='register_user'),
    path('employee/register/', EmployeeListCreateView.as_view(), name='employee_list_create'),
    path('cover_shift/', CoverShiftDetail.as_view()),
    path('cover_shift/<int:pk>/', CoverShiftDelete.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)