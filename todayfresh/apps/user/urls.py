from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from apps.user.views import RegisterViews,ActiveViews,LoginViews,LogoutViews,UsercenterInfoViews,UsercenterSiteViews,UsercenterOrderViews

urlpatterns = [
    #url(r'^register$',views.register,name='register'),
    #url(r'^register_handle$', views.register_handle, name='register_handle'),
    url(r'^register$', RegisterViews.as_view(),name='register'),
    url(r'^active/(?P<token>.*)$', ActiveViews.as_view(),name='active'),
    url(r'^login$',LoginViews.as_view(),name='login'),
    url(r'^logout$',LogoutViews.as_view(),name='logout'),

    # url(r'^centerInfo$',login_required(UsercenterInfoViews.as_view()),name='UsercenterInfoViews'),
    # url(r'^centerOrder$',login_required(UsercenterOrderViews.as_view()),name='UsercenterOrderViews'),
    # url(r'^centerSite$',login_required(UsercenterSiteViews.as_view()),name='UsercenterSiteViews'),
    url(r'^centerInfo$',UsercenterInfoViews.as_view(),name='UsercenterInfoViews'),
    url(r'^centerOrder$',UsercenterOrderViews.as_view(),name='UsercenterOrderViews'),
    url(r'^centerSite$',UsercenterSiteViews.as_view(),name='UsercenterSiteViews'),
]
