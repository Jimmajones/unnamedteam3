from django.test import TestCase
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FireFoxService
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from django.contrib.auth.models import User
from django.contrib.auth.models import UserManager

# URLs for testing
LOGIN_URL = '/accounts/login/'
REGISTER_URL = '/register/'
INDEX_URL = '/'
PROFILES_URL = '/profiles/'

# class names for testing
CONFIRM_CLASS = 'confirm_button'
BACK_CLASS = 'link_back_button'
LOGOUT_CLASS = 'logout'

class AccessViewTestCase(TestCase):
    """
    Set of test cases that test access to the webpages of the website
    """

    def test_login_access(self):
        response = self.client.get(LOGIN_URL)
        self.assertEqual(response.status_code, 200)

    def test_register_access(self):
        response = self.client.get(REGISTER_URL)
        self.assertEqual(response.status_code, 200)

    def test_login_without_login_path_access(self):
        response = self.client.get(INDEX_URL)
        self.assertEqual(response.status_code, 200)


class CorrectTemplateTestCase(TestCase):
    """
    Set of test cases that test if the right template was used
    """

    def test_login_template(self):
        response = self.client.get(LOGIN_URL)
        self.assertTemplateUsed(response, 'registration/login.html')

    def test_register_template(self):
        response = self.client.get(REGISTER_URL)
        self.assertTemplateUsed(response, 'register.html')

    def test_login_without_login_path_template(self):
        response = self.client.get(INDEX_URL)
        self.assertTemplateUsed(response, 'index.html')



class AccessViewTestCaseWithSelenium(StaticLiveServerTestCase):
    """
    Set of test cases that test access to the webpages from other
    webpages using Selenium
    """

    @classmethod
    def setUpClass(cls):
        # set up webdriver for test cases
        super().setUpClass()
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        cls.chrome_driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        cls.chrome_driver.set_window_size(1024, 768)
        cls.chrome_driver.implicitly_wait(5)
        firefox_options = FireFoxOptions()
        firefox_options.add_argument('--headless')
        cls.firefox_driver = webdriver.Firefox(service=FireFoxService(GeckoDriverManager().install()),options=firefox_options)
        cls.firefox_driver.set_window_size(1024, 768)
        cls.firefox_driver.implicitly_wait(5)
    
    @classmethod
    def tearDownClass(cls):
        # quit driver after all test cases have run
        cls.chrome_driver.quit()
        cls.firefox_driver.quit()
        return super().tearDownClass()

    def test_login_access_from_register_page(self):
        # go to register webpage
        url = self.live_server_url
        self.chrome_driver.get(url + REGISTER_URL)

        # click back button and check if user is in the login webpage
        self.chrome_driver.find_element(By.CLASS_NAME, BACK_CLASS).click()
        self.assertEqual(self.chrome_driver.current_url, url + LOGIN_URL)

        self.firefox_driver.get(url + REGISTER_URL)

        # click back button and check if user is in the login webpage
        self.firefox_driver.find_element(By.CLASS_NAME, BACK_CLASS).click()
        self.assertEqual(self.firefox_driver.current_url, url + LOGIN_URL) 

    def test_text_can_be_enter_in_username_input_login_page(self):
        # go to login webpage
        url = self.live_server_url
        self.chrome_driver.get(url + LOGIN_URL)

        # get username input and check if text can be entered in the input box
        username_input = self.chrome_driver.find_element(By.NAME, 'username')
        username_input.send_keys('username')
        self.assertEqual(username_input.get_attribute('value'), 'username') 

    def test_text_can_be_enter_in_password_input_login_page(self):
        # go to login webpage
        url = self.live_server_url
        self.chrome_driver.get(url + LOGIN_URL)

        # get password input and check if text can be entered in the input box
        username_input = self.chrome_driver.find_element(By.NAME, 'password')
        username_input.send_keys('secret#1')
        self.assertEqual(username_input.get_attribute('value'), 'secret#1')
    
    def test_text_can_be_enter_in_username_input_register_page(self):
        # go to register webpage
        url = self.live_server_url
        self.chrome_driver.get(url + REGISTER_URL)

        # get username input and check if text can be entered in the input box
        username_input = self.chrome_driver.find_element(By.NAME, 'username')
        username_input.send_keys('username')
        self.assertEqual(username_input.get_attribute('value'), 'username')
    
    def test_text_can_be_enter_in_email_input_register_page(self):
        # go to register webpage
        url = self.live_server_url
        self.chrome_driver.get(url + REGISTER_URL)

        # get email input and check if text can be entered in the input box
        username_input = self.chrome_driver.find_element(By.NAME, 'email')
        username_input.send_keys('test@example.com')
        self.assertEqual(username_input.get_attribute('value'), 'test@example.com')
    
    def test_text_can_be_enter_in_password1_input_register_page(self):
        # go to register webpage
        url = self.live_server_url
        self.chrome_driver.get(url + REGISTER_URL)

        # get password1 input and check if text can be entered in the input box
        username_input = self.chrome_driver.find_element(By.NAME, 'password1')
        username_input.send_keys('secret')
        self.assertEqual(username_input.get_attribute('value'), 'secret')
    
    def test_text_can_be_enter_in_password2_input_register_page(self):
        # go to register webpage
        url = self.live_server_url
        self.chrome_driver.get(url + REGISTER_URL)

        # get password2 input and check if text can be entered in the input box
        username_input = self.chrome_driver.find_element(By.NAME, 'password2')
        username_input.send_keys('secret')
        self.assertEqual(username_input.get_attribute('value'), 'secret')

class RegisterAndLoginTestCase(StaticLiveServerTestCase):
    """
    Set of test cases that test access to test successfully registering
    a new user and login
    """

    @classmethod
    def setUpClass(cls):
        # set up webdriver for test cases
        super().setUpClass()
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        cls.driver.set_window_size(1024, 768)
        cls.driver.implicitly_wait(5)
    
    @classmethod
    def tearDownClass(cls):
        # quit webdriver after all test cases have run
        cls.driver.quit()
        return super().tearDownClass()

    def test_registering_new_account(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)

        # register a valid new account and check if user has returned to 
        # login page if account is successfully register
        register_account(self.driver, 'test_user', 'test@example.com', 'secret#1', 'secret#1')
        self.assertEqual(self.driver.current_url, url + LOGIN_URL)

    def test_login_new_account(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)

        # register new account and login and check if user 
        # has successfully signed into account
        register_account(self.driver, 'test_user', 'test@example.com', 'secret#1', 'secret#1')
        login_to_account(self.driver, 'test_user', 'secret#1')
        self.assertEqual(self.driver.current_url, url + PROFILES_URL)
    
    def test_user_can_successfully_logout(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        
        # register new account, login and check if user can logout of account 
        register_account(self.driver, 'test_user', 'test@example.com', 'secret#1', 'secret#1')
        login_to_account(self.driver, 'test_user', 'secret#1')
        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        self.assertEqual(self.driver.current_url, url + INDEX_URL) 

    def test_click_login_button_with_no_login_details(self):
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL)
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + LOGIN_URL) 

    def test_click_register_button_with_no_register_details(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + REGISTER_URL)

    def test_click_login_button_with_no_password_login_details(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, 'test_user', 'test@example.com', 'secret#1', 'secret#1')
        self.driver.find_element(By.NAME, 'username').send_keys('test_user')
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + LOGIN_URL) 

    def test_click_login_button_with_no_username_login_details(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, 'test_user', 'test@example.com', 'secret#1', 'secret#1')
        self.driver.find_element(By.NAME, 'password').send_keys('secret#1')
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + LOGIN_URL)   
    
    def test_click_login_button_with_incorrect_password_login_details(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, 'test_user', 'test@example.com', 'secret#1', 'secret#1')
        self.driver.find_element(By.NAME, 'username').send_keys('test_user1')
        self.driver.find_element(By.NAME, 'password').send_keys('secret#2')
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + LOGIN_URL)      


# Helper functions for the testing

def register_account(driver: webdriver, username, email_account, password1, password2):
    # enter new account details
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'email').send_keys(email_account)
    driver.find_element(By.NAME, 'password1').send_keys(password1)
    driver.find_element(By.NAME, 'password2').send_keys(password2)

    # submit new account form
    driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()

def login_to_account(driver: webdriver, username, password):
    # enter account details into sign in page
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)

    # submit sign in information
    driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()

