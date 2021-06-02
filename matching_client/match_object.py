import json

from config import Config

config = Config()


class MatchObject:
    _sm_config = None

    def __init__(self, source_event, candidates: list, target_labels: list, source_labels=None):
        self.candidates_map = self.indexify_list(candidates)
        self.target_labels_map = self.indexify_list(target_labels)
        self.source_labels_map = self.indexify_list(source_labels)
        self.source_event = source_event
        self._json_obj = {'sourceEvent': self.source_event, 'candidates': self.candidates_map,
                          'targetLabels': self.target_labels_map,
                          'sourceLabels': self.source_labels_map, 'smConfig': self._sm_config}

    @staticmethod
    def indexify_list(widgets):
        if widgets is None:
            return {}
        w_map = {}
        for index, value in enumerate(widgets):
            w_map[index] = value
        return w_map

    def get_json(self):
        return self._json_obj

    @classmethod
    def set_sm_config(cls, sm_config):
        cls._sm_config = json.dumps(sm_config)


def setup_sm_config():
    with open(config.sm_conf_path) as json_file:
        sm_config = json.load(json_file)
    MatchObject.set_sm_config(sm_config)
