from django.conf.urls import patterns, url

from polls import views

urlpatterns = patterns(
    '',
    url(r'^$', views.upload, name='uplink'),
    url(r'^download/(.*)', views.download, name="download"),
    url(r'^exchange/(.*)', views.exchange, name="exchange"),
    url(r'^parse/(.*)', views.parse, name="parse")
)