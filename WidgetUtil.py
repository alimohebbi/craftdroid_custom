import re
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup

# local import
from matching_client.match_object import MatchObject
from matching_client.object_sender import send_object
from widget_process.file_name_adder import SourceFileNameAdder, TargetFileNameAdder
from widget_process.widget_classifier import *


class WidgetUtil:
    # NAF means "Not Accessibility Friendly", e.g., a back button without any textual info like content-desc
    FEATURE_KEYS = ['class', 'resource-id', 'text', 'content-desc', 'clickable', 'password', 'naf']
    ALL_FEATURE_KEYS = ["bounds", "checkable", "checked", "enabled", "height",
                        "index", "long-clickable", "package", "scrollable", "selected",
                        "width", "x1", "x2", "y1", "y2"]
    ALL_FEATURE_KEYS.extend(FEATURE_KEYS)
    WIDGET_CLASSES = ['android.widget.EditText', 'android.widget.MultiAutoCompleteTextView', 'android.widget.TextView',
                      'android.widget.Button', 'android.widget.ImageButton', 'android.view.View',
                      "android.widget.DialogTitle", "android.widget.ImageView", "android.widget.IconTextView",
                      "com.google.android.material.textfield.TextInputLayout",
                      'android.support.design.widget.TextInputLayout']
    state_to_widgets = {}  # for a gui state, there are "all_widgets": a list of all widgets, and

    # "most_similar_widgets": a dict for a source widget and the list of its most similar widgets and scores

    @staticmethod
    def get_gui_signature(xml_dom, pkg_name, act_name):
        """Get the signature for a GUI state by the package/activity name and the xml hierarchy
        Breadth first traversal for the non-leaf/leaf nodes and their cumulative index sequences
        """
        xml_dom = re.sub(r'&#\d+;', "", xml_dom)  # remove emoji
        root = ET.fromstring(xml_dom)
        queue = [(root, '0')]
        layouts = []
        executable_leaves = []
        while queue:
            node, idx = queue.pop()
            if len(list(node)):  # the node has child(ren)
                layouts.append(idx)
                for i, child in enumerate(node):
                    queue.insert(0, (child, idx + '-' + str(i)))
            else:  # a leaf node
                executable_leaves.append(idx)
        # print(layouts)
        # print(executable_leaves)
        sign = [pkg_name, act_name, '+'.join(layouts), '+'.join(executable_leaves)]
        return '!'.join(sign)

    @classmethod
    def get_widget_signature(cls, w):
        """Get the signature for a GUI widget by its attributes"""
        sign = []
        for k in cls.FEATURE_KEYS + ['package', 'activity']:
            if k in w:
                sign.append(w[k])
            else:
                sign.append('')
        return '!'.join(sign)

    @classmethod
    def get_most_similar_widget_from_cache(cls, gui_signature, widget_signature):
        """Return the most similar widget and the score to the source widget in a gui state in cache"""
        if gui_signature not in cls.state_to_widgets:
            return None, -1
        if 'most_similar_widgets' in cls.state_to_widgets[gui_signature]:
            if widget_signature in cls.state_to_widgets[gui_signature]['most_similar_widgets']:
                # print('Cache HIT from SIMILAR')
                return cls.state_to_widgets[gui_signature]['most_similar_widgets'][widget_signature][0]
        return None, -1

    @classmethod
    def get_all_widgets_from_cache(cls, gui_signature):
        """Return all widgets in a gui state in cache"""
        if gui_signature in cls.state_to_widgets and 'all_widgets' in cls.state_to_widgets[gui_signature]:
            # print('Cache HIT from ALL')
            return cls.state_to_widgets[gui_signature]['all_widgets']
        else:
            return None

    @staticmethod
    def get_parent_text(soup_ele):
        # consider immediate parent node's text if exists
        parent_text = ''
        parent = soup_ele.find_parent()
        if parent and 'text' in parent.attrs and parent['text']:
            parent_text += parent['text']
        # consider grandparent if it's TextInputLayout (for ? related apps)
        parent = parent.find_parent()
        if parent and 'text' in parent.attrs and parent['text'] and parent['class'][0] == 'TextInputLayout':
            parent_text += parent['text']
        return parent_text

    @staticmethod
    def get_sibling_text(soup_ele):
        # (for Tip related apps)
        # consider immediate previous sibling text if exists and the parent is LinearLayout
        sibling_text = ''
        parent = soup_ele.find_parent()
        if parent and parent['class'][0] in ['android.widget.LinearLayout', 'android.widget.RelativeLayout']:
            prev_sib = soup_ele.previous_sibling
            if prev_sib and 'text' in prev_sib.attrs and prev_sib['text']:
                sibling_text = prev_sib['text']
        return sibling_text

    @classmethod
    def get_attrs(cls, dom, attr_name, attr_value, tag_name=''):
        soup = BeautifulSoup(dom, 'lxml')
        if attr_name == 'text-contain':
            cond = {'text': lambda x: x and attr_value in x}
        else:
            cond = {attr_name: attr_value}
        if tag_name:
            cond['class'] = tag_name
        ele = soup.find(attrs=cond)
        # for k, v in ele.attrs.items():
        #    print(k, v)
        d = {}
        for key in cls.FEATURE_KEYS:
            d[key] = ele.attrs[key] if key in ele.attrs else ""
            if key == 'class':
                d[key] = d[key][0]  # for now, only consider the first class
            elif key == 'clickable' and key in ele.attrs and ele.attrs[key] == 'false':
                d[key] = WidgetUtil.propagate_clickable(ele)
        d['parent_text'] = WidgetUtil.get_parent_text(ele)
        d['sibling_text'] = WidgetUtil.get_sibling_text(ele)
        return d

    @classmethod
    def get_empty_attrs(cls):
        d = {}
        for key in cls.FEATURE_KEYS:
            d[key] = ""
        d['parent_text'] = ""
        d['sibling_text'] = ""
        return d

    @classmethod
    def find_all_widgets(cls, dom, pkg, act, target_pkg, update_cache=True):
        if 'com.android.launcher' in pkg:  # the app is closed
            return []

        if pkg != target_pkg:  # exclude all widgets not belonging to the app's package
            return []

        if act.startswith('com.facebook'):  # the app reaches facebook login, out of the app's scope
            return []

        gui_signature = WidgetUtil.get_gui_signature(dom, pkg, act)
        if not update_cache:
            widgets = WidgetUtil.get_all_widgets_from_cache(gui_signature)
            if widgets:
                return widgets

        soup = BeautifulSoup(dom, 'lxml')
        widgets = []
        for w_class in cls.WIDGET_CLASSES:
            elements = soup.find_all('', w_class)
            for e in elements:
                d = cls.get_widget_from_soup_element(e)
                if d:
                    if 'yelp' in gui_signature and 'text' in d and d['text'] == 'Sign up with Google':
                        d['text'] = 'SIGN UP WITH GOOGLE'  # Specific for Yelp
                    d['package'], d['activity'] = pkg, act
                    widgets.append(d)

        if widgets or update_cache:
            cls.state_to_widgets[gui_signature] = {'all_widgets': widgets, 'most_similar_widgets': {}}
        return widgets

    @classmethod
    def get_widget_from_soup_element(cls, e):
        if not e:
            return None
        d = {}
        if 'enabled' in e.attrs and e['enabled'] == 'true':
            for key in cls.ALL_FEATURE_KEYS:
                d[key] = e.attrs[key] if key in e.attrs else ''
                if key == 'class':
                    d[key] = d[key][0]  # for now, only consider the first class
                elif key == 'clickable' and key in e.attrs and e.attrs[key] == 'false':
                    d[key] = WidgetUtil.propagate_clickable(e)
                elif key == 'resource-id':
                    rid = d[key].split('/')[-1]
                    prefix = ''.join(d[key].split('/')[:-1])
                    d[key] = rid
                    d['id-prefix'] = prefix + '/' if prefix else ''
            d['parent_text'] = WidgetUtil.get_parent_text(e)
            d['sibling_text'] = WidgetUtil.get_sibling_text(e)
            return d
        else:
            return None

    @classmethod
    def propagate_clickable(cls, soup_element):
        # clickable propagation from immediate parent
        parent = soup_element.find_parent()
        if 'clickable' in parent.attrs and parent['clickable'] == 'true':
            return 'true'
        for i in range(2):  # a22-a23-b22 (mutated)
            parent = parent.find_parent()
            if parent and 'class' in parent.attrs and parent['class'][0] in ['android.widget.ListView']:
                if 'clickable' in parent.attrs and parent['clickable'] == 'true':
                    return 'true'
        return 'false'

    @staticmethod
    def advanced_select(sim_pairs, src_event):
        # If there are 1+ widgets with the same sim score,
        # pick the one with the most words in common with the target text
        if len(sim_pairs) == 1:
            return sim_pairs[0]
        ans = sim_pairs[0]
        src_text = src_event['text']
        if src_text:
            overlap_score = -1
            for p in sim_pairs:
                w_text = p[0]['text']
                if w_text:
                    s1 = set(src_text.lower().strip().split())
                    s2 = set(w_text.lower().strip().split())
                    intersection = len(s1.intersection(s2))
                    if intersection > overlap_score:
                        overlap_score = intersection
                        ans = p
        return ans

    @staticmethod
    def weighted_sim(new_widget, old_widget, use_stopwords=True, cross_check=False):
        match_object = MatchObject(old_widget, [new_widget], None)
        scored_indexes = send_object(match_object.get_json())
        return scored_indexes['0']

    @classmethod
    def is_equal(cls, w1, w2, ignore_activity=False):
        if not w1 or not w2:
            return False
        keys_for_equality = set(cls.FEATURE_KEYS)
        keys_for_equality.remove('naf')
        if not ignore_activity:
            keys_for_equality = keys_for_equality.union({'package', 'activity'})
        for k in keys_for_equality:
            if (k in w1 and k not in w2) or (k not in w1 and k in w2):
                return False
            if k in w1 and k in w2:
                v1, v2 = w1[k], w2[k]
                if k == 'resource-id' and 'id-prefix' in w1:
                    v1 = w1['id-prefix'] + w1[k]
                if k == 'resource-id' and 'id-prefix' in w2:
                    v2 = w2['id-prefix'] + w2[k]
                if v1 != v2:
                    return False
        return True

    '''
    @staticmethod
    def get_state_feature(act_name, dom, use_stopwords=True):
        """Express a GUI state as:
        1. tokenized words of current Activity;
        2. # of clickable elements / android.widget.EditText widget / long-clickable elements
        """
        soup = BeautifulSoup(dom, 'lxml')
        feature_vec = [
            len(soup.find_all(attrs={'clickable': 'true', 'enabled': 'true'})),
            len(soup.find_all(attrs={'class': 'android.widget.EditText', 'enabled': 'true'})),
            len(soup.find_all(attrs={'long-clickable': 'true', 'enabled': 'true'}))
        ]
        #denominator = sum(feature_vec)
        #if denominator > 0:
        #    feature_vec = [n/denominator for n in feature_vec]
        return {'act_name': str_util.tokenize('Activity', act_name, use_stopwords=use_stopwords), 'feature': feature_vec}
    '''

    @classmethod
    def locate_widget(cls, dom, criteria):
        # e.g., criteria =
        #   {'class': 'TextView', 'text': 'Okay', 'resource-id': 'tv_task', 'content-desc': ""} or
        #   {'class': 'android.widget.Button', 'resource-id': 'org.secuso.privacyfriendlytodolist:id/btn_skip'}
        regex_cria = {}
        for k, v in criteria.items():
            if v:
                v = v.replace('+', r'\+')  # for error when match special char '+'
                v = v.replace('?', r'\?')  # for error when match special char '?'
                # regex_cria[k] = re.compile(f'{v}$')
                regex_cria[k] = re.compile(f'{v}')
        if not regex_cria:
            return None
        soup = BeautifulSoup(dom, 'lxml')
        return cls.get_widget_from_soup_element(soup.find('', regex_cria))

    @classmethod
    def most_similar(cls, src_event, widgets, use_stopwords=True, expand_btn_to_text=False, cross_check=False):
        w_list = list(widgets)
        dynamic_widgets = get_dynamic_widgets(w_list)
        static_widgets = get_static_widgets(w_list)
        actionable_widget, label_widgets = separate_actionable_label(src_event, dynamic_widgets)
        similars = WidgetUtil.score_widgets(src_event, actionable_widget, label_widgets)
        add_static_flag(actionable_widget, label_widgets)
        similars.extend(WidgetUtil.score_widgets(src_event, static_widgets, None))
        similars.sort(key=lambda x: x[1], reverse=True)
        return similars

    @staticmethod
    def score_widgets(src_event, candidates, target_labels):
        TargetFileNameAdder.add_file_name_to_widgets(target_labels)
        TargetFileNameAdder.add_file_name_to_widgets(candidates)
        SourceFileNameAdder.add_file_name_to_widgets([src_event])
        match_object = MatchObject(src_event, candidates, target_labels)
        scored_indexes = send_object(match_object.get_json())
        scored_widgets = []
        for k in scored_indexes:
            scored_widgets.append((candidates[int(k)], scored_indexes[k]))
        return scored_widgets

    @classmethod
    def get_nearest_button(cls, dom, w):
        # for now just return the first btn on the screen; todo: find the nearest button
        soup = BeautifulSoup(dom, 'lxml')
        for btn_class in ['android.widget.ImageButton', 'android.widget.Button', 'android.widget.EditText']:
            all_btns = soup.find_all('', btn_class)
            if all_btns and len(all_btns) > 0:
                return cls.get_widget_from_soup_element(all_btns[0])
        return None
