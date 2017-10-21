import logging
from collections import defaultdict
import string_utils as su


from .constants import *

logger = logging.getLogger("scenario validation")


def dfs(graph, start, end):
    fringe = [(start, [])]
    while fringe:
        state, path = fringe.pop()
        if path and state == end:
            yield path
            continue
        for next_state in graph[state]:
            if next_state in path:
                continue
            fringe.append((next_state, path+[next_state]))


def is_valid_scenario(scenario):
    """
    Validation of the scenario object
    :param scenario: the scenario object
    :return:
    """
    logger.debug("Starting validation of the scenario object")

    tree = scenario.scenario
    q_ids = tree.keys()
    graph = defaultdict([])

    for q_id, question in tree.items():
        answers = question.get('answers')
        assert len(answers) > 0, "Question should always contain answer"
        answer_ids = answers.keys()
        for a_id, answer in answers.items():
            answer_type = answer['type']
            assert 'text' in answer and type(answer.get('text')) == str,\
                "There should be field of the text and it should be a str"
            if answer_type in [ARTICLE, EXTERNAL, SBSS]:
                assert su.is_url(answer['content']), "Content of the answer of this type should be url"
            elif answer_type in [QUESTION, ]:
                assert answer['content'] in q_ids, \
                    "Content of the question type answer should be in declared question ids."
                graph[q_id].append(answer['content'])
            else:
                raise AssertionError("There are no such handler for type as {}".format(answer_type))

    logger.debug("Searching cycles in the tree")
    cycles = [[node] + path for node in graph for path in dfs(graph, node, node)]
    assert cycles == 0, "There should be no cycles for any node/question"
    logger.debug("Finished validation of the scenario object")
    return True
