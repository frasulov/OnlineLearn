from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
import datetime
from django.core.exceptions import ObjectDoesNotExist
# Create your models here.




class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

GENDER_CHOICES = (
    ("male", "Male"),
    ("female", "Female"),
    ("other", "Other"),
)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('email address'), unique = True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    gender = models.CharField(max_length = 50, blank = True, choices = GENDER_CHOICES, default = 'male')
    profile_pic = models.ImageField(default = 'nouser.jpg', upload_to = 'user')
    biography = models.TextField(blank = True)
    birthday = models.DateField(null = True, blank = True)
    is_instructor = models.BooleanField(default = False)
    linkedn = models.CharField(max_length = 255, blank = True)
    facebook = models.CharField(max_length = 255, blank = True)
    header = models.CharField(max_length = 125, blank = True)
    taken_courses = models.ManyToManyField('Course', blank = True, related_name = 'users')
    last_search_query = models.CharField(max_length = 255, blank = True)
    objects = CustomUserManager()

    def getBirthdayHTML(self):
        if self.birthday:
            return self.birthday.strftime('%Y-%m-%d')
        else:
            return
            # return datetime.datetime.now().strptime('%d/%m/%Y')


    def __str__(self):
        return f"{self.email} {self.is_instructor}"

class Form_Answer(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='answers')
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return f"{self.body}"

    def serialize(self):
        return {
            "id":self.id,
            "body": self.body,
            "user":{
                "id": self.user.id,
                "email":self.user.email,
                "image": self.user.profile_pic.url,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            },
            "created": self.created.strftime("%m/%d/%Y, %H:%M:%S")
        }


class Form_Question(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='questions')
    title = models.CharField(max_length=255)
    body = models.TextField(blank=True)
    answers = models.ManyToManyField('Form_Answer',blank=True, related_name='questions')
    created = models.DateTimeField(auto_now_add=True, blank=True)

    def serialize(self):
        return {
            "id": self.id,
            "title": self.title,
            "body": self.body,
            "user": {
                "id": self.user.id,
                "email":self.user.email,
                "image": self.user.profile_pic.url,
                "first_name": self.user.first_name,
                "last_name": self.user.last_name,
            },
            "answers": [answer.serialize() for answer in self.answers.all()],
            "created": self.created.strftime("%m/%d/%Y, %H:%M:%S")
        }

    def __str__(self):
        return f"{self.title}"

class Course(models.Model):
    title = models.CharField(max_length = 255)
    sub_title = models.CharField(max_length = 255, default='My Subtitle')
    description = models.TextField(blank = True)
    price = models.PositiveIntegerField(default = 0)
    image = models.ImageField(default = 'no_image.png', upload_to = 'course')
    category = models.ForeignKey('Category', on_delete = models.CASCADE, related_name = 'courses')
    sub_category = models.ForeignKey('SubCategory', on_delete = models.CASCADE, related_name = 'courses')
    language = models.ForeignKey('Language', on_delete = models.CASCADE, related_name = 'courses')
    instructor = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'courses')
    pubhlised = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add = True)
    updated = models.DateTimeField(auto_now = True)
    content = models.ManyToManyField('Section', blank = True, related_name = 'courses')
    aq_form = models.ManyToManyField('Form_Question', blank=True, related_name='courses')

    def __str__(self):
        return f"{self.title}"

    def titleLength(self):
        return len(self.title)

LECTURE_TYPE = (
    ("0", "video"),
    ("1", "quiz"),
    ("2", "information"),
)

class Lecture(models.Model):
    text = models.CharField(max_length = 125)
    type = models.CharField(max_length = 50, blank = True, choices = LECTURE_TYPE, default = '0')
    video_link = models.CharField(max_length = 255, blank = True)
    information = models.TextField(blank = True)
    quiz = models.ManyToManyField('Quiz', blank = True, related_name = 'lecture')

    def __str__(self):
        return f"{self.text}"


class Section(models.Model):
    text = models.CharField(max_length = 125)
    lecture = models.ManyToManyField('Lecture', blank = True, related_name = 'sections')

    def __str__(self):
        return f"{self.text}"


class Language(models.Model):
    text = models.CharField(max_length = 125)

    def __str__(self):
        return f"{self.text}"

class Category(models.Model):
    text = models.CharField(max_length = 125)
    image = models.ImageField(default = 'nouser.jpg', upload_to = 'category')
    sub_category = models.ManyToManyField('SubCategory', blank = True, related_name = 'category')

    def __str__(self):
        return f"{self.text}"

class SubCategory(models.Model):
    text = models.CharField(max_length = 125)

    def __str__(self):
        return f"{self.text}"

    def serialize(self):
        return {
            'text':self.text,
            "id": self.id,
        }


class QA(models.Model):
    q = models.ForeignKey('Question', on_delete = models.CASCADE, related_name = 'qa')
    a = models.ForeignKey('Answer', on_delete = models.CASCADE, related_name = 'qa')

class Exam(models.Model):
    quiz = models.ForeignKey('Quiz', on_delete = models.CASCADE, related_name = 'exams')
    student = models.ForeignKey('User', on_delete = models.CASCADE, related_name = 'exams')
    started = models.DateTimeField(auto_now_add = True)
    choices = models.ManyToManyField('QA', blank = True, related_name = 'exams')
    submitted = models.BooleanField(default = False)

    def __str__(self):
        return f"{Quiz}"

    def getResult(self):
        question_answer = []
        for question in self.quiz.questions.all():
            try:
                user_choice = self.choices.get(q = question)
                user_answer = user_choice.a
            except ObjectDoesNotExist:
                user_answer = False
            question_answer.append( {
                "question":question,
                "correct_answer":question.getCorrectAnswer(),
                "user_answer": user_answer
            })
        return question_answer


    def getNumberOfTightAnswers(self):
        score = 0
        right_answer_count = 0
        for question in self.quiz.questions.all():
            count = 0
            try:
                is_correct = self.choices.get(q = question, a = question.getCorrectAnswer())
                count += 1
            except ObjectDoesNotExist:
                pass
            if count:
                right_answer_count +=1
                score += question.score
        return [score,right_answer_count]


    def getTotalScore(self):
        score = 0
        for question in self.quiz.questions.all():
            score += question.score

        return score


    def getFinishedTime(self):
        quiz_time = self.quiz.time_in_minute
        finished = self.started + datetime.timedelta(hours = 4, minutes = quiz_time)
        return finished.strftime("%m/%d/%Y, %H:%M:%S")

class Quiz(models.Model):
    title = models.CharField(max_length = 255, blank = True)
    time_in_minute = models.PositiveIntegerField(default = 1)
    description = models.TextField(blank = True)
    questions = models.ManyToManyField('Question', blank = True, related_name = 'quiz')

    def __str__(self):
        return f"{self.title}"

class Question(models.Model):
    text = models.TextField(blank = False)
    answers = models.ManyToManyField('Answer', blank = True, related_name = 'question')
    score = models.PositiveIntegerField(default = 0)

    def __str__(self):
        return f"{self.text}"

    def getCorrectAnswer(self):
        for answer in self.answers.all():
            if answer.is_true:
                return answer

class Answer(models.Model):
    text = models.TextField(blank = False)
    is_true = models.BooleanField(default = False)

    def __str__(self):
        return f"{self.text} -> {self.is_true}"
