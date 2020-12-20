from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from .models import *
from django.contrib.auth import get_user_model
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.db.models import Count
import json
User = get_user_model()
# Create your views here.


def enroll(request, course_id):
    try:
        course = Course.objects.get(pk = int(course_id))
        user = request.user
        user.taken_courses.add(course)
        user.save()
        return HttpResponseRedirect(reverse('course', args=(course_id,)))
    except ObjectDoesNotExist:
        return notfound(request, 'No such course')

def searchAPI(request, query):
    queries = set()
    if not query:
        return JsonResponse({"error":"Not query"}, status = 404)

    for category in Category.objects.all():
        if query.upper() in category.text.upper():
            queries.add(category.text)
    for category in SubCategory.objects.all():
        if query.upper() in category.text.upper():
            queries.add(category.text)
    for language in Language.objects.all():
        if query.upper() in language.text.upper():
            queries.add(language.text)
    for course in Course.objects.all():
        if query.upper() in course.title.upper():
            for word in course.title.split(' '):
                if query.upper() in word.upper():
                    queries.add(word)
        if query.upper() in course.sub_title.upper():
            for word in course.sub_title.split(' '):
                if query.upper() in word.upper():
                    queries.add(word)

    return JsonResponse({"queries": list(queries)}, status = 201)


def search(request):
    try:
        c = Course.objects.all().annotate(num_users=Count('users')).order_by('num_users')
        if len(c) > 6:
            c = c[:6]
    except ObjectDoesNotExist:
        c = None
    query = request.GET.get('q')
    if query == '':
        return notfound(request, 'You cannot search empty string')
    for category in Category.objects.all():
        if query.upper() == category.text.upper():
            query = category.text
            break
    if request.user.is_authenticated:
        user = request.user
        user.last_search_query =  query
        user.save()
    result_courses = []
    if query:
        all_course = Course.objects.all()
        for course in all_course:
            if query.upper() in course.description.upper() or query.upper() in course.title.upper() or query.upper() == course.category.text.upper() or query.upper() == course.sub_category.text.upper() or query.upper() == course.language.text.upper():
                result_courses.append(course)
    paginator = Paginator(result_courses, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "OnlineLearn/search.html", {
        'search': query,
        'languages': Language.objects.all(),
        'categories': Category.objects.all(),
        "result_len": len(result_courses),
        'page_obj': page_obj,
        "popular_courses":c,
    })


def course(request, course_id):
    try:
        course = Course.objects.get(pk = int(course_id))
        return render(request, 'OnlineLearn/description.html',{
            "course":course,
            "categories":Category.objects.all().order_by('text'),
            "languages":Language.objects.all(),
        })
    except:
        return notfound(request, 'No such course')

def getSubCategory(request, category_id):
    try:
        category = Category.objects.get(pk = int(category_id))
        print(category)
        return JsonResponse({"category":category.text,"subcategories":[subcategory.serialize() for subcategory in category.sub_category.all()]}, status = 201)
    except ObjectDoesNotExist:
        return JsonResponse({"error": "No such category"}, status = 404)

def getCourseQAForm(request, course_id):
    try:
        course = Course.objects.get(pk = int(course_id))
        return JsonResponse({"qa": [question.serialize() for question in course.aq_form.all().order_by('-id')]}, status = 201)
    except ObjectDoesNotExist:
        return JsonResponse({"error":"No such course"}, status= 404)

def addAnswerToForm(request, question_id):
    if request.method == "POST":
        data = json.loads(request.body)
        body = data.get("body", "")
        try:
            question = Form_Question.objects.get(pk = int(question_id))
            new_answer = Form_Answer()
            new_answer.body = body
            new_answer.user = request.user
            new_answer.save()
            question.answers.add(new_answer)
            question.save()
            return JsonResponse({"message":"completed", "answer": new_answer.serialize()}, status=201)
        except ObjectDoesNotExist:
            return JsonResponse({"error":"No such question"}, status= 404)
    else:
        return JsonResponse({"error": "not completed"}, status=201)

def addQuestionToForm(request, course_id):
    if request.method == "POST":
        data = json.loads(request.body)
        title = data.get("title", "")
        body = data.get("body", "")
        try:
            course = Course.objects.get(pk = int(course_id))
            new_question = Form_Question()
            new_question.title = title
            new_question.body = body
            new_question.user = request.user
            new_question.save()
            course.aq_form.add(new_question)
            course.save()
            return JsonResponse({"message":"completed"}, status=201)
        except:
            return JsonResponse({"error":"No such course"}, status= 404)
    else:
        return JsonResponse({"error": "not completed"}, status=201)

def submitExam(request, course_id, exam_id, lecture_id):
    try:
        exam = Exam.objects.get(pk = int(exam_id))
        exam.submitted = True
        exam.save()
        return HttpResponseRedirect(reverse('coursecontent', args=(course_id, lecture_id,)))
    except ObjectDoesNotExist:
        return notfound(request, 'no such exam or course')

def reviewExam(request, exam_id):
    try:
        exam = Exam.objects.get(pk = int(exam_id))
        return render(request, "OnlineLearn/reviewExam.html",{
            "exam":exam
        })
    except ObjectDoesNotExist:
        return notfound(request, "No such exam")

def checkAnswer(request, exam_id,question_id):
    try:
        exam = Exam.objects.get(pk = int(exam_id))
        question = Question.objects.get(pk = int(question_id))
        try:
            qa = exam.choices.get(q = question)
            answer = qa.a
            return JsonResponse({"saved":True, "saved_answer":answer.id}, status = 201)
        except ObjectDoesNotExist:
            return JsonResponse({"saved":False}, status=201)
    except ObjectDoesNotExist:
        return JsonResponse({"error":"Something went wrong!"}, status=201)

def saveAnswer(request, exam_id,question_id, answer_id):
    try:
        exam = Exam.objects.get(pk = int(exam_id))
        question = Question.objects.get(pk = int(question_id))
        answer = Answer.objects.get(pk = int(answer_id))
        try:
            qa = QA.objects.get(q = question)
        except ObjectDoesNotExist:
            qa = QA(q = question, a = answer)
            qa.save()
        qa.a = answer
        qa.save()
        exam.choices.add(qa)
        exam.save()
        return JsonResponse({"result":"Answer is saved"}, status=201)
    except ObjectDoesNotExist:
        return JsonResponse({"error":"Something went wrong!"}, status=201)

def index(request, message = None):
    result_courses = []
    if request.user.is_authenticated:
        query = request.user.last_search_query
        if query:
            all_course = Course.objects.all()
            for course in all_course:
                if query.upper() in course.description.upper() or query.upper() in course.title.upper() or query.upper() == course.category.text.upper() or query.upper() == course.sub_category.text.upper() or query.upper() == course.language.text.upper():
                    result_courses.append(course)
    return render(request, 'OnlineLearn/home.html',{
        "categories": Category.objects.all().order_by('text'),
        "courses":Course.objects.all(),
        "result_courses": result_courses,
        "result_courses_len": len(result_courses),
    })

def notfound(request, message = None):
    return render(request, 'OnlineLearn/notfound.html',{
        "message":message,
        "categories":Category.objects.all().order_by('text'),
    })

def courseContentStartQuiz(request, course_id, lecture_id):
    try:
        course = Course.objects.get(pk = int(course_id))
        if int(lecture_id) == 0:
            lecture_id = course.content.all().first().lecture.all().first().id
        try:
            lecture = Lecture.objects.get(pk = int(lecture_id))
            quiz = lecture.quiz.all().first()
            try:
                exam = Exam.objects.get(student = request.user, quiz = quiz)
                finished = exam.started + datetime.timedelta(hours = 4, minutes = exam.quiz.time_in_minute)
                if datetime.datetime.now().time() >= finished.time():
                    exam.submitted = True
                    exam.save()
            except ObjectDoesNotExist:
                exam = Exam()
                exam.student = request.user
                exam.quiz = quiz
                exam.save()
            questions = exam.quiz.questions.all()
            paginator = Paginator(questions, 1)
            page_number = request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            return render(request, 'OnlineLearn/courseContentQuiz.html',{
                "course":course,
                'exam': exam,
                'lecture_id':lecture.id,
                "start": False,
                "page_obj":page_obj,
                "categories":Category.objects.all().order_by('text'),
            })
        except ObjectDoesNotExist:
            return notfound(request, 'No such lecture')
    except ObjectDoesNotExist:
        return notfound(request, 'No such course')

def courseContent(request, course_id, lecture_id):
    try:
        course = Course.objects.get(pk = int(course_id))
        if (not course in request.user.taken_courses.all()) and (course.instructor != request.user):
            return notfound(request, 'You do not have access to this course')
        if int(lecture_id) == 0:
            lecture_id = course.content.all().first().lecture.all().first().id
        try:
            lecture = Lecture.objects.get(pk = int(lecture_id))
            if lecture.type == "0":
                return render(request, 'OnlineLearn/courseContentVideo.html',{
                    "course":course,
                    "video":True,
                    "lecture": lecture,
                    "categories":Category.objects.all().order_by('text')
                })
            elif lecture.type == '1':
                try:
                    exam = Exam.objects.get(student = request.user, quiz = lecture.quiz.all().first())
                    print(exam)
                    return render(request, 'OnlineLearn/courseContentQuiz.html',{
                        "course":course,
                        'quiz': lecture.quiz.all().first(),
                        'lecture_id':lecture.id,
                        "start": True,
                        "exam": exam,
                        "categories":Category.objects.all().order_by('text')
                    })
                except:
                    return render(request, 'OnlineLearn/courseContentQuiz.html',{
                        "course":course,
                        'quiz': lecture.quiz.all().first(),
                        'lecture_id':lecture.id,
                        "start": True,
                        "categories":Category.objects.all().order_by('text')
                    })
            else:
                return render(request, 'OnlineLearn/courseContentVideo.html',{
                    "course":course,
                    "lecture": lecture,
                    "video":False,
                    "categories":Category.objects.all().order_by('text')
                })

        except ObjectDoesNotExist:
            return notfound(request, 'No such lecture')
    except ObjectDoesNotExist:
        return notfound(request, 'No such course')
    return render(request, 'OnlineLearn/courseContentQuiz.html')




def viewProfile(request, profile_email):
    try:
        user = User.objects.get(email = profile_email)
        return render(request, "OnlineLearn/viewProfile.html",{
            "profile_user": user,
            "categories":Category.objects.all().order_by('text'),
        })
    except ObjectDoesNotExist:
        return notfound(request, 'There is no such profile!')

def addQuestion(request, course_id, quiz_id):
    if request.method == "POST":
        try:
            course = Course.objects.get(pk = int(course_id))
            quiz = Quiz.objects.get(pk = int(quiz_id))
            text = request.POST['text']
            score = request.POST['score']
            correct_answer = request.POST['correct-answer']
            answer1 = 'answer-1' in request.POST and request.POST['answer-1']
            answer2 = 'answer-2' in request.POST and request.POST['answer-2']
            answer3 = 'answer-3' in request.POST and request.POST['answer-3']
            answer4 = 'answer-4' in request.POST and request.POST['answer-4']
            new_question = Question()
            new_question.text = text
            new_question.score = int(score)
            new_question.save()
            if answer1:
                new_answer_1 = Answer()
                new_answer_1.text = answer1
                if int(correct_answer) == 1:
                    new_answer_1.is_true = True
                new_answer_1.save()
                new_question.answers.add(new_answer_1)
            if answer2:
                new_answer_2 = Answer()
                new_answer_2.text = answer2
                if int(correct_answer) == 2:
                    new_answer_2.is_true = True
                new_answer_2.save()
                new_question.answers.add(new_answer_2)
            if answer3:
                new_answer_3 = Answer()
                new_answer_3.text = answer3
                if int(correct_answer) == 3:
                    new_answer_3.is_true = True
                new_answer_3.save()
                new_question.answers.add(new_answer_3)
            if answer4:
                new_answer_4 = Answer()
                new_answer_4.text = answer4
                if int(correct_answer) == 4:
                    new_answer_4.is_true = True
                new_answer_4.save()
                new_question.answers.add(new_answer_4)
            new_question.save()
            quiz.questions.add(new_question)
            quiz.save()
            return HttpResponseRedirect(reverse('addcontent', args=(course_id,)))

        except ObjectDoesNotExist:
            return notfound(request, 'No such course or quiz')
    else:
        return notfound(request, 'No such course or quiz')

def deleteLecture(request, course_id, lecture_id):
    try:
        course = Course.objects.get(pk = int(course_id))
        Lecture.objects.get(pk = int(lecture_id)).delete()
        return HttpResponseRedirect(reverse('addcontent', args=(course_id,)))
    except ObjectDoesNotExist:
        return notfound(request, 'No such course or lecture')

def deleteSection(request, course_id, section_id):
    try:
        course = Course.objects.get(pk = int(course_id))
        Section.objects.get(pk = int(section_id)).delete()
        return HttpResponseRedirect(reverse('addcontent', args=(course_id,)))
    except ObjectDoesNotExist:
        return notfound(request, 'No such course or section')

def deleteCourse(request, course_id):
    try:
        Course.objects.get(pk = int(course_id)).delete()
        return HttpResponseRedirect(reverse('instructorDashboard'))
    except ObjectDoesNotExist:
        return notfound(request, 'No such course')



def editLecture(request, course_id, lecture_id):
    if request.method == "POST":
        try:
            course = Course.objects.get(pk = int(course_id))
            lecture = Lecture.objects.get(pk = int(lecture_id))
            if lecture.type == '0':
                name = request.POST['name']
                videoid = request.POST['videoid']
                if lecture.text != name:
                    lecture.text = name
                if lecture.video_link != videoid:
                    lecture.video_link = videoid
            elif lecture.type == '2':
                name = request.POST['name']
                information = request.POST['information']
                if lecture.text != name:
                    lecture.text = name
                if lecture.information != information:
                    lecture.information = information
            elif lecture.type == '1':
                name = request.POST['name']
                time = request.POST['time']
                description = request.POST['description']
                title = request.POST['title']
                if lecture.text != name:
                    lecture.text = name
                quiz = lecture.quiz.all().first()
                if quiz.title != title:
                    quiz.title = title
                if quiz.time_in_minute != int(time):
                    quiz.time_in_minute = int(time)
                if quiz.description != description:
                    quiz.description = description
                quiz.save()
            lecture.save()
            return HttpResponseRedirect(reverse('addcontent', args=(course_id,)))
        except ObjectDoesNotExist:
            return notfound(request, 'No such course or lecture')
    else:
        return notfound(request, 'Request must be POST')

def addLecture(request, course_id, section_id):
    if request.method == "POST":
        try:
            course = Course.objects.get(pk = int(course_id))
            section = Section.objects.get(pk = int(section_id))
            name = request.POST['name']
            type = request.POST['type']
            lecture = Lecture(text = name, type = type)
            lecture.save()
            if type == "1":
                new_quiz = Quiz()
                new_quiz.save()
                lecture.quiz.add(new_quiz)
                lecture.save()
            section.lecture.add(lecture)
            return HttpResponseRedirect(reverse('addcontent', args=(course_id, )))
        except ObjectDoesNotExist:
            return notfound(request, 'No such course or section')
    else:
        return notfound(request, "It should be post request")


def editSection(request, course_id, section_id):
    if request.method == "POST":
        try:
            course = Course.objects.get(pk = int(course_id))
            section = Section.objects.get(pk = int(section_id))
            name = request.POST['name']
            section.text = name
            section.save()
            return HttpResponseRedirect(reverse('addcontent', args=(course_id, )))
        except ObjectDoesNotExist:
            return notfound(request, "No such course or section")
    else:
        return notfound(request, "It should be post request")

def addContent(request, course_id):
    try:
        course = Course.objects.get(pk = int(course_id))
        if request.method == "POST":
            name = request.POST['name']
            section = Section(text = name)
            section.save()
            course.content.add(section)
            course.save()
        return render(request, "OnlineLearn/addcontent.html", {
            "course":course,
            "categories": Category.objects.all().order_by('text'),
        })
    except ObjectDoesNotExist:
        return notfound(request, 'Not such course')

def instructorDashboard(request):
    if request.method == "POST":
        title = request.POST['title']
        price = request.POST['price']
        category_id = request.POST['category']
        sub_category_id = request.POST['subcategory']
        language_id = request.POST['language']
        descripiton = request.POST['descripiton']
        subtitle = request.POST['subtitle']
        course_image = 'course_image' in request.FILES and request.FILES['course_image']
        try:
            category = Category.objects.get(pk = int(category_id))
            sub_category = SubCategory.objects.get(pk = int(sub_category_id))
            language = Language.objects.get(pk = int(language_id))
        except ObjectDoesNotExist:
            return notfound(request, 'No such language || category || sub category!')
        course = Course()
        course.title = title
        course.sub_title = subtitle
        course.price = int(price)
        course.category = category
        course.sub_category = sub_category
        course.language = language
        course.instructor = request.user
        course.description = descripiton

        if course_image:
            course.image = course_image
        course.save()
        return HttpResponseRedirect(reverse('addcontent', args=(course.id,)))

    return render(request, "OnlineLearn/instructorDashboard.html",{
        "courses": Course.objects.filter(instructor = request.user),
        "categories": Category.objects.all(),
        "languages": Language.objects.all(),

    })



def editProfile(request, profile_email):
    if request.method == 'POST':
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        gender = request.POST['gender']
        birthday = request.POST['birthday']
        bio = request.POST['bio']
        linkedn = 'linkedn' in request.POST and request.POST['linkedn']
        facebook = 'facebook' in request.POST and request.POST['facebook']
        header = 'header' in request.POST and request.POST['header']
        profile_image = 'profile_image' in request.FILES and request.FILES['profile_image']
        print(birthday, 'your birth')
        try:
            user = request.user
            if profile_image:
                user.profile_pic = profile_image
            user.first_name = firstname
            user.last_name = lastname
            user.gender = gender
            user.birthday = datetime.datetime.strptime(birthday,'%Y-%m-%d')
            if bio:
                user.biography = bio
            if header:
                user.header = header
            if facebook:
                user.facebook = facebook
            if linkedn:
                user.linkedn = linkedn
            user.save()
            return HttpResponseRedirect(reverse('index'))
        except ObjectDoesNotExist:
            return notfound(request, "Error while editing profile")
    try:
        user = User.objects.get(email = profile_email)
        if request.user == user:
            return render(request, "OnlineLearn/editProfile.html",{
                "languages":Language.objects.all(),
                "categories":Category.objects.all().order_by('text')
            })
        else:
            return notfound(request, "You can't edit others profile!")
    except ObjectDoesNotExist:
        return notfound(request, "The user with that email does not exist!")

def login_view(request):
    if request.method == "POST":

        email = request.POST["email"]
        password = request.POST["password"]
        user = authenticate(request, email=email, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "OnlineLearn/login.html", {
                "message": "Invalid username and/or password.",
                "categories":Category.objects.all().order_by('text')
            })
    else:
        return render(request, "OnlineLearn/login.html",{
            "categories":Category.objects.all().order_by('text')
        })


def register_view(request):
    if request.method == "POST":
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        gender = request.POST["gender"]
        type = request.POST["type"]
        birthday = request.POST['birthday']
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "OnlineLearn/register.html", {
                "message": "Passwords must match.",
                "categories":Category.objects.all().order_by('text')
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(email = email, password = password, first_name = firstname, last_name = lastname, gender = gender, birthday = datetime.datetime.strptime(birthday,'%Y-%m-%d'))
            if type == '1':
                user.is_instructor = True
            user.save()
        except IntegrityError:
            return render(request, "OnlineLearn/register.html", {
                "message": "The mail already registered.",
                "categories":Category.objects.all().order_by('text'),
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "OnlineLearn/register.html",{
            "categories":Category.objects.all().order_by('text'),
        })

def logout_view(request):
    logout(request)
    return index(request, "Logged out Succesfully!")
