import json
import os
import time
from copy import deepcopy
# from numpy import dot
# from numpy.linalg import norm
import pathlib


from const import TEST_REPO
from Databank import Databank
from test_attribute_extractor.test_attribute_extractor import run_craftdroid, check_run_possible, \
    get_element_attributes_list
from test_attribute_extractor.utils.craftdroid_parser import craftdroid_parse
from test_attribute_extractor.utils.utils import get_caps

import imaplib



IMPORTANT_FIELDS = ["checkable", "checked", "class", "clickable", "content-desc", "enabled", "focusable", "focused",
                    "long-clickable", "package", "password", "resource-id", "scrollable", "selection-start",
                    "selection-end", "selected", "text", "bounds", "displayed", "action"]


def remove_extra_fields(new_actions):
    for action in new_actions:
        key_list = list(action.keys())
        for key in key_list:
            if key not in IMPORTANT_FIELDS:
                action.pop(key)


class Util:

    @staticmethod
    def compose(attrs, tid, actions, pkg_name, act_name, event_type):
        attrs['tid'] = tid
        # attrs['order'] = order
        attrs['package'] = pkg_name
        attrs['activity'] = act_name
        attrs['ignorable'] = 'false'
        attrs['event_type'] = event_type  # 'gui', 'orcale', 'stepping'
        # if the action is wait_until_presence, adjust the content-desc for current app instead of that of the target app
        # e.g., ['wait_until_element_presence', 10, 'xpath', '//*[@content-desc="Open Menu"]']
        if actions[0] == 'wait_until_element_presence' and actions[2] == 'xpath' and '@content-desc=' in actions[3]:
            pre, post = actions[3].split('@content-desc=')
            post = f'@content-desc="{attrs["content-desc"]}"' + ''.join(post.split('"')[2:])
            actions[3] = pre + post
        attrs['action'] = actions
        return attrs

    @staticmethod
    def save_events(actions, config_id, is_success=True):
        # e.g., a41a-a42a-b41
        # folder = 'success' if is_success else 'failed'
        # fpath = [TEST_REPO, config_id[:2], config_id.split('-')[-1], 'generated', folder, config_id + '.json']
        fpath = [TEST_REPO, config_id[:2], config_id.split('-')[-1], 'generated', config_id + '.json']
        fdir = os.path.join(*fpath[:-1])
        if not os.path.exists(fdir):
            os.makedirs(fdir)
        fpath = os.path.join(*fpath)
        new_actions = [deepcopy(a) for a in actions]
        for a in new_actions:
            if a['class'] in ['EMPTY_EVENT', 'SYS_EVENT']:
                continue
            a['resource-id'] = a['id-prefix'] + a['resource-id']
            a.pop('id-prefix', "")
        remove_extra_fields(new_actions)
        with open(fpath, 'w') as f:
            json.dump(new_actions, f, indent=2)

    @staticmethod
    def save_aug_events(actions, fpath):
        with open(fpath, 'w') as f:
            json.dump(actions, f, indent=2)

    @staticmethod
    def find_file_path(config_id, target):
        fpath = [TEST_REPO, config_id[:2], config_id.split('-')[-1]]
        sub_dir = ''
        if target == 'generated':
            fpath += ['generated', sub_dir, config_id + '.json']
        elif target == '0-step':
            fpath += ['generated', '0-step', sub_dir, config_id + '.json']
        elif target == '1-step':
            fpath += ['generated', '1-step', sub_dir, config_id + '.json']
        elif target == '2-step':
            fpath += ['generated', '2-step', sub_dir, config_id + '.json']
        elif target == 'base_from':
            fpath += ['base', config_id.split('-')[0] + '.json']
        elif target == 'base_to':
            fpath += ['base', config_id.split('-')[1] + '.json']
        else:
            assert False, "Wrong target"
        fpath = os.path.join(*fpath)
        assert os.path.exists(fpath), f"Invalid file path: {fpath}"
        return fpath

    @staticmethod
    def run_source_test(file):
        caps, app_package = get_caps(file)
        run_possible, driver = check_run_possible(app_package, caps)
        if run_possible:
            start_time = time.time()
            log_fname = file.replace(file.split("/")[-1],
                                     "result/" + file.split("/")[-1].split(".")[0] + "_run_log.txt")
            parsed_test = craftdroid_parse(file)
            element_attributes_list, completed = get_element_attributes_list(parsed_test, app_package, driver,
                                                                             log_fname)
            print(str(time.time() - start_time) + " seconds\n")
            if completed:
                return element_attributes_list
            else:
                print("UNABLE TO RUN THE WHOLE TEST FOR THE FILE :" + str(file) + ".PLEASE CHECK THE ERROR LOG!")
                return None

    @staticmethod
    def load_events(config_id, target):
        fpath = Util.find_file_path(config_id, target)
        Util.run_source_test(fpath)

    @staticmethod
    def load_events_old(config_id, target):
        # target: 'generated', 'base_from', 'base_to'
        # e.g., a41a-a42a-b41 -> [Util.TEST_REPO, 'a4', 'b41', 'base', 'a41a.json']
        fpath = Util.find_file_path(config_id, target)
        act_list = []
        with open(fpath, 'r', encoding='utf-8') as f:
            acts = json.load(f)
        for act in acts:
            act_list.append(act)
        return act_list

    @staticmethod
    def delete_emails():
        dbank = Databank()
        try:
            print("Deleting all testing messages in the inbox")
            m = imaplib.IMAP4_SSL("imap.gmail.com")
            m.login(dbank.get_login_email(), dbank.get_gmail_password())
            m.select("inbox")
            result, data = m.uid('search', None, rf'X-GM-RAW "subject:\"{dbank.get_email_subject()}\""')
            if data:
                for uid in data[0].split():
                    m.uid('store', uid, '+X-GM-LABELS', '\\Trash')
            # empty trash
            m.select('[Gmail]/Trash')  # select all trash
            m.store("1:*", '+FLAGS', '\\Deleted')  # Flag all Trash as Deleted
            m.expunge()
            m.close()
            m.logout()
        except:
            print("Error when deleting testing messages.")

    # def cosine_sim(v1, v2):
    #     return dot(v1, v2) / (norm(v1) * norm(v2))
    #
    #
    # def get_layout_vec(vec):
    #     denominator = sum(vec)
    #     if denominator > 0:
    #         return [v/denominator for v in vec]
    #     else:
    #         return [v for v in vec]
