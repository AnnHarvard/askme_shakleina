from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from app.models import Question, Answer

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


def index(request):
    questions = Question.objects.new()
    page_obj = paginate(questions, request, per_page=5)
    return render(request, 'index.html', {"questions": page_obj})


def hot(request):
    questions = Question.objects.hot()
    page_obj = paginate(questions, request, per_page=5)
    return render(request, 'hot.html', {"questions": page_obj})


def question(request, question_id):
    question = get_object_or_404(Question, id=question_id)
    answers = Answer.objects.filter(question=question)
    page_obj = paginate(answers, request, per_page=5)
    return render(request, 'question_detail.html', {"question": question, "answers": page_obj})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def edit_profile(request):
    return render(request, 'edit_profile.html')


def tag(request, tag_name):
    questions = Question.objects.by_tag(tag_name)
    page_obj = paginate(questions, request, per_page=5)
    return render(request, "tag.html", {"questions": page_obj, "tag_name": tag_name})
