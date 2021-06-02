import ntpath
import os
import pathlib
import re
import shutil

from config import Config

config = Config()


def config_str(migration):
    col = list(migration.keys())
    col.remove('error')
    col.remove('test_exist')
    col.remove('src')
    col.remove('target')
    col.remove('task')
    conf = dict(migration[col]).values()
    str_row = '_'.join(conf)
    return str_row


def get_log_file_path(migration):
    sub_dir = config_str(migration)
    full_dir = config.migration_log_dir + '/' + sub_dir
    os.makedirs(full_dir, exist_ok=True)
    return full_dir + '/' + migration['src'] + '-' + migration['target'] + '-' + migration['task'] + '.txt'


def check_log_error(migration):
    file = get_log_file_path(migration)
    with open(file, 'r') as file:
        data = file.read().replace('\n', '')
    return True if ('error' in data) or ('Exception' in data) or ('Error' in data) else False


def find_test_file(migration):
    config_id = '-'.join([migration['src'], migration['target'], migration['task']]) + '.json'
    src_path = migration['src'][:2]
    target_path = os.path.join(config.root, 'test_repo', src_path, migration['task'],
                               'generated', config_id)
    if os.path.isfile(target_path):
        return target_path
    return None


def move_test_file(migration, test_file_path):
    sub_dir = config_str(migration)
    full_dir = config.generated_dir + '/' + sub_dir
    dir_for_migration = full_dir + '/' + migration['src'] + '-' + migration['target'] + '-' + migration['task']
    os.makedirs(dir_for_migration, exist_ok=True)
    file_name = ntpath.basename(test_file_path)
    destination_path = dir_for_migration + '/' + file_name
    shutil.move(str(test_file_path), destination_path)


def post_migration(migration):
    err_exist = check_log_error(migration)
    test_file_path = find_test_file(migration)
    test_exist = False
    if test_file_path:
        move_test_file(migration, test_file_path)
        test_exist = True
    return err_exist, test_exist
