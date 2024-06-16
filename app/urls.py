from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('questions/<int:question_id>', views.question, name='question'),
    path('ask/', views.ask, name='ask'),
    path('log_in/', views.log_in, name='log_in'),
    path('signup/', views.signup, name='signup'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('tag/<str:tag_name>', views.tag, name='tag'),
    path('log_out/', views.log_out, name='log_out')
]
