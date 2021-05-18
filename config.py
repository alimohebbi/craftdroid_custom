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
    def decompile_temp(self):
        return self._get_property('decompile_temp')

    @property
    def image_repo(self):
        return self._get_property('image_repo')


    def _get_property(self, property_name):
        if property_name not in self._config.keys():  # we don't want KeyError
            return None  # just return None if not found
        return self._config[property_name]

