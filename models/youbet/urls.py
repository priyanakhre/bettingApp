from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^api/v1/user/$', views.user_service, name='api-users'),
    url(r'^api/v1/user/(?P<user_id>[0-9]+)/$', views.user_service, name='api-user'),
    url(r'^api/v1/bet/$', views.bet_service, name='api-bets'),
    url(r'^api/v1/bet/(?P<bet_id>[0-9]+)/$', views.bet_service, name='api-bet'),
    url(r'^api/v1/response/$', views.response_service, name='api-responses'),
    url(r'^api/v1/response/(?P<response_id>[0-9]+)/$', views.response_service, name='api-response'),
    url(r'^api/v1/bet/(?P<bet_id>[0-9]+)/responses/$', views.get_all_responses_for_bet, name='api-responses_for_bet')
]