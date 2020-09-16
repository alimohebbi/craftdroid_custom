from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


desired_caps = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': 'Android Emulator',
    'appPackage': "com.blogspot.e_kanivets.moneytracker",
    'appActivity': "com.blogspot.e_kanivets.moneytracker.activity.record.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)

el1 = driver.find_element_by_id("com.blogspot.e_kanivets.moneytracker:id/tv_total_income")
el1.click()


el2 = driver.find_element_by_id("com.blogspot.e_kanivets.moneytracker:id/tv_total_income")
el2.click()

el3 = driver.find_element_by_id("android:id/text1")
el3.click()

el4 = driver.find_element_by_id("android:id/text1")
el4.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text="+ 0 NON"]')))
