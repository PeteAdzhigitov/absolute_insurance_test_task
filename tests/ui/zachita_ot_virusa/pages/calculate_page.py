import datetime

import allure
from selenium.webdriver.common.by import By


class CalculatePage:
    def __init__(self, driver):
        self.driver = driver

        self.__absense_of_contact_with_covid_checkbox = self.driver.find_element(By.XPATH, '//span[@class="checkmark"]//preceding-sibling::input[@name="virus-contact"]')
        self.__insurance_sum = self.driver.find_element(By.XPATH, '//label[@class="off"]//parent::span')
        self.__cost_of_police_5_000 = self.driver.find_element(By.XPATH, '//input[@name="price" and @placeholder="5 000 ₽"]')
        self.__cost_of_police_1_500 = self.driver.find_element(By.XPATH, '//input[@name="price" and @placeholder="1 500 ₽"]')
        self.__conformation_that_you_havent_contacted_with_covid = self.driver.find_element(By.XPATH, '//span[@class="checkmark"]//preceding-sibling::input[@name="virus-contact"]//following-sibling::span')
        self.__agree_with_processing_personal_data = self.driver.find_element(By.XPATH, '//input[@name="agree-polis"]//following-sibling::span')
        self.__continue_button = self.driver.find_element(By.XPATH, '//span//parent::button[@name="calculate"]')
        self.__continue_button_is_disabled = self.driver.find_elements(By.XPATH, '//span//parent::button[@name="calculate" and @disabled] ')

        self.__date_start_of_police = self.driver.find_element(By.ID, 'dateStart').get_attribute('placeholder')
        self.__date_end_of_police = self.driver.find_element(By.ID, 'dateEnd').get_attribute('placeholder')
        self.__no_possible_to_buy_police_information_not_hiden = self.driver.find_elements(By.XPATH, '//div[@class="medicine-info"]')
        self.__no_possible_to_buy_police_information_hiden = self.driver.find_elements(By.XPATH, '//div[@class="medicine-info" and @hidden]')
        self.__hospitalisation_hiden = self.driver.find_element(By.XPATH, '//span[@class="hospitalization" and @hidden]').text
        self.__hospitalisation_not_hiden = self.driver.find_element(By.XPATH, '//span[@class="hospitalization"]').text

    def choose_500_000_policy(self):
        with allure.step('Choose policy wich costs 500 000'):
            start_of_policy = (datetime.date.today() + datetime.timedelta(days=15)).strftime('%d.%m.%Y')
            end_of_policy = (datetime.date.today() + datetime.timedelta(days=381)).strftime('%d.%m.%Y')
            if self.driver.find_elements(By.XPATH, '//span[@class="hospitalization"]')[0].text != '1 500':
                self.__insurance_sum.click()

            assert self.__date_start_of_police == start_of_policy
            assert self.__date_end_of_police == end_of_policy

    def choose_100_000_policy(self):
        with allure.step('Choose policy wich costs 100 000'):
            start_of_policy = (datetime.date.today() + datetime.timedelta(days=15)).strftime('%d.%m.%Y')
            end_of_policy = (datetime.date.today() + datetime.timedelta(days=381)).strftime('%d.%m.%Y')
            if self.driver.find_elements(By.XPATH, '//span[@class="hospitalization"]')[0].text != '500':
                self.__insurance_sum.click()

            assert self.__date_start_of_police == start_of_policy
            assert self.__date_end_of_police == end_of_policy

    def click_on_confirm_abscence_of_contact_with_covid(self):
        with allure.step('Click that there wasn\'t contact with someone with covid'):
            self.__conformation_that_you_havent_contacted_with_covid.click()

    def click_on_profession_in_area_of_medicine(self):
        with allure.step('Click on conformation that area of work is medicine'):
            self.driver.execute_script("window.scrollTo(605, 10)")
            medicine_profession = self.driver.find_element(By.CLASS_NAME, "checkbox-container")
            medicine_profession.click()
            assert len(self.__no_possible_to_buy_police_information_not_hiden) == 1

    def agree_with_processing_personal_data(self):
        with allure.step('Click on conformation that you agree with processing your personal data'):
            self.__agree_with_processing_personal_data.click()

    def click_continue_button(self):
        with allure.step('Click on continue button of calculate form'):
            assert self.__continue_button.is_enabled()
            self.__continue_button.click()

    def continue_button_not_enabled(self):
        with allure.step('Button is not enabled'):
            assert len(self.__continue_button_is_disabled) == 1