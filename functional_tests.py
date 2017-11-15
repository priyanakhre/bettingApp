from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

class testFrontEnd(unittest.TestCase):
    @classmethod
    def setUp(inst):
        driver = webdriver.Remote(
		   command_executor='http://selenium-chrome:4444/wd/hub',
		   desired_capabilities=DesiredCapabilities.CHROME)
        driver.get("http://web1:8000/home/")

    def signUp(self):
        assert "CrystalBall" in driver.title
        element = driver.find_element_by_xpath("/html/body/div/form[1]")
        assert "Register" in element.getAttribute("value")
        element.click()
        first_name = driver.find_element_by_id("id_first_name")
        last_name = driver.find_element_by_id("id_last_name")
        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")
        confirm_password = driver.find_element_by_id("id_confirm_password")

        first_name.send_keys('Priya')
        last_name.send_keys('Nakhre')
        username.send_keys('priya1997')
        password.send_keys('testpassword')
        confirm_password.send_keys('testpassword')

        submit = driver.find_element_by_xpath("/html/body/form[2]/input[7]")
        submit.click()

        #element.click()

    def tearDown(inst):
        driver.close()