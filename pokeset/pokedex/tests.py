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
from selenium.webdriver.common.keys import Keys
from django.contrib.auth.models import User
from .models import Pokemon, Profile

# URLs for testing
LOGIN_URL = '/accounts/login/'
REGISTER_URL = '/register/'
INDEX_URL = '/'
PROFILES_URL = '/profiles/'

# class names for testing
CONFIRM_CLASS = 'confirm_button'
BACK_CLASS = 'link_back_button'
LOGOUT_CLASS = 'logout'

# test account details
USERNAME = 'test_user'
EMAIL = 'test@example.com'
PASSWORD = 'secret#1'

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

    def test_index_access(self):
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

    def test_index_template(self):
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
    
    def test_login_access_from_index_page(self):
        # go to index page
        url = self.live_server_url
        self.chrome_driver.get(url + INDEX_URL)

        # click login link and check that user is in the login page
        self.chrome_driver.find_element(By.NAME, "login_link").click()
        self.assertEqual(self.chrome_driver.current_url, url + LOGIN_URL)

    def test_register_access_from_index_page(self):
        # go to index page
        url = self.live_server_url
        self.chrome_driver.get(url + INDEX_URL)

        # click login link and check that user is in the login page
        self.chrome_driver.find_element(By.NAME, "register_link").click()
        self.assertEqual(self.chrome_driver.current_url, url + REGISTER_URL)

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
        username_input.send_keys(PASSWORD)
        self.assertEqual(username_input.get_attribute('value'), PASSWORD)
    
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
        username_input.send_keys(EMAIL)
        self.assertEqual(username_input.get_attribute('value'), EMAIL)
    
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
        register_account(self.driver, USERNAME, EMAIL, PASSWORD, PASSWORD)
        self.assertEqual(self.driver.current_url, url + LOGIN_URL)

    def test_login_new_account(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)

        # register new account and login and check if user 
        # has successfully signed into account
        register_account(self.driver, USERNAME, EMAIL, PASSWORD, PASSWORD)
        login_to_account(self.driver, USERNAME, PASSWORD)
        self.assertEqual(self.driver.current_url, url + PROFILES_URL)
    
    def test_user_can_successfully_logout(self):
        # go to register webpage
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        
        # register new account, login and check if user can logout of account 
        register_account(self.driver, USERNAME, EMAIL, PASSWORD, PASSWORD)
        login_to_account(self.driver, USERNAME, PASSWORD)
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
        register_account(self.driver, USERNAME, EMAIL, PASSWORD, PASSWORD)
        self.driver.find_element(By.NAME, 'username').send_keys(USERNAME)
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + LOGIN_URL) 

    def test_click_login_button_with_no_username_login_details(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, USERNAME, EMAIL, PASSWORD, PASSWORD)
        self.driver.find_element(By.NAME, 'password').send_keys(PASSWORD)
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + LOGIN_URL) 
    
    def test_registering_new_account_with_no_username(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL) 
        self.driver.find_element(By.NAME, 'email').send_keys(EMAIL)
        self.driver.find_element(By.NAME, 'password1').send_keys(PASSWORD)
        self.driver.find_element(By.NAME, 'password2').send_keys(PASSWORD) 
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + REGISTER_URL)
    

    def test_registering_new_account_with_no_email(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL) 
        self.driver.find_element(By.NAME, 'username').send_keys(USERNAME)
        self.driver.find_element(By.NAME, 'password1').send_keys(PASSWORD)
        self.driver.find_element(By.NAME, 'password2').send_keys(PASSWORD) 
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + REGISTER_URL)
    
    def test_registering_new_account_with_no_password1(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL) 
        self.driver.find_element(By.NAME, 'username').send_keys(USERNAME)
        self.driver.find_element(By.NAME, 'email').send_keys(EMAIL)
        self.driver.find_element(By.NAME, 'password2').send_keys(PASSWORD) 
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + REGISTER_URL)
    
    def test_registering_new_account_with_no_password1(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL) 
        self.driver.find_element(By.NAME, 'username').send_keys(USERNAME)
        self.driver.find_element(By.NAME, 'email').send_keys(EMAIL)
        self.driver.find_element(By.NAME, 'password1').send_keys(PASSWORD) 
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + REGISTER_URL)
    
    def test_click_login_button_with_incorrect_password_login_details(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, USERNAME, EMAIL, PASSWORD, PASSWORD)
        self.driver.find_element(By.NAME, 'username').send_keys('test_user1')
        self.driver.find_element(By.NAME, 'password').send_keys('secret#2')
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.current_url, url + LOGIN_URL)  

    def test_registering_new_account_with_password1_and_password2_different(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, USERNAME, EMAIL, PASSWORD, 'secret#2')
        self.assertEqual(self.driver.current_url, url + REGISTER_URL)
    
    def test_user_access_account_after_before_session_expires(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, USERNAME, EMAIL, PASSWORD, PASSWORD)
        login_to_account(self.driver, USERNAME, PASSWORD)
        original_window = self.driver.current_window_handle
        self.driver.switch_to.new_window('window')
        self.driver.get(url + INDEX_URL)
        self.driver.find_element(By.NAME, 'profiles_link').click()
        self.assertEqual(self.driver.current_url, url + PROFILES_URL)
        self.driver.close()
        self.driver.switch_to.window(original_window)
    
    def test_user_access_account_after_before_session_expires(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, USERNAME, EMAIL, PASSWORD, PASSWORD)
        login_to_account(self.driver, USERNAME, PASSWORD)
        original_window = self.driver.current_window_handle
        self.driver.switch_to.new_window('window')
        self.driver.get(url + INDEX_URL)
        self.driver.find_element(By.NAME, 'profiles_link').click()
        self.assertEqual(self.driver.current_url, url + PROFILES_URL)
        self.driver.close()
        self.driver.switch_to.window(original_window)
    
    def test_register_account_with_password_less_than_eight_characters(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, USERNAME, EMAIL, 'secret1', 'secret1')
        self.assertEqual(self.driver.current_url, url + REGISTER_URL)
    
    def test_register_account_with_numeric_password(self):
        url = self.live_server_url
        self.driver.get(url + REGISTER_URL)
        register_account(self.driver, USERNAME, EMAIL, '123456789', '123456789')
        self.assertEqual(self.driver.current_url, url + REGISTER_URL)


class ProfileTestCases(StaticLiveServerTestCase):
    """
    Set of test cases that test the profiles page of the website
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
    
    def test_profiles_page_access(self):
        user = User.objects.create_user(USERNAME, EMAIL, PASSWORD)
        user.save()
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL)
        login_to_account(self.driver, USERNAME, PASSWORD)

        self.assertEqual(self.driver.current_url, url + PROFILES_URL)
        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        user.delete()
    
    def test_creating_new_profile(self):
        user = User.objects.create_user(USERNAME, EMAIL, PASSWORD)
        user.save()
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL)
        login_to_account(self.driver, USERNAME, PASSWORD)

        self.driver.find_element(By.NAME, "new_profile_circle").click()
        self.driver.find_element(By.NAME, "name").send_keys("test_profile")
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.find_element(By.NAME, "test_profile").text, "test_profile")
        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        user.delete()
    
    def test_cancel_creating_new_profile(self):
        user = User.objects.create_user(USERNAME, EMAIL, PASSWORD)
        user.save()
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL)
        login_to_account(self.driver, USERNAME, PASSWORD)

        self.driver.find_element(By.NAME, "new_profile_circle").click()
        self.driver.find_element(By.NAME, "name").send_keys("test_profile")
        self.driver.find_element(By.CLASS_NAME, "link_button").click()
        self.assertEqual(self.driver.find_element(By.CLASS_NAME, "profile_popup").get_attribute("style"),
        "display: none;")
        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        user.delete()
    
    def test_creating_profile_without_name(self):
        user = User.objects.create_user(USERNAME, EMAIL, PASSWORD)
        user.save()
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL)
        login_to_account(self.driver, USERNAME, PASSWORD)

        self.driver.find_element(By.NAME, "new_profile_circle").click()
        self.driver.find_element(By.CLASS_NAME, CONFIRM_CLASS).click()
        self.assertEqual(self.driver.find_element(By.CLASS_NAME, "profile_popup").get_attribute("style"), 
        "display: block;")
        self.driver.find_element(By.CLASS_NAME, "link_button").click()
        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        user.delete()

class RecordingPokemonTestCases(StaticLiveServerTestCase):
    """
    Set of test cases that test the functionality of recording
    pokemon on the website
    """

    @classmethod
    def setUpClass(cls):
        # set up webdriver for test cases
        super().setUpClass()
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        cls.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()),options=chrome_options)
        cls.driver.set_window_size(1024, 768)
        cls.driver.implicitly_wait(10)

    @classmethod
    def tearDownClass(cls):
        # quit webdriver after all test cases have run
        cls.driver.quit()
        return super().tearDownClass() 

    def test_dashboard_page_access(self):
        test_user = User.objects.create_user(USERNAME + "1", EMAIL, PASSWORD + "1")
        user_profile = Profile.objects.create(name="test_profile", user=test_user)
        test_user.save()
        user_profile.save()
        
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL)
        login_to_account(self.driver, USERNAME + "1", PASSWORD + "1")
        self.driver.find_element(By.NAME, "test_profile_button").click()
        self.assertEqual(self.driver.current_url, url + "/dashboard/5")

        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        user_profile.delete()
        test_user.delete()

    def test_create_pokemon_page_access_and_input(self):
        test_user = User.objects.create_user(USERNAME + "2", EMAIL, PASSWORD + "2")
        user_profile = Profile.objects.create(name="test_profile", user=test_user)
        test_user.save()
        user_profile.save()
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL)

        login_to_account(self.driver, USERNAME + "2", PASSWORD + "2")
        self.driver.find_element(By.NAME, "test_profile_button").click()
        self.driver.find_element(By.ID, "add_pokemon_button").click()
        self.assertEqual(self.driver.current_url, url + "/create_pokemon/2")

        username_input_name = self.driver.find_element(By.NAME, "name")
        username_input_name.send_keys("Pikachu")
        self.assertEqual(username_input_name.get_attribute('value'), "Pikachu")

        username_input_description = self.driver.find_element(By.NAME, "description")
        username_input_description.send_keys("This is a pokemon")
        self.assertEqual(username_input_description.get_attribute('value'), "This is a pokemon")

        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        user_profile.delete()
        test_user.delete()
    
    def test_create_pokemon_successfully(self):
        test_user = User.objects.create_user(USERNAME + "3", EMAIL, PASSWORD + "3")
        user_profile = Profile.objects.create(name="test_profile", user=test_user)
        test_user.save()
        user_profile.save()
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL)

        login_to_account(self.driver, USERNAME + "3", PASSWORD + "3")
        self.driver.find_element(By.NAME, "test_profile_button").click()
        self.driver.find_element(By.ID, "add_pokemon_button").click()

        self.driver.find_element(By.NAME, "name").send_keys("Pikachu")
        self.driver.find_element(By.NAME, "description").send_keys("This is a pokemon")
        self.driver.find_element(By.NAME, "type_one").send_keys("e" + Keys.ENTER)
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()

        self.assertEqual(self.driver.current_url, url + "/edit_pokemon/1/")

        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        user_profile.delete()
        test_user.delete()

    def test_creating_pokemon_with_incomplete_details(self):
        test_user = User.objects.create_user(USERNAME + "4", EMAIL, PASSWORD + "4")
        user_profile = Profile.objects.create(name="test_profile", user=test_user)
        test_user.save()
        user_profile.save()
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL) 

        login_to_account(self.driver, USERNAME + "4", PASSWORD + "4")
        self.driver.find_element(By.NAME, "test_profile_button").click()
        self.driver.find_element(By.ID, "add_pokemon_button").click()

        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()

        self.driver.find_element(By.NAME, "name").clear()
        self.driver.find_element(By.NAME, "description").send_keys("This is a pokemon")
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()
        self.assertEqual(self.driver.current_url, url + "/create_pokemon/4")

        self.driver.find_element(By.NAME, "name").send_keys("Pikachu")
        self.driver.find_element(By.NAME, "type_one").send_keys("-" + Keys.ENTER)
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()
        self.assertEqual(self.driver.current_url, url + "/create_pokemon/4")

        self.driver.find_element(By.NAME, "name").send_keys("Pikachu")
        self.driver.find_element(By.NAME, "type_two").send_keys("e" + Keys.ENTER)
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()
        self.assertEqual(self.driver.current_url, url + "/create_pokemon/4")

        self.driver.find_element(By.CLASS_NAME, "back_button").click()
        self.assertEqual(self.driver.current_url, url + "/dashboard/4")

        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        user_profile.delete()
        test_user.delete()

    def test_edit_and_detailed_view_access_from_dashboard(self):
        test_user = User.objects.create_user(USERNAME + "5", EMAIL, PASSWORD + "5")
        user_profile = Profile.objects.create(name="test_profile", user=test_user)
        test_pokemon = Pokemon.objects.create(name="Pikachu", type_one="ELE", profile=user_profile)
        test_user.save()
        user_profile.save()
        test_pokemon.save()
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL) 

        login_to_account(self.driver, USERNAME + "5", PASSWORD + "5")
        self.driver.find_element(By.NAME, "test_profile_button").click()
        self.driver.find_element(By.CLASS_NAME, "sorting_1").click()
        self.assertEqual(self.driver.current_url, url + "/detailed_view/2/")

        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()
        self.assertEqual(self.driver.current_url, url + "/edit_pokemon/2/")

        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        user_profile.delete()
        test_user.delete()
        test_pokemon.delete()
    
    def test_editing_pokemon(self):
        test_user = User.objects.create_user(USERNAME + "6", EMAIL, PASSWORD + "6")
        user_profile = Profile.objects.create(name="test_profile", user=test_user)
        test_pokemon = Pokemon.objects.create(name="Pikachu", type_one="ELE", profile=user_profile)
        test_user.save()
        user_profile.save()
        test_pokemon.save()
        url = self.live_server_url
        self.driver.get(url + LOGIN_URL) 

        login_to_account(self.driver, USERNAME + "6", PASSWORD + "6")
        self.driver.find_element(By.NAME, "test_profile_button").click()
        self.driver.find_element(By.CLASS_NAME, "sorting_1").click()
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()

        # Test editing moves
        self.driver.find_element(By.ID, "moves").find_element(By.TAG_NAME, "button").click()
        self.driver.find_element(By.ID, "add_move").find_element(By.ID, "move_name").send_keys("electric attack")
        self.driver.find_element(By.ID, "add_move").find_element(By.NAME, "move_type").send_keys("e" + Keys.ENTER)
        self.driver.find_element(By.ID, "add_move").find_element(By.CLASS_NAME, "confirm_button").click()
        self.assertEqual(self.driver.current_url, url + "/detailed_view/3/")
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()

        self.assertEqual(self.driver.find_element(By.ID, "moves").find_element(By.NAME, "can_learn").find_element(
            By.TAG_NAME, "option").text, "electric attack")

        # Test editing abilities
        self.driver.find_element(By.ID, "abilities").find_element(By.TAG_NAME, "button").click()
        self.driver.find_element(By.ID, "add_ability").find_element(By.ID, "ability_name").send_keys("dance")
        self.driver.find_element(By.ID, "add_ability").find_element(By.CLASS_NAME, "confirm_button").click()
        self.assertEqual(self.driver.current_url, url + "/detailed_view/3/")
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()

        self.assertEqual(self.driver.find_element(By.ID, "abilities").find_element(By.NAME, "abilities").find_element(
            By.TAG_NAME, "option").text, "dance")
        
        # Test editing locations
        self.driver.find_element(By.ID, "location").find_element(By.TAG_NAME, "button").click()
        self.driver.find_element(By.ID, "add_location").find_element(By.ID, "location_name").send_keys("the park")
        self.driver.find_element(By.ID, "add_location").find_element(By.CLASS_NAME, "confirm_button").click()
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()
        self.assertEqual(self.driver.current_url, url + "/edit_pokemon/3/")

        self.assertEqual(self.driver.find_element(By.ID, "location").find_element(By.NAME, "can_find_in").find_element(
            By.TAG_NAME, "option").text, "the park")
        
        # test changing the name of the pokemon
        self.driver.find_element(By.ID, "name").find_element(By.ID, "id_name").clear()
        self.driver.find_element(By.ID, "name").find_element(By.ID, "id_name").send_keys("mew" + Keys.ENTER)
        self.assertEqual(self.driver.current_url, url + "/detailed_view/3/")
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()
        self.assertEqual(self.driver.find_element(By.ID, "name").find_element(By.ID, "id_name").get_attribute("value"), "mew")

        # test changing the description of the pokemon
        self.driver.find_element(By.ID, "description").find_element(By.ID, "id_description").clear()
        self.driver.find_element(By.ID, "description").find_element(By.ID, "id_description").send_keys("this is a pokemon" + Keys.ENTER)
        self.assertEqual(self.driver.current_url, url + "/detailed_view/3/")
        self.driver.find_element(By.CLASS_NAME, "big_bottom_button").click()
        self.assertEqual(self.driver.find_element(By.ID, "description").find_element(By.ID, "id_description").get_attribute("value"), "this is a pokemon")

         # test changing type one of the pokemon
        self.driver.find_element(By.ID, "type_one").find_element(By.ID, "id_type_one").send_keys("p" + Keys.ENTER)
        self.assertEqual(self.driver.find_element(By.ID, "type_one").find_element(By.ID, "id_type_one").get_attribute("value"), "PSY")

        # test changing type two of the pokemon
        self.driver.find_element(By.ID, "type_two").find_element(By.ID, "id_type_two").send_keys("s" + Keys.ENTER)
        self.assertEqual(self.driver.find_element(By.ID, "type_two").find_element(By.ID, "id_type_two").get_attribute("value"), "STE")
       
       
        self.driver.find_element(By.CLASS_NAME, LOGOUT_CLASS).click()
        test_user.delete()
        user_profile.delete()
        test_pokemon.delete()
    
    
   
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

