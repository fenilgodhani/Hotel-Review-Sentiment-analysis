from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$',views.index , name="index"),
	url(r'^submit',views.submit , name="submit"),
	url(r'^check_index',views.check_index,name="check_index")
]
