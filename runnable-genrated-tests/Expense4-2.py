from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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

el1 = driver.find_element_by_id("luankevinferreira.expenses:id/fab")
el1.click()

el3 = driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
el3.click()
