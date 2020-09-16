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
    'appPackage': "privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist",
    'appActivity': "privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist.ui.tutorial.TutorialActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)
tid = os.path.basename(__file__).split('.')[0]
actions = []

el1 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/btn_skip")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/btn_skip')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el1.click()

el2 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/fab_new_list")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/fab_new_list')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el2.click()

el3 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/list_name")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/list_name')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', 'Grocery'],
                            driver.current_package, driver.current_activity, 'gui'))
el3.send_keys("Grocery")

el4 = driver.find_element_by_id("android:id/button1")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'android:id/button1')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el4.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text="Grocery"]')))
attrs = WidgetUtil.get_attrs(driver.page_source, 'text', 'Grocery', 'android.widget.TextView')
actions.append(Util.compose(attrs, tid,
                            ['wait_until_element_presence', 10, 'xpath', '//android.widget.TextView[@text="Grocery"]'],
                            driver.current_package, driver.current_activity, 'oracle'))
Util.save_aug_events(actions, f'{tid}.json')
