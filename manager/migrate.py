import multiprocessing
import traceback

import Explorer
from config import Config
from .emulator import start_emulator, stop_emulator
from .post import post_migration, get_log_file_path
from .pre import prepare_for_migration

config = Config()


def write_file(input_text, log_file):
    f = open(log_file, "w")
    f.write(input_text)
    f.close()


def log_killed_process(logfile):
    message = 'Timeout Error: **** Migration is killed ****'
    print(message)
    logfile.write(message)


def craftdroid_process(migration, logfile):
    config_id = '-'.join([migration['src'], migration['target'], migration['task']])
    try:
        Explorer.start(config_id, config.appium_port, config.emulator, logfile)
    except Exception:
        trace = traceback.format_exc()
        logfile.write(trace)
        traceback.print_exc()


def run_craftdroid(migration):
    logfile = open(get_log_file_path(migration), 'w')
    p = multiprocessing.Process(target=craftdroid_process, name="Start", args=(migration, logfile))
    p.start()
    p.join(config.migration_timeout)
    if p.exitcode is None:
        log_killed_process(logfile)
    p.kill()
    logfile.close()


def migration_process(migration_df, i):
    row = migration_df.iloc[i]
    prepare_for_migration(row)
    # start_emulator()
    run_craftdroid(row)
    # stop_emulator()
    err_exist, test_exist = post_migration(row)
    migration_df.at[i, 'error'] = err_exist
    migration_df.at[i, 'test_exist'] = test_exist
