from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


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

el1 = driver.find_element_by_id("com.moonpi.swiftnotes:id/action_search")
el1.click()

el2 = driver.find_element_by_id("com.moonpi.swiftnotes:id/search_src_text")
el2.send_keys("Go shopping")

driver.back()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.RelativeLayout/android.widget.TextView[1][@text="Press '+' to add new note"]')))
