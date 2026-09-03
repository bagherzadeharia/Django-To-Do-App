from todo.views import *
from django.urls import path

app_name = 'todo'

urlpatterns = [
    path('', ToDoListView.as_view(), name="list"),
    path('check/<int:id>', ToDoCheckView.as_view(), name='check'),
    path('edit/<int:pk>', ToDoEditView.as_view(), name='edit'),
    path('create/', ToDoCreateView.as_view(), name='create'),
    path('delete/<int:id>', ToDoDeleteView.as_view(), name='delete'),
]