import json
from rest_framework.response import Response
from django.utils.translation import get_language_from_request

from .apps import QuizConfig


def get_quiz_scenario(request, *args, **kwargs):
    language = get_language_from_request(request)
    scenario = QuizConfig.get_scenario(language)

    # TODO: should get visitor data
    return Response(
        scenario.as_json()
    )
