import shutil
import subprocess
import json

from config import Config

config = Config()


def remove_dir(path):
    try:
        shutil.rmtree(path)
    except FileNotFoundError as a:
        pass


def add_config_file(migration):
    file_path = config.root + '/matching_client/sm_config'
    col = list(migration.keys())
    col = list(set(col) - {'error', 'test_exist', 'src', 'target', 'task'})
    conf = dict(migration[col])
    conf['app_pair'] = '-'.join([migration['src'], migration['target'], migration['task'], 'craftdroid'])
    with open(file_path, 'w') as f:
        json.dump(conf, f)


def prepare_for_migration(migration):
    add_config_file(migration)
