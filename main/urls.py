from django.urls import path
from .views import index
from .views import other_page
from .views import NewsBoardLoginView
from .views import profile
from .views import NewsBoardLogoutView
from .views import ChangeUserInfoView
from .views import NewsBoardPasswordChangeView
from .views import RegisterUserView, RegisterDoneView
from .views import user_activate
from .views import DeleteUserView


app_name = 'main'
urlpatterns = [
    path('<str:page>/', other_page, name='other'),
    path('', index, name='index'),
    path('accounts/register/', RegisterUserView.as_view(),
         name='register'),
    path('accounts/register/activate/<str:sign>/', user_activate,
         name='register_activate'),
    path('accounts/register/done/', RegisterDoneView.as_view(),
         name='register_done'),
    path('accounts/login/', NewsBoardLoginView.as_view(), name='login'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/delete/', DeleteUserView.as_view(),
         name='profile_delete'),
    path('accounts/profile/change/', ChangeUserInfoView.as_view(),
         name='profile_change'),
    path('accounts/password/change/', NewsBoardPasswordChangeView.as_view(),
         name='password_change'),
    path('accounts/logout/', NewsBoardLogoutView.as_view(), name='logout'),

]
