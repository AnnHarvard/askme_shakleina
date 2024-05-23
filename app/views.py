from django.shortcuts import render
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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
    page_obj = paginate(QUESTIONS, request, per_page=5)
    return render(request, 'index.html', {"questions": page_obj})


def hot(request):
    page_obj = paginate(QUESTIONS[5:], request, per_page=5)
    return render(request, 'hot.html', {"questions": page_obj})


def question(request, question_id):
    item = QUESTIONS[question_id]
    page_obj = paginate(ANSWERS, request, per_page=5)
    return render(request, 'question_detail.html', {"question": item, "answers": page_obj})


def ask(request):
    return render(request, 'ask.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def edit_profile(request):
    return render(request, 'edit_profile.html')


def tag(request, tag_name):
    page_obj = paginate(QUESTIONS, request, per_page=5)
    return render(request, "tag.html", {"questions": page_obj, "tag_name": tag_name})
