import json


class MatchObject:

    def __init__(self, source_event, candidates: list, target_labels: list, source_labels=None):
        candidates_map = self.indexify_list(candidates)
        target_labels_map = self.indexify_list(target_labels)
        source_labels_map = self.indexify_list(source_labels)
        self._json_obj = {'sourceEvent': source_event, 'candidates': candidates_map, 'targetLabels': target_labels_map,
                          'sourceLabels': source_labels_map}

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
        return [i for i in widgets if len(i) != 10]

    @staticmethod
    def get_static_widgets(widgets):
        return [i for i in widgets if len(i) == 10]

    def set_sm_config(self, sm_config):
        self._json_obj['smConfig'] = json.dumps(sm_config)
