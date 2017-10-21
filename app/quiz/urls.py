from django.conf.urls import url

from . import views


urlpatterns = [
    url(
        r'^scenario.json/$',
        views.get_quiz_scenario,
        name='get-scenario'
    ),
]
