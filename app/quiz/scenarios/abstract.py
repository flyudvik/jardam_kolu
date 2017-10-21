import json


class Scenario(object):
    def __init__(self, script, scenario, language):
        """
        :param script: absolute path to the script as module string
        :param scenario: dictionary of used data that will be returned
        """
        self.script = script
        self.scenario = scenario
        self.language = language

    def as_json(self):
        return json.dumps(self.scenario)
