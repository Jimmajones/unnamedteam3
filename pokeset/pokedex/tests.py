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
        response = self.client.get('/pokedex/login/')
        self.assertEqual(response.status_code, 200)

    def test_register_access(self):
        response = self.client.get('/pokedex/register/')
        self.assertEqual(response.status_code, 200)

    def test_login_without_login_path_access(self):
        response = self.client.get('')
        self.assertEqual(response.status_code, 200)


class CorrectTemplateTestCase(TestCase):
    """
    Set of test cases that test if the right template was used
    """

    def test_login_template(self):
        response = self.client.get('/login/')
        self.assertTemplateUsed(response, 'login.html')

    def test_register_template(self):
        response = self.client.get('/register/')
        self.assertTemplateUsed(response, 'register.html')

    def test_login_without_login_path_template(self):
        response = self.client.get('')
        self.assertTemplateUsed(response, 'login.html')



class AccessViewTestCaseWithSelenium(StaticLiveServerTestCase):
    """
    Set of test cases that test access to the webpages from other
    webpages using Selenium
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        cls.driver.set_window_size(1024, 768)
        cls.driver.implicitly_wait(5)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        return super().tearDownClass()

    def test_register_access_from_login_page(self):
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')
        self.driver.find_element(By.CLASS_NAME, 'link_button').click()
        self.assertEqual(self.driver.current_url, url + '/pokedex/register/')

    def test_register_access_from_login_page(self):
        url = self.live_server_url
        self.driver.get(url + '/pokedex/register')
        self.driver.find_element(By.CLASS_NAME, 'link_back_button').click()
        self.assertEqual(self.driver.current_url, url + '/pokedex/login/')
    

class RegisterAndLoginTestCase(StaticLiveServerTestCase):
    """
    Set of test cases that test access to test successfully registering
    a new user and login
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        cls.driver.set_window_size(1024, 768)
        cls.driver.implicitly_wait(5)
    
    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        return super().tearDownClass()

    def test_registering_new_account(self):
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')
        self.driver.find_element(By.CLASS_NAME, 'link_button').click()
        self.driver.find_element(By.NAME, 'username').send_keys('test_user')
        self.driver.find_element(By.NAME, 'email').send_keys('test@example.com')
        self.driver.find_element(By.NAME, 'password1').send_keys('secret#1')
        self.driver.find_element(By.NAME, 'password2').send_keys('secret#1')
        self.driver.find_element(By.CLASS_NAME, 'confirm_button').click()
        self.assertEqual(self.driver.current_url, url + '/pokedex/login/')

    def test_login_new_account(self):
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')
        self.driver.find_element(By.CLASS_NAME, 'link_button').click()
        self.driver.find_element(By.NAME, 'username').send_keys('test_user')
        self.driver.find_element(By.NAME, 'email').send_keys('test@example.com')
        self.driver.find_element(By.NAME, 'password1').send_keys('secret#1')
        self.driver.find_element(By.NAME, 'password2').send_keys('secret#1')
        self.driver.find_element(By.CLASS_NAME, 'confirm_button').click()
        self.driver.find_element(By.NAME, 'username').send_keys('test_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret#1')
        self.driver.find_element(By.CLASS_NAME, 'confirm_button').click()
        self.assertEqual(self.driver.current_url, url + '/pokedex/profiles/')
    
    def test_user_can_successfully_logout(self):
        url = self.live_server_url
        self.driver.get(url + '/pokedex/login')
        self.driver.find_element(By.CLASS_NAME, 'link_button').click()
        self.driver.find_element(By.NAME, 'username').send_keys('test_user')
        self.driver.find_element(By.NAME, 'email').send_keys('test@example.com')
        self.driver.find_element(By.NAME, 'password1').send_keys('secret#1')
        self.driver.find_element(By.NAME, 'password2').send_keys('secret#1')
        self.driver.find_element(By.CLASS_NAME, 'confirm_button').click()
        self.driver.find_element(By.NAME, 'username').send_keys('test_user')
        self.driver.find_element(By.NAME, 'password').send_keys('secret#1')
        self.driver.find_element(By.CLASS_NAME, 'confirm_button').click()
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




