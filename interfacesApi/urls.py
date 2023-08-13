from django.urls import path
from rest_framework import routers
from . import views
from .views import device_messages_hndlr
from django.urls import path, include
router = routers.DefaultRouter()
router.register(r'messages-Data', device_messages_hndlr)

urlpatterns = [
    path('', views.index, name="index"),
    path('upload_file', views.upload_file, name="upload_file"),
    path('list_files/', views.list_files, name="list_files"),
    # path('download_file/<int:file_id>/', views.download_file, name="download_file"),
    # path('delete_file/<int:file_id>/', views.delete_file, name="delete_file"),
    path('get_diag_messages',views.get_diag_messages,name='get_diag_messages'),
    path('api/', include(router.urls)),
]
