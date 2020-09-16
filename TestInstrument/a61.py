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
    'appPackage': "luankevinferreira.expenses",
    'appActivity': "luankevinferreira.expenses.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)
tid = os.path.basename(__file__).split('.')[0]
actions = []

el1 = driver.find_element_by_id("luankevinferreira.expenses:id/fab")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'luankevinferreira.expenses:id/fab')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el1.click()

el2 = driver.find_element_by_id("luankevinferreira.expenses:id/expense_value")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'luankevinferreira.expenses:id/expense_value')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', '45'],
                            driver.current_package, driver.current_activity, 'gui'))
el2.send_keys("45")

el3 = driver.find_element_by_id("luankevinferreira.expenses:id/expense_description")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'luankevinferreira.expenses:id/expense_description')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', 'restaurant'],
                            driver.current_package, driver.current_activity, 'gui'))
el3.send_keys("restaurant")

el4 = driver.find_element_by_id("luankevinferreira.expenses:id/date_picker")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'luankevinferreira.expenses:id/date_picker')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el4.click()

el5 = driver.find_element_by_id("android:id/button1")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'android:id/button1')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el5.click()

el6 = driver.find_element_by_id("luankevinferreira.expenses:id/save_expense")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'luankevinferreira.expenses:id/save_expense')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el6.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.Button[@text="$45.00"]')))
attrs = WidgetUtil.get_attrs(driver.page_source, 'text', '$45.00', 'android.widget.Button')
actions.append(Util.compose(attrs, tid,
                            ['wait_until_element_presence', 10, 'xpath', '//android.widget.Button[@text="$45.00"]'],
                            driver.current_package, driver.current_activity, 'oracle'))
Util.save_aug_events(actions, f'{tid}.json')
