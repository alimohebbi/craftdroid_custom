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
    'appPackage': "com.moonpi.swiftnotes",
    'appActivity': "com.moonpi.swiftnotes.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)
tid = os.path.basename(__file__).split('.')[0]
actions = []

el1 = driver.find_element_by_id("com.moonpi.swiftnotes:id/newNote")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.moonpi.swiftnotes:id/newNote')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el1.click()

el2 = driver.find_element_by_id("com.moonpi.swiftnotes:id/titleEdit")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.moonpi.swiftnotes:id/titleEdit')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', 'Title1'],
                            driver.current_package, driver.current_activity, 'gui'))
el2.send_keys("Title1")


el3 = driver.find_element_by_id("com.moonpi.swiftnotes:id/scrollView")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.moonpi.swiftnotes:id/scrollView')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', 'Note1'],
                            driver.current_package, driver.current_activity, 'gui'))
el3.send_keys("Note1")

el4 = driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.RelativeLayout/android.view.ViewGroup/android.widget.ImageButton")
attrs = WidgetUtil.get_attrs(driver.page_source, 'naf', True, 'android.widget.ImageButton')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el4.click()

el5 = driver.find_element_by_id("android:id/button1")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'android:id/button1')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el5.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.RelativeLayout/android.widget.TextView[1][@text="Title1"]')))
attrs = WidgetUtil.get_attrs(driver.page_source, 'text', 'Title1', 'android.widget.TextView')
actions.append(Util.compose(attrs, tid,
                            ['wait_until_element_presence', 10, 'xpath', '//android.widget.RelativeLayout/android.widget.TextView[1][@text="Title1"]'],
                            driver.current_package, driver.current_activity, 'oracle'))
Util.save_aug_events(actions, f'{tid}.json')
