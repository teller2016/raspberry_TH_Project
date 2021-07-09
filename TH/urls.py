"""TH URL Configuration

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
from django.urls import path
import appTH.views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', appTH.views.home, name="home"),
    path('restart/<word>/<second>', appTH.views.restart, name="restart"),
    path('end', appTH.views.end, name="end"),
    path('th_csv/<word>/', appTH.views.th_csv, name="th_csv"),
    path('graph', appTH.views.graph, name="graph"),
    path('result', appTH.views.result, name="result"),
    
    path('getThData/', appTH.views.getThData, name="getThData"),
    path('getThState/', appTH.views.getThState, name="getThState"),
    path('getAllThData/', appTH.views.getAllThData, name="getAllThData"),
    
    path('beforeResult', appTH.views.beforeResult, name="beforeResult"),
]
