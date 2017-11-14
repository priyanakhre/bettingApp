from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(
   command_executor='http://selenium-chrome:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.CHROME)
driver.get("http://web1:8000/home/")
assert "CrystalBall" in driver.title
driver.close()