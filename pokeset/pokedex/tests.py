from django.test import TestCase
from selenium import webdriver
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

class AccessViewTestCase(TestCase):
    """
    Set of test cases that test access to the webpages of the website
    """

    def test_login_access(self):
        response = self.client.get('login')
        self.assertEqual(response.status_code, 200)

    def test_register_access(self):
        response = self.client.get('register')
        self.assertEqual(response.status_code, 200)

    def test_login_without_login_path_access(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)


class CorrectTemplateTestCase(TestCase):
    """
    Set of test cases that test if the right template was used
    """

    def test_login_template(self):
        response = self.client.get('login')
        self.assertTemplateUsed(response, 'login.html')

    def test_register_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'register.html')

    def test_login_without_login_path_template(self):
        response = self.client.get('')
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
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        cls.driver.set_window_size(1024, 768)
        cls.driver.implicitly_wait(5)
    
    @classmethod
    def tearDownClass(cls):
        # quit webdriver after all test cases have run
        cls.driver.quit()
        return super().tearDownClass()

    def test_register_access_from_login_page(self):
        # go to login webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')

        # click 'create new account' button and check if user is in the register webpage
        self.driver.find_element(By.CLASS_NAME, 'link_button').click()
        self.assertEqual(self.driver.current_url, url + '/pokedex/register/')

    def test_register_access_from_login_page(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/register')

        # click back button and check if user is in the login webpage
        self.driver.find_element(By.CLASS_NAME, 'link_back_button').click()
        self.assertEqual(self.driver.current_url, url + '/pokedex/login/') 

    def test_text_can_be_enter_in_username_input_login_page(self):
        # go to login webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')

        # get username input and check if text can be entered in the input box
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('username')
        self.assertEqual(username_input.get_attribute('value'), 'username') 

    def test_text_can_be_enter_in_password_input_login_page(self):
        # go to login webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')

        # get password input and check if text can be entered in the input box
        username_input = self.driver.find_element(By.NAME, 'password')
        username_input.send_keys('secret#1')
        self.assertEqual(username_input.get_attribute('value'), 'secret#1')
    
    def test_text_can_be_enter_in_username_input_register_page(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/register')

        # get username input and check if text can be entered in the input box
        username_input = self.driver.find_element(By.NAME, 'username')
        username_input.send_keys('username')
        self.assertEqual(username_input.get_attribute('value'), 'username')
    
    def test_text_can_be_enter_in_email_input_register_page(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/register')

        # get email input and check if text can be entered in the input box
        username_input = self.driver.find_element(By.NAME, 'email')
        username_input.send_keys('test@example.com')
        self.assertEqual(username_input.get_attribute('value'), 'test@example.com')
    
    def test_text_can_be_enter_in_password1_input_register_page(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/register')

        # get password1 input and check if text can be entered in the input box
        username_input = self.driver.find_element(By.NAME, 'password1')
        username_input.send_keys('secret')
        self.assertEqual(username_input.get_attribute('value'), 'secret')
    
    def test_text_can_be_enter_in_password2_input_register_page(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/register')

        # get password2 input and check if text can be entered in the input box
        username_input = self.driver.find_element(By.NAME, 'password2')
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
        chrome_options = Options()
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
        self.driver.get(url + '/pokedex/login')
        self.driver.find_element(By.CLASS_NAME, 'link_button').click()

        # register a valid new account and check if user has returned to 
        # login page if account is successfully register
        register_account(self.driver, 'test_user', 'test@example.com', 'secret#1', 'secret#1')
        self.assertEqual(self.driver.current_url, url + '/pokedex/login/')

    def test_login_new_account(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')
        self.driver.find_element(By.CLASS_NAME, 'link_button').click()

        # register new account and login and check if user 
        # has successfully signed into account
        register_account(self.driver, 'test_user', 'test@example.com', 'secret#1', 'secret#1')
        login_to_account(self.driver, 'test_user', 'secret#1')
        self.assertEqual(self.driver.current_url, url + '/pokedex/profiles/')
    
    def test_user_can_successfully_logout(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')
        self.driver.find_element(By.CLASS_NAME, 'link_button').click()
        
        # register new account, login and check if user can logout of account 
        register_account(self.driver, 'test_user', 'test@example.com', 'secret#1', 'secret#1')
        login_to_account(self.driver, 'test_user', 'secret#1')
        self.driver.find_element(By.CLASS_NAME, 'back_button').click()
        self.assertEqual(self.driver.current_url, url + '/pokedex/login/') 

    def test_click_login_button_with_no_login_details(self):
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')
        self.driver.find_element(By.CLASS_NAME, "confirm_button").click()
        self.assertEqual(self.driver.current_url, url + '/pokedex/login/') 

    def test_click_register_button_with_no_register_details(self):
        url = self.live_server_url
        self.driver.get(url + '/pokedex/register')
        self.driver.find_element(By.CLASS_NAME, "confirm_button").click()
        self.assertEqual(self.driver.current_url, url + '/pokedex/register/')    


# Helper functions for the testing

def register_account(driver: webdriver, username, email_account, password1, password2):
    # enter new account details
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'email').send_keys(email_account)
    driver.find_element(By.NAME, 'password1').send_keys(password1)
    driver.find_element(By.NAME, 'password2').send_keys(password2)

    # submit new account form
    driver.find_element(By.CLASS_NAME, 'confirm_button').click()

def login_to_account(driver: webdriver, username, password):
    # enter account details into sign in page
    driver.find_element(By.NAME, 'username').send_keys(username)
    driver.find_element(By.NAME, 'password').send_keys(password)

    # submit sign in information
    driver.find_element(By.CLASS_NAME, 'confirm_button').click()

