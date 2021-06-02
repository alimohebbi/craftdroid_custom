import os
import yaml


class Config(object):

    def __init__(self):
        THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(THIS_FOLDER, 'config.yml')
        with open(path, 'r') as ymlfile:
            self._config = yaml.load(ymlfile, Loader=yaml.FullLoader)

    @property
    def apks_dir(self):
        return self._get_property('apks_dir')

    @property
    def sm_conf_path(self):
        return self._get_property('sm_conf_path')

    @property
    def decompile_temp(self):
        return self._get_property('decompile_temp')

    @property
    def image_repo(self):
        return self._get_property('image_repo')

    @property
    def train_sets(self):
        return self._get_property('train_set')

    @property
    def embedding(self):
        return self._get_property('embedding')

    @property
    def algorithm(self):
        return self._get_property('algorithm')

    @property
    def descriptors(self):
        return self._get_property('descriptors')

    @property
    def migration_plan_path(self):
        return self._get_property('migration_plan_path')

    @property
    def results(self):
        return self._get_property('results')

    @property
    def migration_timeout(self):
        return self._get_property('migration_timeout')

    @property
    def appium_port(self):
        return self._get_property('appium_port')

    @property
    def emulator(self):
        return self._get_property('emulator')

    @property
    def clean_file(self):
        return self._get_property('clean_file')

    @property
    def migration_log_dir(self):
        return self._get_property('migration_log_dir')

    @property
    def generated_dir(self):
        return self._get_property('generated_dir')

    @property
    def root(self):
        return self._get_property('root')

    def _get_property(self, property_name):
        if property_name not in self._config.keys():  # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]
