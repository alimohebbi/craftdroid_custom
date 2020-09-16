from appium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By


desired_caps = {
    'platformName': 'Android',
    'platformVersion': '6.0',
    'deviceName': 'Android Emulator',
    'appPackage': "com.benoitletondor.easybudgetapp",
    'appActivity': "com.benoitletondor.easybudgetapp.view.WelcomeActivity",
    'autoGrantPermissions': True,
    'noReset': False
}
driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
driver.implicitly_wait(5)

el1 = driver.find_element_by_id("com.benoitletondor.easybudgetapp:id/onboarding_screen1_next_button")
el1.click()

el2 = driver.find_element_by_id("com.benoitletondor.easybudgetapp:id/currency_cell_title_tv")
el2.click()

el3 = driver.find_element_by_id("com.benoitletondor.easybudgetapp:id/onboarding_screen2_next_button")
el3.click()

el4 = driver.find_element_by_id("com.benoitletondor.easybudgetapp:id/onboarding_screen3_initial_amount_et")
el4.send_keys("500")

el5 = driver.find_element_by_id("com.benoitletondor.easybudgetapp:id/onboarding_screen3_next_button")
el5.click()


WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.XPATH, '//android.widget.TextView[@text="(That was easy, huh?)"]')))
