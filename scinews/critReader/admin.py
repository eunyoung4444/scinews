from django.contrib import admin
from .models import Article, Question,  Research, SurveyEmbed, Questionlink, Quizlink, AQrel 
# Register your models here.


admin.site.register(Article)
admin.site.register(Question)
admin.site.register(Research)
admin.site.register(Questionlink)
admin.site.register(Quizlink)
admin.site.register(SurveyEmbed)
admin.site.register(AQrel)
