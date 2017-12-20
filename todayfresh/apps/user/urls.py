from django.conf.urls import url
from apps.user.views import RegisterViews,ActiveViews,LoginViews

urlpatterns = [
    #url(r'^register$',views.register,name='register'),
    #url(r'^register_handle$', views.register_handle, name='register_handle'),
    url(r'^register$', RegisterViews.as_view(),name='register'),
    url(r'^active/(?P<token>.*)$', ActiveViews.as_view(),name='active'),
    url(r'^login$',LoginViews.as_view(),name='login'),
]
