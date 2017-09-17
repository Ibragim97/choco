from django.conf.urls import url
from .  import views



urlpatterns = [
    url(r'^get/', views.ApiGetView.as_view(), name='get'),
    url(r'^update/', views.ApiUpdateView.as_view(), name='update'),
]
