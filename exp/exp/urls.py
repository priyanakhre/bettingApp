"""exp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from . import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^exp/all_bets/$', views.all_bets, name='exp-all_bets'),
    url(r'^exp/create_bet/$', views.create_bet, name='exp-create-bet'),
    url(r'^exp/recent_bets/(?P<count>[0-9]+)/$', views.recent_bets, name='exp-recent_bets'),
    url(r'^exp/all_categories/$', views.all_categories, name='exp-all_categories'),
    url(r'^exp/bet_detail/(?P<bet_id>[0-9]+)/$', views.bet_detail, name='exp-bet_detail'),
    url(r'^exp/bet_responses/(?P<bet_id>[0-9]+)/$', views.bet_responses, name='exp-bet_responses'),
    url(r'^exp/response_detail/(?P<response_id>[0-9]+)/$', views.response_detail, name='exp-response_detail'),
    url(r'^exp/accounts/login/$', views.login, name="login"),
    url(r'^exp/accounts/logout/$', views.logout, name='logout'),
    url(r'^exp/accounts/check_auth/$', views.check_authenticator, name='check-authenticator'),
    url(r'^exp/user/create$', views.create_user, name='create-user'),
    url(r'^exp/search/$', views.find_bet, name='find-bet'),

]