import os
import unittest
from appium import webdriver

desired_caps = {}
desired_caps['platformName'] = 'Android'
desired_caps['platformVersion'] = '6.0'
desired_caps['deviceName'] = 'emulator2'
desired_caps['appActivity'] = 'com.kvannli.simonkvannli.dailybudget.MainActivity'
desired_caps['appPackage'] = 'com.kvannli.simonkvannli.dailybudget'
desired_caps['autoGrantPermissions'] = True
desired_caps['noReset'] = False

driver = webdriver.Remote('http://localhost:4723/wd/hub', desired_caps)
if driver.is_keyboard_shown():
    driver.hide_keyboard()
    print('hi')


