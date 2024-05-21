from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='index'),
    path('questions/<int:question_id>', views.question, name='question'),
]
