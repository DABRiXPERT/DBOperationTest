"""
URL configuration for DBOperationTest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from Main import views

urlpatterns = [
    path('', views.index, name='index'),
    path('upload_csv/', views.upload_csv, name='upload_csv'),
    path('resolve_conflicts', views.resolve_conflicts, name='resolve_conflicts'),
    path('show/', views.show_data, name='show_data'),
    path('delete_row/<int:id>/', views.delete_row, name='delete_row'),
    path('clear_data/', views.clear_data, name='clear_data'),
    path('update_row/<int:id>/', views.update_row, name='update_row'),
    path('data_visualize/', views.data_visualize, name='data_visualize'),
]


