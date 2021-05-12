import json


class MatchObject:

    def __init__(self, source_event, candidates: list):
        candidates_map = {}
        for index, value in enumerate(candidates):
            candidates_map[index] = value
        self._json_obj = {'sourceEvent': source_event, 'candidates': candidates_map}

    def get_json(self):
        return self._json_obj
