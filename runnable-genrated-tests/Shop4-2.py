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

el1 = driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="More options"]')
el1.click()

el2 = driver.find_element_by_id("android:id/title")
el2.click()
driver.implicitly_wait(5)
el3 = driver.find_element_by_id("android:id/title")
el3.click()

el5 = driver.find_element_by_id("android:id/button2")
el5.click()

el6 = driver.find_element_by_id("android:id/summary")
el6.click()

el7 = driver.find_element_by_id("android:id/button2")
el7.click()

el8 = driver.find_element_by_id("android:id/summary")
el8.click()

el9 = driver.find_element_by_id("android:id/title")
el9.click()

el9 = driver.find_element_by_id("android:id/button2")
el9.click()

el10 = driver.find_element_by_id("android:id/summary")
el10.click()

el11 = driver.find_element_by_id("android:id/action_bar_title")
el11.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text="Settings"]')))
