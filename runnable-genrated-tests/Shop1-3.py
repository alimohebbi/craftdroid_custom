from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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

el1 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/btn_skip")
el1.click()

el2 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/fab_new_list")
el2.click()

el3 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/list_name")
el3.send_keys("Grocery")

el4 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/list_notes")
el4.send_keys("Weekly grocery shopping")

el5 = driver.find_element_by_id("android:id/button2")
el5.click()

el6 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/fab_new_list")
el6.click()
