import os
from time import sleep

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
    'appPackage': "com.kvannli.simonkvannli.dailybudget",
    'appActivity': "com.kvannli.simonkvannli.dailybudget.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)
tid = os.path.basename(__file__).split('.')[0]
actions = []



el1 = driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Open navigation drawer"]')
attrs = WidgetUtil.get_attrs(driver.page_source, 'naf', True, 'android.widget.ImageButton')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el1.click()
sleep(1)

el2 = driver.find_element_by_xpath('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout[2]/android.support.v4.widget.DrawerLayout/android.widget.ListView/android.widget.TextView[3]')
attrs = WidgetUtil.get_attrs(driver.page_source, 'class', 'android.widget.TextView')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el2.click()

el3 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/editText")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.kvannli.simonkvannli.dailybudget:id/editText')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', 'uber'],
                            driver.current_package, driver.current_activity, 'gui'))
el3.send_keys("uber")

el4 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/button2")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.kvannli.simonkvannli.dailybudget:id/button2')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el4.click()

el5 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/editText2")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.kvannli.simonkvannli.dailybudget:id/editText2')
actions.append(Util.compose(attrs, tid, ['send_keys_and_hide_keyboard', '500'],
                            driver.current_package, driver.current_activity, 'gui'))
el5.send_keys("500")

el6 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/button2")
attrs = WidgetUtil.get_attrs(driver.page_source, 'resource-id', 'com.kvannli.simonkvannli.dailybudget:id/button2')
actions.append(Util.compose(attrs, tid, ['click'], driver.current_package, driver.current_activity, 'gui'))
el6.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TableRow/android.widget.TableLayout/android.widget.TableRow[1]/android.widget.TextView[@text="uber"]')))
attrs = WidgetUtil.get_attrs(driver.page_source, 'text', 'uber', 'android.widget.TextView')
actions.append(Util.compose(attrs, tid,
                            ['wait_until_element_presence', 10, 'xpath', '//android.widget.TableRow/android.widget.TableLayout/android.widget.TableRow[1]/android.widget.TextView[@text="uber"]'],
                            driver.current_package, driver.current_activity, 'oracle'))
Util.save_aug_events(actions, f'{tid}.json')
