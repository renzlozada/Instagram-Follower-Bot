import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

my_user = os.environ["my_user"]
my_pass = os.environ["my_pass"]
account = "petermckinnon"


class InstaFollower:
    def __init__(self):
        self.mount_id = None
        edge_option = webdriver.EdgeOptions()
        edge_option.add_experimental_option('detach', True)
        self.driver = webdriver.Edge(options=edge_option)
        self.wait = WebDriverWait(self.driver, 60)
        self.driver.maximize_window()

    def login(self):
        """
        Opens a web browser and navigates to Instagram's login page.

        This method automates the login process by locating the login and password input fields,
        entering the provided username and password, and submitting the login form.

        :return: None
        """
        self.driver.get("https://www.instagram.com/")
        login_field = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[1]/div/label/input')))
        login_field.send_keys(my_user)
        pass_field = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="loginForm"]/div/div[2]/div/label/input')))
        pass_field.send_keys(my_pass)
        pass_field.send_keys(Keys.ENTER)
        time.sleep(10)

    def find_followers(self):
        """
        Navigates to a specific Instagram account's followers list and retrieves follower data.

        This method opens the Instagram account page specified by 'account', fetches the mountID
        for XPath generation, clicks on the 'Followers' button to open the followers modal,
        and scrolls through the modal to load all follower data.

        :return: None
        """
        self.driver.get(f"https://www.instagram.com/{account}/")
        time.sleep(5)
        self.search_mount_id()  # Fetches the mountID for the XPath
        followers = self.driver.find_element(By.XPATH,
                                             f'//*[@id="{self.mount_id}"]/div/div/div[2]/div/div/div/div[1]/div[1]/div[2]/div[2]/section/main/div/header/section/ul/li[2]/a')
        followers.click()
        modal = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, '_aano')))
        for i in range(2):
            self.driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", modal)
            time.sleep(2)

    def search_mount_id(self):
        """
        Searches for and retrieves the current ID needed for XPath generation.

        This method finds and extracts the current ID from the web page, which is used to generate
        the XPath for locating specific elements on the Instagram profile page.

        :return: None
        """
        div_list = self.driver.find_elements(By.TAG_NAME, 'div')
        self.mount_id = div_list[1].get_attribute("id")

    def follow(self):
        follow_available = True
        num = 1
        while follow_available:
            try:
                # This code section auto-populates the number of followers when the 'Followers' button is clicked.
                # To handle variations in the displayed count (e.g., sometimes showing 49), a try-block is used.
                # Additionally, it prints the order of the clicked button for tracking purposes.
                follow_button = self.driver.find_element(By.XPATH,
                                                         f'/html/body/div[5]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[2]/div[2]/div/div[{num}]/div/div/div/div[3]/div/button')
                print(f"Follow Button #: {num}")
                follow_button.click()
                time.sleep(3)
                num += 1
            except ElementClickInterceptedException:
                cancel_button = self.driver.find_element(By.XPATH,
                                                         '/html/body/div[6]/div[1]/div/div[2]/div/div/div/div/div/div/button[2]')
                cancel_button.click()
            except NoSuchElementException:
                print("`Following` limit reached. ")
                follow_available = False
