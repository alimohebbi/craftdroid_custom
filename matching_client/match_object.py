import json

from config import Config

config = Config()


class MatchObject:
    _sm_config = None

    def __init__(self, source_event, candidates: list, target_labels: list, source_labels=None):
        candidates_map = self.indexify_list(candidates)
        target_labels_map = self.indexify_list(target_labels)
        source_labels_map = self.indexify_list(source_labels)
        self._json_obj = {'sourceEvent': source_event, 'candidates': candidates_map, 'targetLabels': target_labels_map,
                          'sourceLabels': source_labels_map, 'smConfig': self._sm_config}

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

    @staticmethod
    def get_dynamic_widgets(widgets):
        return [i for i in widgets if len(i) > 13 and 'static' not in i]


    @staticmethod
    def add_static_flag(actionable_widget, label_widgets):
        for i in actionable_widget:
            i['static'] = True
        for i in label_widgets:
            i['static'] = True

    @staticmethod
    def get_static_widgets(widgets):
        return [i for i in widgets if len(i) < 13 or 'static' in i]

    @classmethod
    def set_sm_config(cls, sm_config):
        cls._sm_config = json.dumps(sm_config)


def setup_sm_config():
    with open(config.sm_conf_path) as json_file:
        sm_config = json.load(json_file)
    MatchObject.set_sm_config(sm_config)
