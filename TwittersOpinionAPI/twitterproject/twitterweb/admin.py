from django.contrib import admin
from .models import TweetModel, SearchTermModel

admin.site.register(TweetModel)
admin.site.register(SearchTermModel)
# Register your models here.
