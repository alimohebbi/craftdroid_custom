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

el1 = driver.find_element_by_id("com.blogspot.e_kanivets.moneytracker:id/btn_add_income")
el1.click()

el2 = driver.find_element_by_id("com.blogspot.e_kanivets.moneytracker:id/et_category")
el2.send_keys("45")

el3 = driver.find_element_by_id("com.blogspot.e_kanivets.moneytracker:id/et_price")
el3.send_keys("restaurant")
driver.back()

el4 = driver.find_element_by_id("com.blogspot.e_kanivets.moneytracker:id/tv_date")
el4.click()


el5 = driver.find_element_by_id("android:id/date_picker_header_year")
el5.click()

el6 = driver.find_element_by_id("android:id/button1")
el6.click()

el7 = driver.find_element_by_id("com.blogspot.e_kanivets.moneytracker:id/tv_date")
el7.click()

el8 = driver.find_element_by_id("android:id/button1")
el8.click()

el9 = driver.find_element_by_id("com.blogspot.e_kanivets.moneytracker:id/tv_date")
el9.click()


el10 = driver.find_element_by_id("android:id/date_picker_header_year")
el10.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.Button[@text=\"2020\"]')))
