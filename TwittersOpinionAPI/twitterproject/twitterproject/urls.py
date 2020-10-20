"""twitterproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from twitterweb import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('twitterweb.urls')),
    path('gettopterms', views.getTopTerms),
    path('getpiechart', views.getpiechart),
    path('getlivetest', views.getlivetest),
    path('createSentimentJob', views.create_sentiment_job),
    path('getDashboardData', views.get_dashboard_data)
]
