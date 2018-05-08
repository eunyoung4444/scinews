from django.db import models
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

# Create your models here.
class Research(models.Model):
    research_no=models.PositiveIntegerField(default=1)
    research_keyword=models.CharField(max_length=50)
    research_link=models.CharField(max_length=200)
    def __str__(self):
        return self.research_keyword

class Article(models.Model):
    article_research=models.ForeignKey(Research, on_delete=models.CASCADE)
    article_no=models.IntegerField(default=99)
    article_title=models.CharField(max_length=250)
    article_body=models.CharField(max_length=100000)
    article_date=models.CharField(max_length=100,default="December 2017")
    article_link=models.CharField(max_length=100,default="#")
    article_publisher=models.CharField(max_length=100, default="publisher")
    def __str__(self):
        return self.article_title

class Question(models.Model):
    question_research=models.ForeignKey(Research, on_delete=models.CASCADE)
    question_firstmadeat=models.ForeignKey(Article, on_delete=models.CASCADE)
    question_text=models.CharField(max_length=200)
    question_firstmadeby=models.ForeignKey(User, on_delete=models.CASCADE)
    question_firstmadeas=models.CharField(max_length=20)
    question_popularity=models.PositiveIntegerField(default=1)
    question_abstract=models.IntegerField(default=0)
    question_pubdate = models.DateTimeField('date published')
    def generate(self):
        self.save()
    def __str__(self):
        return self.question_text


class Questionlink(models.Model):
    link_article=models.ForeignKey(Article)
    link_question=models.ForeignKey(Question)
    link_research=models.ForeignKey(Research, on_delete=models.CASCADE)
    link_madeby=models.ForeignKey(User)
    link_madeat=models.IntegerField(default=1)
    def generate(self):
        self.save()
    def __str__(self):
        return self.link_question.question_text


class Quizlink(models.Model):
    link_article=models.ForeignKey(Article)
    link_question=models.ForeignKey(Question)
    link_research=models.ForeignKey(Research, on_delete=models.CASCADE)
    link_madeby=models.ForeignKey(User)
    link_refsentids=models.IntegerField(default=1)
    link_reftexts=models.CharField(max_length=1000)
    def generate(self):
        self.save()
    def __str__(self):
        return self.link_reftexts
    
class SurveyEmbed(models.Model):
    survey_no=models.IntegerField(default=0)
    survey_name=models.CharField(max_length=100)
    survey_link=models.CharField(max_length=400)
    def __str__(self):
        return self.survey_name
    

