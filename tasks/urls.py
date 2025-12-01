from django.urls import path, include
from rest_framework import routers
from tasks.views import TaskViewSet, NotificationViewSet, login_view, logout_view, dashboard, task_create, task_list
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = routers.DefaultRouter
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('api/', include(routers.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('', dashboard, name='dashboard'),
    path('tasks/create/', task_create, name='task_create'),
    path('tasks/', task_list, name='task_list'),
]