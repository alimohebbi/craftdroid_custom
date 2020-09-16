import os

from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Util import Util
from WidgetUtil import WidgetUtil

desired_caps = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': 'Android Emulator',
    'appPackage': "me.writeily",
    'appActivity': "me.writeily.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)
tid = os.path.basename(__file__).split('.')[0]
actions = []

el1 = driver.find_element_by_id("me.writeily:id/fab_expand_menu_button")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'me.writeily:id/fab_expand_menu_button')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el1.click()

el2 = driver.find_element_by_id("me.writeily:id/create_note")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'me.writeily:id/create_note')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el2.click()

el3 = driver.find_element_by_id("me.writeily:id/edit_note_title")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'me.writeily:id/edit_note_title')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', 'note'],
                            driver.current_package, driver.current_activity, 'gui'))
el3.send_keys("note")

el4 = driver.find_element_by_id("me.writeily:id/note_content")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'me.writeily:id/note_content')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', 'something'],
                            driver.current_package, driver.current_activity, 'gui'))
el4.send_keys("something")


el4 = driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
attrs = WidgetUtil.get_attrs(driver.page_source, 'class', 'android.widget.ImageButton')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el4.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.LinearLayout[2]/android.widget.LinearLayout/android.widget.TextView[1]')))
attrs = WidgetUtil.get_attrs(driver.page_source, 'text', 'note', 'android.widget.TextView')
actions.append(Util.compose(attrs, tid,
                            ['wait_until_element_presence', 10, 'xpath', '//android.widget.TextView[1][@text="note"]'],
                            driver.current_package, driver.current_activity, 'oracle'))
Util.save_aug_events(actions, f'{tid}.json')
