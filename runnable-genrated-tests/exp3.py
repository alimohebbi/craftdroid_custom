from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


desired_caps = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': 'Android Emulator',
    'appPackage': "me.writeily",
    'appActivity': "me.writeily.MainActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)

el1 = driver.find_element_by_id("me.writeily:id/fab_expand_menu_button")
el1.click()

el2 = driver.find_element_by_id("me.writeily:id/create_note")
el2.click()

el3 = driver.find_element_by_id("me.writeily:id/edit_note_title")
el3.send_keys("Title1")

el4 = driver.find_element_by_id("me.writeily:id/keyboard_shortcut")
el4.click()

