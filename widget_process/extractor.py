from bs4 import BeautifulSoup
import copy
from WidgetUtil import WidgetUtil
from widget_process.widget_classifier import separate_actionable_label


def find_all_widgets(dom):
    soup = BeautifulSoup(dom, 'lxml')
    widgets = []
    for w_class in WidgetUtil.WIDGET_CLASSES:
        elements = soup.find_all('', w_class)
        for e in elements:
            d = WidgetUtil.get_widget_from_soup_element(e)
            if d:
                widgets.append(d)
    return widgets


def get_widget_from_dom(attr, dom):
    soup = BeautifulSoup(dom, 'lxml')
    e = soup.find(attrs=attr)
    return WidgetUtil.get_widget_from_soup_element(e)


def get_src_labels(src_event):
    widgets = find_all_widgets(src_event['page'])
    _, labels = separate_actionable_label(src_event, widgets)
    return labels


def refine_event(src_event):
    src_copy = copy.deepcopy(src_event)
    for i in src_event.keys():
        if i not in WidgetUtil.FEATURE_KEYS:
            src_copy.pop(i)
    event = get_widget_from_dom(src_copy, src_event['page'])
    event['activity'] = src_event['activity']
    event['event_type'] = src_event['event_type']
    event['action'] = src_event['action']
    return event
