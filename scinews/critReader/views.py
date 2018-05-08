from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.shortcuts import render
from django.http import Http404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader, RequestContext
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from .forms import UserForm, LoginForm
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import operator
# Create your views here.

def index(request):
    article_list=Article.objects.all()
    context={
        'article_list': article_list
        }
    return render(request, 'critreader/index.html', context)

def article(request,article_no):
    try:
        article=Article.objects.get(article_no=article_no)
    except Article.DoesNotExist:
        raise Http404("Research does not exist")
    thisArticle=Article.objects.get(article_no=article_no)
    thisResearch=thisArticle.article_research
    allqs=Question.objects.filter(question_research=thisResearch)
    titleqs=Question.objects.filter(question_research=thisResearch, question_abstract=1)
#    orderedq=reversed(sorted(allqs, key=operator.attrgetter('question_popularity')))
#    orderedlist=list(orderedq)
    questionlinkhere=Questionlink.objects.filter(link_article=thisArticle)
    quizlinkhere=Quizlink.objects.filter(link_article=thisArticle)
    quizlinkthere=Quizlink.objects.filter(link_article!=thisArticle, link_research=thisResearch)
    context={
    'article':thisArticle,
    'allqs':allqs,
    'titleqs':titleqs,
    'questionhere':questionlinkhere,
    'quizlinkhere':quizlinkhere,
    'quizlinkthere':quizlinkthere,
    } 
    return render(request, 'critreader/article.html', context)

def col_question_collector(request,article_no):
    try:
        article=Article.objects.get(article_no=article_no)
    except Article.DoesNotExist:
        raise Http404("Research does not exist")
    thisArticle=Article.objects.get(article_no=article_no)
    questions=Question.objects.filter(question_article=thisArticle)
    context={
    'article':thisArticle,
    'questions':questions,
    } 
    return render(request, 'critreader/colqcol.html', context)


def question_collector(request,article_no):
    try:
        article=Article.objects.get(article_no=article_no)
    except Article.DoesNotExist:
        raise Http404("Research does not exist")
    thisArticle=Article.objects.get(article_no=article_no)
    context={
    'article':thisArticle,
    } 
    return render(request, 'critreader/qcol.html', context)

def quiz_collector(request,article_no):
    try:
        article=Article.objects.get(article_no=article_no)
    except Article.DoesNotExist:
        raise Http404("Research does not exist")
    thisArticle=Article.objects.get(article_no=article_no)
    context={
    'article':thisArticle,
    } 
    return render(request, 'critreader/quizcol.html', context)

def survey(request, survey_no):
    try:
        survey=SurveyEmbed.objects.get(survey_no=survey_no)
    except SurveyEmbed.DoesNotExist:
        raise Http404("Survey does not exist")
    thissurvey=SurveyEmbed.objects.get(survey_no=survey_no)
    context={
    'survey':thissurvey,
    } 
    return render(request, 'critreader/surveyembed.html', context)

def viewquiz(request, article_no):
    try:
        article=Article.objects.get(article_no=article_no)
    except Article.DoesNotExist:
        raise Http404("Research does not exist")
    thisArticle=Article.objects.get(article_no=article_no)
    quizs=Question.objects.filter(question_article=thisArticle,question_madeat="quizcol")
    reftexts=[RefText.objects.filter(reftext_question=aquiz) for aquiz in quizs]
    context={
    'article':thisArticle,
    'quizs':quizs,
    'reftexts':reftexts,
    } 
    return render(request, 'critreader/viewquiz.html', context)

def viewquestion(request, article_no):
    try:
        article=Article.objects.get(article_no=article_no)
    except Article.DoesNotExist:
        raise Http404("Research does not exist")
    thisArticle=Article.objects.get(article_no=article_no)
    questions=Question.objects.filter(question_article=thisArticle,question_madeat="qcol")
    context={
    'article':thisArticle,
    'questions':questions,
    } 
    return render(request, 'critreader/viewquestion.html', context)

@csrf_exempt
def addquestionwithref(request, article_no):
    articleno=request.POST.get('articleno',None)
    text=request.POST.get('text', None)
    madeby=request.POST.get('madeby',None)
    madeat=request.POST.get('madeat',None)
    refsentids=request.POST.get('refsentids',None)
    pubdate=timezone.now()
    thisArticle=Article.objects.get(article_no=articleno)
    username=User.objects.get(username=madeby)
    newQuestion=Question(question_article=thisArticle, question_text=text, question_madeby=username, question_madeat=madeat, question_popularity=1, question_pubdate=pubdate)
    newQuestion.save()
    newRefText=RefText(reftext_question=newQuestion, reftext_text=refsentids, reftext_pubdate=pubdate, reftext_madeby=username)
    newRefText.save()
    return HttpResponseRedirect('')

@csrf_exempt
def addquestion(request, article_no):
    articleno=request.POST.get('articleno',None)
    text=request.POST.get('text', None)
    madeby=request.POST.get('madeby',None)
    madeat=request.POST.get('madeat',None)
    pubdate=timezone.now()
    thisArticle=Article.objects.get(article_no=articleno)
    username=User.objects.get(username=madeby)
    newQuestion=Question(question_article=thisArticle, question_text=text, question_madeby=username, question_madeat=madeat, question_popularity=1, question_pubdate=pubdate)
    newQuestion.save()
    return HttpResponseRedirect('')

@csrf_exempt    
def addcount(request, article_no):
    pk=request.POST.get('qpk', None)
    thisQuestion=Question.objects.get(pk=pk)
    curcount=request.POST.get('curcount',None)
    thisQuestion.question_popularity=int(curcount)+1
    thisQuestion.save()
    return HttpResponseRedirect('')
    

    

def signup(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            new_user = User.objects.create_user(**form.cleaned_data)
            login(request, new_user)
            return redirect('tutorial')
    else:
        form = UserForm()
        return render(request, 'critreader/signup.html', {'form': form})

def signin(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username = username, password = password)
        if user is not None:
            login(request, user)
            return redirect('tutorial')
        else:
            return HttpResponse('로그인 실패. 다시 시도 해보세요.')
    else:
        form = LoginForm()
        return render(request, 'critreader/login.html', {'form': form})

@csrf_exempt    
def tutorial(request):
    return render(request, 'critreader/tutorial.html')

