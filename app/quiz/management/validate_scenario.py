"""
Command for validating scenarios that are written inside scenarios folder
"""
import traceback

from django.core.management.base import BaseCommand

from ..apps import QuizConfig
from ..scenarios.validators import is_valid_scenario


class ValidateScenarioCommand(BaseCommand):
    def handle(self, *args, **kwargs):
        scenarios = QuizConfig.scenarios
        for i, scenario in enumerate(scenarios):
            try:
                assert is_valid_scenario(scenario)
            except AssertionError:
                traceback.print_last()
                print("Scenario #{} failed validation".format(i))
