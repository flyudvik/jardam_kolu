import logging
import pkgutil

from django.apps import AppConfig

from .scenarios.abstract import Scenario
from .scenarios.constants import SKIPPABLE

logger = logging.getLogger("quiz")


class QuizConfig(AppConfig):
    name = 'app.quiz'
    verbose_name = 'Quiz'
    scenarios = []

    @classmethod
    def get_scenarios(cls):
        return cls.scenarios

    @classmethod
    def get_scenario(cls, language=None):
        if language is None:
            logger.debug("There is no language provided, fuck you")
            return None
        return list(filter(lambda x: x.language == language, cls.scenarios))[0]

    def ready(self):
        from . import scenarios

        package = scenarios
        prefix = package.__name__ + "."

        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix):
            d = len(list(filter(lambda x: x in modname, SKIPPABLE)))
            if d > 0:
                continue
            module = __import__(modname)
            logger.debug("Importing {} module.".format(modname))
            self.scenarios.append(Scenario(
                script=modname, scenario=module.scenario,
                language=module.language,
            ))
