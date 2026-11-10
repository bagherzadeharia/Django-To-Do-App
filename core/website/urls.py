from django.urls import path, include
from website.views import indexView

app_name = 'website'

urlpatterns = [
    path('', indexView, name='index')
]
