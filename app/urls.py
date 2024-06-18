from django.conf.urls.static import static
from django.urls import path

from AskMe_Shakleina import settings
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
    path('log_out/', views.log_out, name='log_out'),
    path('questions/<int:question_id>/like_question/', views.like_question, name='like_question'),
    path('answers/<int:answer_id>/like_answer/', views.like_answer, name='like_answer'),
    path('questions/<int:question_id>/answers/<int:answer_id>/mark_correct/', views.mark_correct_answer,
         name='mark_correct_answer'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
