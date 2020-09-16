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
    'appPackage': "cz.martykan.forecastie",
    'appActivity': "cz.martykan.forecastie.activities.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)
tid = os.path.basename(__file__).split('.')[0]
actions = []

el1 = driver.find_element_by_id("cz.martykan.forecastie:id/action_search")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'cz.martykan.forecastie:id/action_search')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el1.click()

el2 = driver.find_element_by_xpath("//android.widget.FrameLayout/android.widget.EditText")
attrs = WidgetUtil.get_attrs(driver.page_source, 'class', 'android.widget.EditText')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', 'atlanta'],
                            driver.current_package, driver.current_activity, 'gui'))
el2.send_keys("atlanta")

el3 = driver.find_element_by_id("android:id/button1")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'android:id/button1')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el3.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.view.ViewGroup/android.widget.TextView')))
attrs = WidgetUtil.get_attrs(driver.page_source, 'text', 'Atlanta, US', 'android.widget.TextView')
actions.append(Util.compose(attrs, tid,
                            ['wait_until_element_presence', 10, 'xpath', '//android.view.ViewGroup/android.widget.TextView[@text="Atlanta, US"]'],
                            driver.current_package, driver.current_activity, 'oracle'))
Util.save_aug_events(actions, f'{tid}.json')
