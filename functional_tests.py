from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.common.exceptions import NoSuchElementException

class testFrontEnd(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Remote(
		   command_executor='http://selenium-chrome:4444/wd/hub',
		   desired_capabilities=DesiredCapabilities.CHROME
        )

    def test_signUp(self):
        driver = self.driver
        driver.get("http://web1:8000/home/")
        assert "CrystalBall" in driver.title
        element = driver.find_element_by_id("register")
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

        submit = driver.find_element_by_id("regsubmit")
        submit.click()
        exists = False
        try:
            driver.find_element_by_id("id_username")
        except NoSuchElementException:
            exists = False
            assert exists
        exists = True
        assert exists
        

    def test_login(self):
        driver = self.driver
        driver.get("http://web1:8000/home/")
        #assert "CrystalBall" in driver.title

        element = driver.find_element_by_id("login")
        element.click()

        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")

        username.send_keys('priya2')
        password.send_keys('nakhre')
        #//*[@id="loginsubmit"]
        submit = driver.find_element_by_xpath("//*[@id='loginsubmit']")
        
        #submit = driver.find_element_by_id("loginsubmit")
        submit.click()
        exists = False
        try:
            driver.find_element_by_id("loginmessage")
        except NoSuchElementException:
            exists = False
            assert exists
        exists = True
        assert exists

    def test_create_bet(self):
        driver = self.driver
        driver.get("http://web1:8000/home/")
        assert "CrystalBall" in driver.title
        

        element = driver.find_element_by_id("login")
        element.click()

        username = driver.find_element_by_id("id_username")
        password = driver.find_element_by_id("id_password")

        username.send_keys('priya2')
        password.send_keys('nakhre')
        #//*[@id="loginsubmit"]
        submit = driver.find_element_by_xpath("//*[@id='loginsubmit']")
        
        #submit = driver.find_element_by_id("loginsubmit")
        submit.click()

    
        submit = driver.find_element_by_xpath('//*[@id="bs-example-navbar-collapse-1"]/ul[1]/li[2]/form/input')
        submit.click()

        driver.find_element_by_id("id_privacy").click()
        driver.find_element_by_id("id_response_limit").send_keys(5)
        driver.find_element_by_id("id_category").send_keys("school")
        driver.find_element_by_id("id_question").send_keys("Best School?")
        driver.find_element_by_id("id_description").send_keys("what the best school is")
        driver.find_element_by_id("id_min_buyin").send_keys(2)
        driver.find_element_by_id("id_per_person_cap").send_keys(3)
        driver.find_element_by_id("id_expiration").send_keys("10/31/2018")

        driver.find_element_by_xpath("//*[@id='createsubmit']").click()

        driver.implicitly_wait(10)
        exists = False
        try:
            driver.find_element_by_xpath("//*[@id='allbets']").click()
        except NoSuchElementException:
            exists = False
            assert exists
        exists = True
        assert exists

    def tearDown(self):
        self.driver.close()



if __name__ == '__main__':
    unittest.main()