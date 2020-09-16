from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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

el1 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/imageButton2")
el1.click()

el2 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/doneButton")
el2.click()

el3 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/input_amount")
el3.send_keys(1500)

el4 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/doneButton")
el4.click()

el5 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/imageButton2")
el5.click()

el6 = driver.find_element_by_id("com.kvannli.simonkvannli.dailybudget:id/doneButton")
el6.click()
