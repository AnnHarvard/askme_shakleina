import random
from faker import Faker
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.db import connection

from app.models import Question, Answer, Tag, QuestionLike, AnswerLike, Profile

fake = Faker()


class Command(BaseCommand):
    help = 'Fill db with fake data'

    def add_arguments(self, parser):
        parser.add_argument('ratio', type=int, help='Defines the ratio of fake data to create')

    def handle(self, *args, **options):

        ratio = options['ratio']
        self.create_users_and_profiles(ratio)
        self.create_tags(ratio)
        self.create_questions(ratio * 10)
        self.create_answers(ratio * 100)
        self.create_question_likes(ratio * 100)
        self.create_answer_likes(ratio * 100)

    def create_users_and_profiles(self, ratio):
        users = [
            User(
                username=fake.user_name() + '-' + fake.name(),
                email=fake.email(),
                password=fake.password(),
            )
            for _ in range(ratio)
        ]
        User.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS(f'{ratio} users created.'))
        profiles = [
            Profile(
                user=user,
            )
            for user in users
        ]
        Profile.objects.bulk_create(profiles)
        self.stdout.write(self.style.SUCCESS(f'{ratio} profiles created.'))

    def create_tags(self, ratio):
        tags = [
            Tag(
                name=fake.word(),
            )
            for _ in range(ratio)
        ]
        Tag.objects.bulk_create(tags)
        self.stdout.write(self.style.SUCCESS(f'{ratio} tags created.'))

    def create_questions(self, ratio):
        users = User.objects.all()
        tags = list(Tag.objects.all())
        questions = [
            Question(
                title=fake.sentence(),
                text=fake.paragraph(),
                user=random.choice(users),
                created_at=fake.date_time(),
            )
            for _ in range(ratio)
        ]
        Question.objects.bulk_create(questions)
        for question in questions:
            question.tags.add(*random.sample(tags, k=random.randint(1, 5)))
            question.save()
        self.stdout.write(self.style.SUCCESS(f'{ratio} questions created.'))

    def create_answers(self, ratio):
        users = User.objects.all()
        questions = Question.objects.all()
        answers = []
        for _ in range(ratio):
            question = random.choice(questions)
            answer = Answer(
                question=question,
                text=fake.paragraph(),
                user=random.choice(users),
                created_at=fake.date_time_between_dates(datetime_start=question.created_at, datetime_end='now'),
            )
            answers.append(answer)
        Answer.objects.bulk_create(answers)
        self.stdout.write(self.style.SUCCESS(f'{ratio} answers created.'))

    def create_question_likes(self, ratio):
        self.stdout.write(self.style.SUCCESS('question likes started.'))

        users = list(User.objects.values_list('id', flat=True))
        questions = list(Question.objects.all())
        question_likes = []
        existing_likes = set()
        question_likes_count = {question.id: 0 for question in questions}
        for i in range(ratio):
            question = random.choice(questions)
            user_id = random.choice(users)
            like_tuple = (question.id, user_id)
            if (like_tuple not in existing_likes
                    and not QuestionLike.objects.filter(question_id=question.id, user_id=user_id).exists()):
                existing_likes.add(like_tuple)
                question_like = QuestionLike(
                    question_id=question.id,
                    user_id=user_id,
                )
                question_likes.append(question_like)
                question_likes_count[question.id] += 1
                if i % 10000 == 0:
                    self.stdout.write(self.style.SUCCESS(f'{i} passed'))

        self.stdout.write(self.style.SUCCESS('started bulk_create\n'))
        QuestionLike.objects.bulk_create(question_likes)
        self.stdout.write(self.style.SUCCESS('started like_number update'))
        for i, question in enumerate(questions):
            if question_likes_count[question.id] > 0:
                question.like_number += question_likes_count[question.id]
                question.save()
            if i % 1000 == 0:
                self.stdout.write(self.style.SUCCESS(f'{i} passed'))
        self.stdout.write(self.style.SUCCESS(f'{len(question_likes)} question likes created.'))

    def create_answer_likes(self, ratio):
        self.stdout.write(self.style.SUCCESS('answer likes started.'))

        users = list(User.objects.values_list('id', flat=True))
        answers = list(Answer.objects.all())
        answer_likes = []
        existing_likes = set()
        answer_likes_count = {answer.id: 0 for answer in answers}
        for i in range(ratio):
            answer = random.choice(answers)
            user_id = random.choice(users)
            like_tuple = (answer.id, user_id)
            if (like_tuple not in existing_likes
                    and not AnswerLike.objects.filter(answer_id=answer.id, user_id=user_id).exists()):
                existing_likes.add(like_tuple)
                answer_like = AnswerLike(
                    answer_id=answer.id,
                    user_id=user_id,
                )
                answer_likes.append(answer_like)
                answer_likes_count[answer.id] += 1
                if i % 10000 == 0:
                    self.stdout.write(self.style.SUCCESS(f'{i} passed'))

        self.stdout.write(self.style.SUCCESS('started bulk_create\n'))
        AnswerLike.objects.bulk_create(answer_likes)
        self.stdout.write(self.style.SUCCESS('started like_number update'))
        for i, answer in enumerate(answers):
            if answer_likes_count[answer.id] > 0:
                answer.like_number += answer_likes_count[answer.id]
                answer.save()
            if i % 1000 == 0:
                self.stdout.write(self.style.SUCCESS(f'{i} passed'))
        self.stdout.write(self.style.SUCCESS(f'{len(answer_likes)} answer likes created.'))
