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

el1 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/fab")
el1.click()

el2 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/addShoppingListButton")
el2.click()

el3 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/addShoppingListButton")
el3.click()

el4 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/shoppingListNameEditText")
el4.send_keys("Grocery")

el5 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/addShoppingListButton")
el5.click()

el6 = driver.find_element_by_id("pl.com.andrzejgrzyb.shoppinglist:id/shoppingListNameTextView")
el6.click()

WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text="Grocery"]')))
