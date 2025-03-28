from django.urls import path
from volunteers.views import index

urlpatterns = [
    path('', index, name='volunteers-index'),
]