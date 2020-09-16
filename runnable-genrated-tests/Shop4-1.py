from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


desired_caps = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': 'Android Emulator',
    'appPackage': "pl.com.andrzejgrzyb.shoppinglist",
    'appActivity': "pl.com.andrzejgrzyb.shoppinglist.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)

el1 = driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Open navigation drawer"]')
el1.click()

el2 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/fab")
el2.click()

el3 = driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Open navigation drawer"]')
el3.click()

el4 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/fab")
el4.click()

el5 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/fab")
el5.click()

el6 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/addShoppingListButton")
el6.click()

el7 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/shoppingListNameEditText")
el7.send_keys("item1")

el8 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/addShoppingListButton")
el8.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text=\"item1\"]')))
