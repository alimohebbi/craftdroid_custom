from bs4 import BeautifulSoup

from WidgetUtil import WidgetUtil


def find_all_widgets(dom, pkg, act):
    if act.startswith('com.facebook'):  # the app reaches facebook login, out of the app's scope
        return []

    soup = BeautifulSoup(dom, 'lxml')
    widgets = []
    for w_class in WidgetUtil.WIDGET_CLASSES:
        elements = soup.find_all('', w_class)
        for e in elements:
            d = WidgetUtil.get_widget_from_soup_element(e)
            if d:
                d['package'], d['activity'] = pkg, act
                widgets.append(d)
    return widgets


def get_widget_from_dom(attr, dom):
    soup = BeautifulSoup(dom, 'lxml')
    e = soup.find_next(attrs=attr)
    return WidgetUtil.get_widget_from_soup_element(e)
