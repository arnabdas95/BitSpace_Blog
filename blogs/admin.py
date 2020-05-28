from django.contrib import admin
from .models import Profile, Article
    #,Likes_It

admin.site.register(Profile)
admin.site.register(Article)
#admin.site.register(Likes_It)