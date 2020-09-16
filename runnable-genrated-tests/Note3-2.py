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

el2 = driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Collapse"]')
el2.click()

el3 = driver.find_element_by_id("com.moonpi.swiftnotes:id/newNote")
el3.click()

el4 = driver.find_element_by_id("com.moonpi.swiftnotes:id/titleEdit")
el4.send_keys("note")

el5 = driver.find_element_by_id("com.moonpi.swiftnotes:id/bodyEdit")
el5.send_keys("something")

el6 = driver.find_element_by_id("com.moonpi.swiftnotes:id/action_note_colour")
el6.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[1][@text="Change note color"]')))
