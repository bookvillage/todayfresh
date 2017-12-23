from django.conf.urls import url
from apps.goods.views import IndexViews
urlpatterns = [
    url(r'^$',IndexViews.as_view(),name='index')
]
