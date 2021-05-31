import unittest

from widget_process.file_name_finder import SourceFileNameAdder, FileNameFinder, TargetFileNameAdder


class TestFileNameFinder(unittest.TestCase):

    def test_add_file_name_source(self):
        file_name_finder = FileNameFinder.get_instance()
        file_name_finder.set_apps('a22-a23-b2')
        widget = {'activity': 'PanelInput', 'resource-id': 'reminder_del'}
        SourceFileNameAdder.add_file_name_to_widgets([widget])
        self.assertEqual(widget['file_name'], 'ic_close')

    def test_add_file_name_target(self):
        file_name_finder = FileNameFinder.get_instance()
        file_name_finder.set_apps('a23-a22-b2')
        widget = {'activity': 'PanelInput', 'resource-id': 'reminder_del'}
        TargetFileNameAdder.add_file_name_to_widgets([widget])
        self.assertEqual(widget['file_name'], 'ic_close')

    def test_add_file_name_id_not_exist(self):
        file_name_finder = FileNameFinder.get_instance()
        file_name_finder.set_apps('a23-a22-b2')
        widget = {'activity': 'PanelInput', 'resource-id': 'reminderrr_del'}
        TargetFileNameAdder.add_file_name_to_widgets([widget])
        self.assertEqual(widget['file_name'], '')

    def test_add_file_name_activity_not_exist(self):
        file_name_finder = FileNameFinder.get_instance()
        file_name_finder.set_apps('a23-a22-b2')
        widget = {'activity': 'zzz', 'resource-id': 'reminder_del'}
        TargetFileNameAdder.add_file_name_to_widgets([widget])
        self.assertEqual(widget['file_name'], '')

    def test_add_file_name_activity_not_match(self):
        file_name_finder = FileNameFinder.get_instance()
        file_name_finder.set_apps('a23-a22-b2')
        widget = {'activity': 'input_panel', 'resource-id': 'thumb_up'}
        TargetFileNameAdder.add_file_name_to_widgets([widget])
        self.assertEqual(widget['file_name'], '')

    def test_add_file_name_multiple(self):
        file_name_finder = FileNameFinder.get_instance()
        file_name_finder.set_apps('a23-a22-b2')
        widget = {'activity': 'PanelInput', 'resource-id': 'reminder_del'}
        widget2 = {'activity': 'thingListItem', 'resource-id': 'thumb_up'}
        TargetFileNameAdder.add_file_name_to_widgets([widget, widget2])
        self.assertEqual(widget['file_name'], 'ic_close')
        self.assertEqual(widget2['file_name'], 'ic_thumb_up_white')
