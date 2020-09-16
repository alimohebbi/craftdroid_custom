from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


desired_caps = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': 'Android Emulator',
    'appPackage': "org.asdtm.goodweather",
    'appActivity': "org.asdtm.goodweather.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)


el1 = driver.find_element_by_id("org.asdtm.goodweather:id/main_menu_search_city")
el1.click()

el2 = driver.find_element_by_id("org.asdtm.goodweather:id/city_name")
el2.click()


el3 = driver.find_element_by_id("org.asdtm.goodweather:id/main_temperature")
el3.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.view.ViewGroup/android.widget.TextView[@text="London, UK"]')))

