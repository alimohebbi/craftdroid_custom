from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


desired_caps = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': 'Android Emulator',
    'appPackage': "br.com.activity",
    'appActivity': "br.com.vansact.MainApp",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)

el1 = driver.find_element_by_id("br.com.activity:id/action_add")
el1.click()

el2 = driver.find_element_by_id("android:id/button2")
el2.click()

el3 = driver.find_element_by_id("br.com.activity:id/action_add")
el3.click()

el4 = driver.find_element_by_id("android:id/button1")
el4.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text="No item was added"]')))
