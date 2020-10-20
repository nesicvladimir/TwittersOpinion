from django.db import models

# Create your models here.

class TweetModel(models.Model):
    text=models.CharField(max_length=280, default="def")
    username=models.CharField(max_length=200, null=True)
    label=models.CharField(max_length=20,null=True)
    score=models.FloatField(null=True) 
    created_at=models.CharField(null=True, max_length=255)
    location=models.CharField(null=True, max_length=255)
    lat=models.FloatField(null=True) 
    lng=models.FloatField(null=True) 
    country_code=models.CharField(max_length=5, null=True)
    state_code=models.CharField(max_length=5, null=True)
    session=models.CharField(null=True, max_length=255)

    # class Meta:
    #     managed=True


class SearchTermModel(models.Model):
    text=models.CharField(max_length=280, null=False)