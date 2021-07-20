import multiprocessing
import subprocess
import sys
import time
import traceback
from threading import Timer

import Explorer
from config import Config
from .post import post_migration, get_log_file_path
from .pre import prepare_for_migration

config = Config()


def write_file(input_text, log_file):
    f = open(log_file, "w")
    f.write(input_text)
    f.close()


def kill(process):
    process[0].kill()
    print('killed')
    print(process[1]['src'] + ' to ' + process[1]['target'])


def craftdroid_process(migration):
    logfile = open(get_log_file_path(migration), 'w')
    config_id = '-'.join([migration['src'], migration['target'], migration['task']])
    try:
        Explorer.start(config_id, config.appium_port, config.emulator, logfile)
        logfile.close()
    except Exception:
        trace = traceback.format_exc()
        logfile.write(trace)
        logfile.close()
        traceback.print_exc()


def run_craftdroid(migration):
    p = multiprocessing.Process(target=craftdroid_process, name="Start", args=(migration,))
    p.start()
    p.join(config.migration_timeout)
    p.kill()


def migration_process(migration_df, i):
    row = migration_df.iloc[i]
    prepare_for_migration(row)
    run_craftdroid(row)
    err_exist, test_exist = post_migration(row)
    migration_df.at[i, 'error'] = err_exist
    migration_df.at[i, 'test_exist'] = str(test_exist)
