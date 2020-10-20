from django.shortcuts import render
from django.http import HttpResponse, Http404, JsonResponse
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core import serializers
from django.conf import settings
import json
import jsonify
import tweepy
import pickle
from .config import consumer_key, consumer_secret, access_token, access_token_secret
import codecs
import numpy as np
from nltk.tokenize import RegexpTokenizer
from .models import TweetModel, SearchTermModel
from django.forms.models import model_to_dict
from geopy.geocoders import Bing, Nominatim
from geopy.exc import GeocoderTimedOut
from multiprocessing import Pool
import requests, datetime
import time, uuid, copy, string
from django.db.models import Count
from nltk.corpus import stopwords
from twitterweb.utility_functions import get_result, live_test, load_embeddings, map_to_chart_data
from django.db import connection, connections
from apscheduler.scheduler import Scheduler
from datetime import datetime
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
# Twitter
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
# api = tweepy.API(auth,wait_on_rate_limit=True, parser=tweepy.parsers.JSONParser())
api = tweepy.API(auth, wait_on_rate_limit=True)

sched = Scheduler()
sched.daemonic = False
sched.start()
def homepage(request):
    return render(request, "build/index.html")

@api_view(["GET"])
def getTopTerms(request):
    res = SearchTermModel.objects.all().values('text').annotate(total=Count('text')).order_by('-total')[:10]
    return HttpResponse(json.dumps(list(res)), content_type="application/json")

@api_view(["GET"])
def getlivetest(request):
    # set_session(session)
    print(request.GET.get("text"))
    result = live_test(str(request.GET.get("text")))
    # sid = SentimentIntensityAnalyzer()
    # ss = sid.polarity_scores(str(request.GET.get("text")))
    # score = (ss['compound'] + 1) / 2  #skaliranje izmedju 0 i 1
    return HttpResponse(json.dumps(result), content_type="application/json")
@api_view(["GET"])
def getpiechart(request):

    start_time = time.time()
    # set_session(session)
    tweets = []
    positive_tweets = []
    negative_tweets = []
    neutral_tweets = []
    # results = api.search(q="#" + request.GET.get("text") + " -filter:retweets",rpp=5,lang="en", tweet_mode='extended')
    # return  HttpResponse(json.dumps(results), content_type="application/json");
    locations_to_code = []
    tweets_to_locate = []
    text =  request.GET.get("text")
    if text == '':
        content = {'message': "Search term can't be empty!"}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    searchTerm = SearchTermModel(text = text)
    searchTerm.save()
    if request.GET.get("useTimeFilter") == "true":
        date_since = datetime.datetime.strptime(request.GET.get("dateSince") , '%d-%m-%Y')
        print(date_since)
        date_until = datetime.datetime.strptime(request.GET.get("dateUntil") , '%d-%m-%Y')
        if date_since > date_until or date_since < (datetime.datetime.today() - datetime.timedelta(days=7)) or date_until > datetime.datetime.today():
            print("ERROR")
            content = {'message': 'Dates are invalid!'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        search_result = tweepy.Cursor(api.search, q="#" + request.GET.get("text") + " -filter:retweets",
                                    count=100, lang="en", since=date_since,
                    until=date_until, tweet_mode="extended").items(int(request.GET.get("count")))
        try:
            first = search_result.next()
        except StopIteration:
            content = {'message': "Sorry, there is no tweets about " +  request.GET.get("text") + "."}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
        
            
    else:
        search_result = tweepy.Cursor(api.search, q="#" + request.GET.get("text") + " -filter:retweets",
                                count=100, lang="en", tweet_mode="extended").items(int(request.GET.get("count")))

    try:
        first = search_result.next()
    except StopIteration:
        content = {'message': "Sorry, there is no tweets about " +  request.GET.get("text") + "."}
        return Response(content, status=status.HTTP_400_BAD_REQUEST)
    thisdict, cnt, pos_cnt, neu_cnt, neg_cnt, very_neg_cnt, very_pos_cnt = get_result(search_result)
    # thisdict, cnt, pos_cnt, neu_cnt, neg_cnt= get_result(search_result)

    duration = time.time() - start_time
    print("duration: " + str(duration))
    print("length: " + str(len(tweets)))
    return HttpResponse(json.dumps(thisdict), content_type="application/json")

@api_view(["GET"])
def get_dashboard_data(request):
    # query = "SELECT * FROM SCHEDULED_TASK WHERE JOB_UUID = '59e08826-f1d9-11ea-ac11-0492265afb6e'"
    query = "SELECT SEARCH_TERM, UUID FROM SENTIMENT_JOB"
    with connections['postgres'].cursor() as cursor:
        cursor.execute(query)
        job_result = cursor.fetchall()
    # print(result)
    response = []
    for j in job_result:
        with connections['postgres'].cursor() as cursor:
            cursor.execute("""
                SELECT * FROM SCHEDULED_TASK WHERE JOB_UUID = %s;
                """, [
                    str(j[1])
                ]
            )
            result = cursor.fetchall()
        response.append(map_to_chart_data(result, str(j[0])))
    return HttpResponse(json.dumps(response), content_type="application/json")
   

@api_view(["GET"])
def create_sentiment_job(request):
    
    job_uuid = uuid.uuid1()

    with connections['postgres'].cursor() as cursor:
        cursor.execute("""
            INSERT INTO sentiment_job (
                search_term, first_analysis_tmstmp, uuid, active)
                VALUES (
                %s, CLOCK_TIMESTAMP(), %s, 'Y'
                )
            """, [
                request.GET.get("text"), job_uuid
            ]
        )   
    start_datetime = datetime.strptime(request.GET.get("startDate"), '%d-%m-%Y %H:%M')
    print(start_datetime)
    interval = request.GET.get("interval")
    if interval =='undefined' or interval == 'hour':
        sched.add_cron_job(scheduled_sentiment_task,  hour='0-23', minute=str(start_datetime.minute), start_date=start_datetime, args=[request.GET.get("text"), job_uuid])
    else:
        sched.add_cron_job(scheduled_sentiment_task, day='0-31', hour=str(start_datetime.hour), minute=str(start_datetime.minute), start_date=start_datetime, args=[request.GET.get("text"), job_uuid])

    content = {'message': "OK" +  request.GET.get("text") + "."}
    return Response(content, status=status.HTTP_200_OK)


def scheduled_sentiment_task(search_term, job_uuid):

    search_result = tweepy.Cursor(api.search, q="#" + search_term + " -filter:retweets",
                                count=100, lang="en", tweet_mode="extended").items(1000)

    thisdict, cnt, pos_cnt, neu_cnt, neg_cnt, very_neg_cnt, very_pos_cnt = get_result(search_result)

    pos_percent = round(pos_cnt/cnt*100, 2)
    neu_percent = round(neu_cnt/cnt*100, 2)
    neg_percent = round(neg_cnt/cnt*100, 2)
    very_neg_percent = round(very_neg_cnt/cnt*100, 2)
    very_pos_percent = round(very_pos_cnt/cnt*100, 2)
    with connections['postgres'].cursor() as cursor:
        cursor.execute("""
            INSERT INTO public.scheduled_task(
                positive_res, negative_res, neutral_res, very_negative_res, very_positive_res, tmstmp, job_uuid)
            VALUES (%s, %s, %s, %s, %s, CLOCK_TIMESTAMP(), %s);
            """, [
                pos_percent, neg_percent, neu_percent, very_neg_percent, very_pos_percent, job_uuid
            ]
        )

        cursor.execute("""
            UPDATE sentiment_job
            SET last_analysis_tmstmp = CLOCK_TIMESTAMP(),
                analysis_cnt = analysis_cnt + 1
            WHERE uuid = %s;
            """, [
                str(job_uuid)
            ]
        )

    print("Executed: " + str(search_term))