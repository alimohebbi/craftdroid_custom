from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


desired_caps = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': 'Android Emulator',
    'appPackage': "privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist",
    'appActivity': "privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist.ui.tutorial.TutorialActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)

el1 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/btn_skip")
el1.click()

el2 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/fab_new_list")
el2.click()

el3 = driver.find_element_by_id("android:id/button1")
el3.click()

el4 = driver.find_element_by_xpath('//android.widget.ImageButton[@content-desc="Navigate up"]')
el4.click()

el5 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/fab_new_list")
el5.click()

el6 = driver.find_element_by_id("android:id/button2")
el6.click()

el7 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/fab_new_list")
el7.click()


el8 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/list_name")
el8.send_keys("list1")


el9 = driver.find_element_by_id("android:id/button1")
el9.click()

el10 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/fab_new_product")
el10.click()

el11 = driver.find_element_by_id("android:id/button1")
el11.click()

el12 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/expand_button")
el12.click()

el13 = driver.find_element_by_id("android:id/button1")
el13.click()

el14 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/quantity")
el14.send_keys("item1")

el15 = driver.find_element_by_id("privacyfriendlyshoppinglist.secuso.org.privacyfriendlyshoppinglist:id/expand_button")
el15.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text="New Product"]')))
