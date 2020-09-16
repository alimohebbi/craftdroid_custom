from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import os
import sys

# local import
from Util import Util
from WidgetUtil import WidgetUtil

desired_caps = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': 'Android Emulator',
    'appPackage': "com.rubenroy.minimaltodo",
    'appActivity': "com.rubenroy.minimaltodo.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)

tid = os.path.basename(__file__).split('.')[0]
actions = []

el1 = driver.find_element_by_id("com.rubenroy.minimaltodo:id/addToDoItemFAB")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.rubenroy.minimaltodo:id/addToDoItemFAB')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el1.click()

el2 = driver.find_element_by_id("com.rubenroy.minimaltodo:id/userToDoEditText")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.rubenroy.minimaltodo:id/userToDoEditText')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', 'Sample Todo'],
                            driver.current_package, driver.current_activity, 'gui'))
el2.send_keys("Sample Todo")
driver.press_keycode(4)  # AndroidKeyCode for 'Back'
actions.append(Util.compose(None, tid, ['KEY_BACK'], driver.current_package, driver.current_activity, 'SYS_EVENT'))

el3 = driver.find_element_by_id("com.rubenroy.minimaltodo:id/makeToDoFloatingActionButton")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.rubenroy.minimaltodo:id/makeToDoFloatingActionButton')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el3.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text="Sample Todo"]')))
attrs = WidgetUtil.get_attrs(driver.page_source, 'text', 'Sample Todo', 'android.widget.TextView')
# type of name of attribute , value of attribute and type(class/tagname) of attribute. get_attrs uses these params to identify the widget
# the type of attribute param is optional, specially when you use resource_id attribute
actions.append(Util.compose(attrs, tid,
                            ['wait_until_element_presence', 10, 'xpath', '//android.widget.TextView[@text="Sample Todo"]'],
                            driver.current_package, driver.current_activity, 'oracle'))
# There are 5 type of actions gui, oracle, stepping, SYS_EVENT, EMPTY_EVENT which only first two are know for us and probably you don't need them.
# when you like to check a widget exist on current window you use oracle actions otherwise gui. oracles usually are used at the end of test
# but somtimes are used for check intermidiate steps when you have complex test for instance your test add two items and you want to check if
# first one have been created then you create next one.

Util.save_aug_events(actions, f'{tid}.json')
