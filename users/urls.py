from django.urls import path, include

from users import views


urlpatterns = [
    path('<int:pk_user>/', views.TableTopUserView.as_view(), name='user-detail'),
]