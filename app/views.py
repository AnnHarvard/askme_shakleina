from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth import authenticate, login
from django.contrib import auth
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods

from app.forms import LoginForm, RegisterForm, ProfileEditForm, QuestionForm, AnswerForm
from app.models import *

# Create your views here.
QUESTIONS = [
    {
        'id': i,
        "title": f"Question {i}",
        "text": f"This is question number {i}"
    } for i in range(200)
]
ANSWERS = [
    {
        "id": i,
        "title": f"Answer {i}",
        "text": f"This is answer number {i}"
    } for i in range(20)
]


def paginate(objects_list, request, per_page=10):
    page_num = request.GET.get('page', 1)
    paginator = Paginator(objects_list, per_page)
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return page_obj


@login_required(login_url='log_in/', redirect_field_name='continue')
def index(request):
    liked_questions = QuestionLike.objects.filter(user=request.user).values_list('question_id', flat=True)

    popular_tags = Tag.objects.get_popular()
    questions = Question.objects.new()
    page_obj = paginate(questions, request, per_page=5)
    return render(request, 'index.html',
                  {"questions": page_obj, 'popular_tags': popular_tags, 'username': request.user.username,
                   'liked_questions': liked_questions})


def hot(request):
    liked_questions = QuestionLike.objects.filter(user=request.user).values_list('question_id', flat=True)

    popular_tags = Tag.objects.get_popular()
    questions = Question.objects.hot()
    page_obj = paginate(questions, request, per_page=5)
    return render(request, 'hot.html',
                  {"questions": page_obj, 'popular_tags': popular_tags, 'username': request.user.username,
                   'liked_questions': liked_questions})


@login_required(login_url='/log_in/', redirect_field_name='continue')
@csrf_protect
def question(request, question_id):
    popular_tags = Tag.objects.get_popular()
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question).order_by('created_at')
    page_obj = paginate(answers, request, per_page=9)

    # liked_questions = set()
    # if request.user.is_authenticated:
    #     if Question.objects.has_user_liked(question, request.user):
    #         liked_questions.add(question.id)

    liked_questions = QuestionLike.objects.filter(user=request.user).values_list('question_id', flat=True)
    liked_answers = AnswerLike.objects.filter(user=request.user).values_list('answer_id', flat=True)

    if request.method == 'GET':
        answer_form = AnswerForm()
    if request.method == 'POST':
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = answer_form.save(commit=False)
            answer.question = question
            answer.user = request.user
            answer.save()
            total_answers = answers.count() + 1  # include the new answer
            answers_per_page = 9
            page_number = (total_answers - 1) // answers_per_page + 1

            return redirect(f"{reverse('question', args=[question.id])}?page={page_number}#answer-{answer.id}")
    return render(request, 'question_detail.html',
                  {"question": question, "answers": page_obj, "form": answer_form, "username": request.user.username,
                   'popular_tags': popular_tags, 'liked_questions': liked_questions, 'liked_answers': liked_answers})


@login_required(login_url='/log_in/', redirect_field_name='continue')
@csrf_protect
def ask(request):
    popular_tags = Tag.objects.get_popular()
    if request.method == 'GET':
        ask_form = QuestionForm()
    if request.method == 'POST':
        ask_form = QuestionForm(request.POST)
        if ask_form.is_valid():
            question = ask_form.save(commit=False)
            question.user = request.user
            question.save()
            ask_form.save_tags(question)
            return redirect(reverse('question', kwargs={'question_id': question.id}))
    return render(request, 'ask.html',
                  {"form": ask_form, "username": request.user.username, "popular_tags": popular_tags})


@csrf_protect
def log_in(request):
    popular_tags = Tag.objects.get_popular()
    if request.method == "GET":
        login_form = LoginForm()
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = authenticate(request, **login_form.cleaned_data)
            if user is not None:
                login(request, user)
                return redirect(request.GET.get('continue', '/'))
            else:
                if not User.objects.filter(username=login_form.cleaned_data['username']).exists():
                    login_form.add_error('username', 'User does not exist')
                    login_form.add_error('password', 'User does not exist')
                else:
                    login_form.add_error('password', 'Wrong password')

    return render(request, 'login.html',
                  {'form': login_form, "username": request.user.username, 'popular_tags': popular_tags})


def log_out(request):
    auth.logout(request)
    return redirect(reverse('index'))


@csrf_protect
def signup(request):
    popular_tags = Tag.objects.get_popular()
    if request.method == "GET":
        user_form = RegisterForm()
    if request.method == "POST":
        user_form = RegisterForm(request.POST, request.FILES)
        if user_form.is_valid():
            user = user_form.save()
            if user is not None:
                return redirect(reverse('index'))
            else:
                user_form.add_error(None, 'User saving error!')
        else:
            user_form.add_error('password', "Passwords don't match")
            user_form.add_error('password_check', "Passwords don't match")
    return render(request, 'signup.html',
                  {'form': user_form, "username": request.user.username, 'popular_tags': popular_tags})


@login_required
@csrf_protect
def edit_profile(request):
    popular_tags = Tag.objects.get_popular()
    if request.method == "GET":
        edit_form = ProfileEditForm(instance=request.user)
    if request.method == "POST":
        edit_form = ProfileEditForm(request.POST, request.FILES, instance=request.user)
        if edit_form.is_valid():
            edit_form.save()
            return redirect(reverse('edit_profile'))

    return render(request, 'edit_profile.html', {"form": edit_form,
                                                 "username": request.user.username, 'popular_tags': popular_tags})


@login_required(login_url='/log_in/', redirect_field_name='continue')
def tag(request, tag_name):
    popular_tags = Tag.objects.get_popular()
    questions = Question.objects.by_tag(tag_name)
    page_obj = paginate(questions, request, per_page=5)
    return render(request, "tag.html", {"questions": page_obj, "tag_name": tag_name, "username": request.user.username,
                                        'popular_tags': popular_tags})


@require_http_methods(["POST"])
@login_required(login_url="/log_in/")
@csrf_protect
def like_question(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    question_like, question_like_created = QuestionLike.objects.get_or_create(question=question, user=request.user)
    if not question_like_created:
        question_like.delete()

    Question.objects.update_like_number(question)

    return JsonResponse({'likes_count': question.like_number})


@require_http_methods(["POST"])
@login_required(login_url="/log_in/")
@csrf_protect
def like_answer(request, answer_id):
    answer = get_object_or_404(Answer, pk=answer_id)
    answer_like, answer_like_created = AnswerLike.objects.get_or_create(answer=answer, user=request.user)

    if not answer_like_created:
        answer_like.delete()

    Answer.objects.update_like_number(answer)

    return JsonResponse({'likes_count': answer.like_number})


@require_http_methods(["POST"])
@login_required(login_url="/log_in/")
@csrf_protect
def mark_correct_answer(request, question_id, answer_id):
    is_correct = request.GET.get('is_correct') == 'true'

    question = get_object_or_404(Question, id=question_id)
    answer = get_object_or_404(Answer, id=answer_id, question=question)

    if request.user == question.user:
        answer.is_correct = is_correct
        answer.save()
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'You are not the author of this question'}, status=403)
