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


el1 = driver.find_element_by_id("android:id/button1")
el1.click()


el1 = driver.find_element_by_id("br.com.activity:id/search")
el1.click()


el1 = driver.find_element_by_id("android:id/search_src_text")
el1.send_keys("Grocery")


el1 = driver.find_element_by_id("br.com.activity:id/edDescription")
el1.send_keys("Weekly grocery shopping")


el1 = driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="More options"]')
el1.click()


el1 = driver.find_element_by_id("android:id/title")
el1.click()
