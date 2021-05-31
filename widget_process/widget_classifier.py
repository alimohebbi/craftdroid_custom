WIDGET_LABEL_CLASS = {"TextView", "DialogTitle", "ImageView", "IconTextView", "TextInputLayout"}


def separate_actionable_label(src_event, dynamic_widgets):
    actionables = []
    labels = []
    for w in dynamic_widgets:
        if has_static_class(w) and not is_clickable(w):
            if has_text_or_content(w):
                labels.append(w)
        else:
            actionables.append(w)

    if 'wait_until_element' in src_event['action'][0]:
        return dynamic_widgets, labels
    else:
        return actionables, labels


def get_dynamic_widgets(widgets):
    return [i for i in widgets if len(i) > 13 and 'static' not in i]


def add_static_flag(actionable_widget, label_widgets):
    for i in actionable_widget:
        i['static'] = True
    for i in label_widgets:
        i['static'] = True


def get_static_widgets(widgets):
    return [i for i in widgets if len(i) < 13 or 'static' in i]


def has_text_or_content(w):
    if w['text'] and w['text'] != '':
        return True
    if w['content-desc'] and w['content-desc'] != '':
        return True

    return False


def has_static_class(w):
    for i in WIDGET_LABEL_CLASS:
        if w['class'].endswith(i):
            return True
    return False


def is_clickable(w):
    if w['clickable'] and w['clickable'] == 'true':
        return True
    if w['long-clickable'] and w['long-clickable'] == 'true':
        return True
    if w['checkable'] and w['checkable'] == 'true':
        return True
    return False
