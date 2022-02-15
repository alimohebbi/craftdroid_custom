import json
from abc import ABC, abstractmethod

from config import Config
from matching_client.match_object import MatchObject
from matching_client.object_sender import send_object

config = Config()


class FileNameFinder:
    src_file_names = None
    target_file_names = None
    _instance = None
    target_app = None
    src_app = None

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            cls._instance = FileNameFinder()
        return cls._instance

    def set_apps(self, migration):
        self.src_app = migration.split('-')[0]
        self.target_app = migration.split('-')[1]
        src_path = config.image_repo + '/' + self.src_app + '.json'
        target_path = config.image_repo + '/' + self.target_app + '.json'
        with open(src_path) as json_file:
            self.src_file_names = json.load(json_file)
        with open(target_path) as json_file:
            self.target_file_names = json.load(json_file)

    def find_file_by_src_id(self, resource_id):
        return self._find_file_by_id(resource_id, self.src_file_names)

    def find_file_by_target_id(self, resource_id):
        return self._find_file_by_id(resource_id, self.target_file_names)

    @staticmethod
    def _find_file_by_id(resource_id, file_names):
        result = {}
        for file in file_names.keys():
            names = file_names[file]
            if resource_id in names:
                result[file] = names[resource_id]
        return result

    def get_match_object(self, activity, candidates_activity):
        src_dummy_widget = {'text': activity, 'class': 'Button'}
        candidates_dummy_widgets = [{'text': i, 'class': 'Button'} for i in candidates_activity]
        match_obj = MatchObject(src_dummy_widget, candidates_dummy_widgets, None)
        return match_obj


class FileNameAdder(ABC):
    @classmethod
    def add_file_name_to_widgets(cls, widgets: list):
        if widgets is None:
            return
        for w in widgets:
            resource_id = w['resource-id']
            results = cls._find_file_by_src_id(resource_id)
            file_name = ''
            if len(results):
                best_activity = cls._find_best_activity(w['activity'], list(results.keys()))
                if best_activity:
                    file_name = results[best_activity]

            w['file_name'] = file_name

    @staticmethod
    def _find_best_activity(activity, candidates):
        file_name_finder = FileNameFinder.get_instance()
        match_object = file_name_finder.get_match_object(activity, candidates)
        scored_indexes = send_object(match_object.get_json())
        scored_widgets = []
        for k in scored_indexes:
            scored_widgets.append((candidates[int(k)], scored_indexes[k]))
        scored_widgets.sort(key=lambda x: x[1], reverse=True)
        return scored_widgets[0][0] if len(scored_widgets) else None

    @staticmethod
    @abstractmethod
    def _find_file_by_src_id(resource_id):
        pass


class SourceFileNameAdder(FileNameAdder):
    @staticmethod
    def _find_file_by_src_id(resource_id):
        file_name_finder = FileNameFinder.get_instance()
        return file_name_finder.find_file_by_src_id(resource_id)


class TargetFileNameAdder(FileNameAdder):
    @staticmethod
    def _find_file_by_src_id(resource_id):
        file_name_finder = FileNameFinder.get_instance()
        return file_name_finder.find_file_by_target_id(resource_id)


def addFileNameToMatchObject(m_obj: MatchObject):
    TargetFileNameAdder.add_file_name_to_widgets(m_obj.target_labels_map.values())
    TargetFileNameAdder.add_file_name_to_widgets(m_obj.candidates_map.values())
    SourceFileNameAdder.add_file_name_to_widgets([m_obj.source_event])
    SourceFileNameAdder.add_file_name_to_widgets(m_obj.source_labels_map.values())
