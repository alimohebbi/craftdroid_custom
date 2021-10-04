import pandas as pd

from config import Config
from manager.migrate import migration_process

config = Config()


def load_migrations():
    return pd.read_csv(config.migration_plan_path)


def find_or_create():
    global results
    condition = (results['word_embedding'] == sm_config['word_embedding']) & \
                (results['training_set'] == sm_config['training_set']) & \
                (results['algorithm'] == sm_config['algorithm']) & \
                (results['descriptors'] == sm_config['descriptors']) & \
                (results['src'] == sm_config['src']) & \
                (results['task'] == sm_config['task']) & \
                (results['target'] == sm_config['target'])

    if len(results.index[condition].tolist()) == 1:
        return results.index[condition].tolist()[0]
    results = results.append(sm_config, ignore_index=True)
    return results.index[[-1]].to_list()[0]


def forbidden_config(semantic_config):
    if semantic_config['word_embedding'] in ['jaccard', 'edit_distance', 'random']:
        return semantic_config['training_set'] != 'empty'
    if semantic_config['word_embedding'] in ['use', 'nnlm', 'bert']:
        return semantic_config['training_set'] != 'standard'
    if semantic_config['word_embedding'] not in ['jaccard', 'edit_distance', 'random']:
        return semantic_config['training_set'] == 'empty'


def is_config_in_sample(semantic_config):
    samples = pd.read_csv(config.config_samples)
    return ((samples['word_embedding'] == semantic_config['word_embedding']) & (
            samples['training_set'] == semantic_config['training_set']) &
            (samples['algorithm'] == semantic_config['algorithm']) &
            (samples['descriptors'] == semantic_config['descriptors'])
            ).any()


def first_round_migration():
    if forbidden_config(sm_config) or not is_config_in_sample(sm_config):
        return
    row_index = find_or_create()
    if results.iloc[row_index]['error'] != '':
        print_exist_message(row_index)
        return
    migration_process(results, row_index)


def redo_failed_migaratoins():
    if forbidden_config(sm_config) or not is_config_in_sample(sm_config):
        return
    row_index = find_or_create()
    if bool(results.iloc[row_index]['error']) and not results.iloc[row_index]['test_exist']:
        print('Redo the failed migration: ' + config_str(row_index))
        migration_process(results, row_index)


def print_exist_message(row_index):
    str_row = config_str(row_index)
    print("Already exist: " + str_row)


def config_str(row_index):
    col = list(results.columns)
    col.remove('error')
    col.remove('test_exist')
    conf = dict(results.iloc[row_index][col]).values()
    str_row = '_'.join(conf)
    return str_row


def get_results():
    try:
        return pd.read_csv(config.results)
    except FileNotFoundError:
        columns = ["word_embedding", "training_set", "algorithm", "descriptors", 'src', 'target', 'error', 'test_exist']
        return pd.DataFrame(columns=columns)


src_index = 0
target_index = 1


def get_subjects():
    migration_subjects = load_migrations()
    if target_index > migration_subjects.shape[0]:
        return None
    subject = {}
    subject['src'] = migration_subjects.iloc[src_index]['src']
    subject['target'] = migration_subjects.iloc[target_index]['src']
    subject['task'] = migration_subjects.iloc[target_index]['task']
    return subject


def update_subject_index():
    global src_index, target_index
    if forbidden_config(sm_config) or not is_config_in_sample(sm_config):
        return
    row_index = find_or_create()
    if bool(results.iloc[row_index]['test_exist']):
        src_index = target_index
    target_index += 1


if __name__ == '__main__':
    results = get_results()
    results.fillna('', inplace=True)
    for embedding in config.embedding:
        for train_set in config.train_sets:
            for algorithm in config.algorithm:
                for descriptors in config.descriptors:
                    sm_config = {'word_embedding': embedding,
                                 'training_set': train_set,
                                 'algorithm': algorithm,
                                 'descriptors': descriptors,
                                 'error': '',
                                 'test_exist': ''}
                    if forbidden_config(sm_config) or not is_config_in_sample(sm_config):
                        continue
                    subjects = get_subjects()
                    while subjects is not None:
                        sm_config['src'] = subjects['src']
                        sm_config['target'] = subjects['target']
                        sm_config['task'] = subjects['task']
                        first_round_migration()
                        redo_failed_migaratoins()
                        update_subject_index()
                        subjects = get_subjects()
                        results.to_csv(config.results, index=False)

