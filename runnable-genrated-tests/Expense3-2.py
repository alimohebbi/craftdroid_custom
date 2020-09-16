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

el2 = driver.find_element_by_xpath('//android.widget.TextView[@text="Expenses"]')
el2.click()

el3 = driver.find_element_by_id("luankevinferreira.expenses:id/expense_description")
el3.send_keys("uber")

el4 = driver.find_element_by_id("android:id/text1")
el4.click()

el5 = driver.find_element_by_id("android:id/text1")
el5.click()

el6 = driver.find_element_by_id("luankevinferreira.expenses:id/expense_value")
el6.send_keys("500")

el7 = driver.find_element_by_id("android:id/text1")
el7.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text="Clothes"]')))
