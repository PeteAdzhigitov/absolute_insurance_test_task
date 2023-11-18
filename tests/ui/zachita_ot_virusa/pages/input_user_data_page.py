import time
from telnetlib import EC

import allure
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from enum import Enum
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait


class FieldsValidationTexts(Enum):
    NAME_NOT_SPECIFIED = 'Не указано имя.'
    NAME_OF_INSURED_NOT_SPECIFIED = 'Не указано имя.'
    SURNAME_NOT_SPECIFIED = 'Не указана фамилия.'
    SURNAME_OF_INSURED_NOT_SPECIFIED = 'Не указана фамилия.'
    DATE_OF_BIRTH_NOT_SPECIFIED = 'Не указана дата рождения.'
    AGE_HAVE_TO_BE_18_YEARS_OLD = 'Возраст страхователя должен быть не менее 18 лет'
    DATE_OF_BIRTH_OF_INSURED_NOT_SPECIFIED = 'Не указана дата рождения.'
    DATE_OF_BIRTH_OF_INSURED_NOT_COMPLY_WITH_RULES = 'Возраст застрахованного должен быть не менее 3 и не более 55 лет'
    DATE_OF_PASSPORT_RELEASE = 'Не указаны дата выдачи паспорта.'
    DATE_OF_PASSPORT_RELEASE_OF_INSURED = 'Не указаны дата выдачи паспорта.'
    SERIES_AND_NUMBER_OF_PASSPORT_NOT_SPECIFIED = 'Не указаны серия/номер паспорта.'
    SERIES_AND_NUMBER_OF_PASSPORT_NOT_SPECIFIED_OF_INSURED = 'Не указаны серия/номер паспорта.'
    EMAIL_NOT_SPECIFIED = 'Не указан E-Mail.'
    ADDRESS_NOT_SPECIFIED = 'Не указан адрес регистрации.'
    PHONE_NUMBER_NOT_SPECIFIED = 'Не указан номер телефона.'

class InputUserDataPage:

    def __init__(self, driver):
        self.driver = driver

        self.__buy_policy_page_title = self.driver.find_element(By.XPATH, '//h1[@class="calc-col-content__h1"]')
        self.user_name_field = self.driver.find_element(By.ID, 'name')
        self.user_date_of_birth_field = self.driver.find_element(By.ID, 'dateBirth')
        self.date_of_passport_release = self.driver.find_element(By.ID, 'idDate')
        self.user_passport_series_and_number_field = self.driver.find_element(By.ID, 'id')
        self.user_address_field = self.driver.find_element(By.ID, 'address')
        self.user_phone_field = self.driver.find_element(By.ID, 'phone')
        self.user_email_field = self.driver.find_element(By.ID, 'email')

        self.fio_of_insured_field = self.driver.find_element(By.ID, 'nameInsured')
        self.date_of_birth_of_insured_field = self.driver.find_element(By.ID, 'dateBirthInsured')
        self.series_and_number_of_passport_of_insured_field = self.driver.find_element(By.ID, 'idInsured')
        self.date_of_passport_release_insured_field = self.driver.find_element(By.ID, 'idDateInsured')

        self.__user_is_insured = self.driver.find_elements(By.XPATH, '//span[@class="checkmark"]')[3]
        self.__to_the_payment_button = self.driver.find_element(By.XPATH, '//button[@class="btn btn-default"]')
        self.__continue_button_is_invinsible = self.driver.find_elements(By.XPATH, '//button[@class="btn btn-default" and @disabled]')

        self.__no_possobility_to_buy_policy = self.driver.find_element(By.XPATH, '//div[@class="note"]')
        self.empty_space = self.driver.find_elements(By.XPATH, '//div[@class="calc-hr"]')[-1]

    def buy_policy_page(self):
        with allure.step('User is on a Buy policy page'):
            assert self.__buy_policy_page_title.is_displayed()

    def fill_user_data_form(self, user_data, user_is_insured=True):
        with allure.step('Fill user form'):
            self.driver.execute_script("window.scrollTo(207, 10)")
            if user_is_insured == True:
                if self.driver.find_element(By.ID, "addPerson").get_attribute('style') == 'display: none;':
                    pass
                else:
                    self.__user_is_insured.click()
            else:
                wait = WebDriverWait(self.driver, 10)
                if self.driver.find_element(By.ID, "addPerson").get_attribute('style') != 'display: block;':
                    self.__user_is_insured.click()
                    wait.until(EC.visibility_of_element_located((By.ID, 'nameInsured')))
                else:
                    pass

            self.user_name_field.send_keys(user_data.user_name)
            self.user_date_of_birth_field.send_keys(user_data.date_of_birth)
            self.date_of_passport_release.send_keys(user_data.date_of_passport_release)
            self.user_passport_series_and_number_field.send_keys(user_data.passport_series_and_number)
            self.user_address_field.send_keys(user_data.address)
            self.user_phone_field.send_keys(user_data.phone_number)
            self.user_email_field.send_keys(user_data.email)
            self.user_email_field.send_keys(Keys.ENTER)

    def fill_insured_person_info_form(self, user_data):
        with allure.step('Fill insured user form'):
            self.fio_of_insured_field.send_keys(user_data.insured_name)
            self.date_of_birth_of_insured_field.send_keys(user_data.insured_user_date_of_birth)
            self.date_of_birth_of_insured_field.send_keys(Keys.ENTER)
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.element_to_be_clickable((By.ID, 'idInsured')))
            self.series_and_number_of_passport_of_insured_field.send_keys(user_data.insured_passport_number)
            self.date_of_passport_release_insured_field.send_keys(user_data.insured_date_of_passport_release)

    def send_user_data_form(self):
        with allure.step('Send form'):
            self.__to_the_payment_button.click()
            wait = WebDriverWait(self.driver, 10)
            wait.until(EC.invisibility_of_element_located((By.XPATH, '//div[@class="loader" and @style="display: block;"]')))

    def there_is_no_posobility_to_buy_police(self):
        with allure.step('User is on payment page and can\'t buy policy'):
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.text_to_be_present_in_element((By.XPATH, '//div[@class="note"]'), 'К сожалению, оформление полиса онлайн невозможно.'))
            assert self.__no_possobility_to_buy_policy.text == 'К сожалению, оформление полиса онлайн невозможно.'

    def user_is_on_payment_page_500_000_policy(self):
        with allure.step('User is on payment page'):
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.visibility_of_element_located((By.XPATH, '//tui-svg[@automation-id="header__logo"]')))
            amount_to_pay = self.driver.find_element(By.XPATH, '//span[@automation-id="tui-money__integer-part"]')
            assert amount_to_pay.text == '5 000'

    def user_is_on_payment_page_100_000_policy(self):
        with allure.step('User is on payment page'):
            wait = WebDriverWait(self.driver, 30)
            wait.until(EC.visibility_of_element_located((By.XPATH, '//tui-svg[@automation-id="header__logo"]')))
            amount_to_pay = self.driver.find_element(By.XPATH, '//span[@automation-id="tui-money__integer-part"]')
            assert amount_to_pay.text == '1 500'


    def check_lack_of_last_name_error(self):
        with allure.step('Check surname field of user validation error'):
            self.__last_name_validation_error_text = self.driver.find_elements(By.XPATH, '//input[@name="lastName"]//following-sibling::div[@class="error"]')[1].text
            assert self.__last_name_validation_error_text == FieldsValidationTexts.SURNAME_NOT_SPECIFIED.value

    def check_lack_of_name_error(self):
        with allure.step('Check name field of user validation error'):
            self.__name_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="firstName"]//following-sibling::div[@class="error"]').text
            assert self.__name_validation_error_text == FieldsValidationTexts.NAME_NOT_SPECIFIED.value

    def check_lack_of_series_and_number_of_passport_error(self):
        with allure.step('Check series and number field of user validation error'):
            self.__series_and_number_of_passport_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="id"]//following-sibling::div[@class="error"]').text
            assert self.__series_and_number_of_passport_validation_error_text == FieldsValidationTexts.SERIES_AND_NUMBER_OF_PASSPORT_NOT_SPECIFIED.value

    def check_lack_date_of_birth_error(self):
        with allure.step('Check date of birth field of user validation error'):
            self.__date_of_birth_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="dateBirth"]//following-sibling::div[@class="error"]').text
            assert self.__date_of_birth_validation_error_text == FieldsValidationTexts.DATE_OF_BIRTH_NOT_SPECIFIED.value

    def check_lack_date_of_birth_error_les_then_18_years(self):
        with allure.step('Check date of birth not complies with the rules field of user validation error'):
            self.__date_of_birth_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="dateBirth"]//following-sibling::div[@class="error"]').text
            assert self.__date_of_birth_validation_error_text == FieldsValidationTexts.AGE_HAVE_TO_BE_18_YEARS_OLD.value

    def check_lack_date_of_passport_release(self):
        with allure.step('Check date of passport release field of user validation error'):
            self.__date_of_passport_release_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="idDate"]//following-sibling::div[@class="error"]').text
            assert self.__date_of_passport_release_validation_error_text == FieldsValidationTexts.DATE_OF_PASSPORT_RELEASE.value

    def check_lack_adrress_error(self):
        with allure.step('Check address field of user validation error'):
            self.__adress_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="address"]//following-sibling::div[@class="error"]').text
            assert self.__adress_validation_error_text == FieldsValidationTexts.ADDRESS_NOT_SPECIFIED.value

    def check_lack_email_error(self):
        with allure.step('Check email field of user validation error'):
            self.__email_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="email"]//following-sibling::div[@class="error"]').text
            assert self.__email_validation_error_text == FieldsValidationTexts.EMAIL_NOT_SPECIFIED.value

    def check_lack_phone_error(self):
        with allure.step('Check phone field of  user validation error'):
            self.__phone_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="phone"]//following-sibling::div[@class="error"]').text
            assert self.__phone_validation_error_text == FieldsValidationTexts.PHONE_NUMBER_NOT_SPECIFIED.value

    def check_lack_date_of_birth_of_insured_error(self):
        with allure.step('Check date of birth field of insured user validation error'):
            self.__date_of_birth_of_insured_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="dateBirthInsured"]//following-sibling::div[@class="error"]').text
            assert self.__date_of_birth_of_insured_validation_error_text == FieldsValidationTexts.DATE_OF_BIRTH_OF_INSURED_NOT_SPECIFIED.value

    def check_lack_date_of_birth_of_insured_error_not_correct_day(self):
        with allure.step('Check date of birth field of insured user validation error'):
            self.__date_of_birth_of_insured_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="dateBirthInsured"]//following-sibling::div[@class="error"]').text
            assert self.__date_of_birth_of_insured_validation_error_text == FieldsValidationTexts.DATE_OF_BIRTH_OF_INSURED_NOT_COMPLY_WITH_RULES.value

    def check_lack_date_of_passport_release_of_insured_error(self):
        with allure.step('Check date of passport release field of insured user validation error'):
            self.__date_of_passport_release_of_insured_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="idDateInsured"]//following-sibling::div[@class="error"]').text
            assert self.__date_of_passport_release_of_insured_validation_error_text == FieldsValidationTexts.DATE_OF_PASSPORT_RELEASE_OF_INSURED.value

    def check_lack_name_of_insured_error(self):
        with allure.step('Check name field of insured user validation error'):
            self.__first_name_insured_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="firstNameInsured"]//following-sibling::div[@class="error"]').text
            assert self.__first_name_insured_validation_error_text == FieldsValidationTexts.NAME_OF_INSURED_NOT_SPECIFIED.value

    def check_lack_surname_of_insured_error(self):
        with allure.step('Check surname field of insured user validation error'):
            self.__last_name_insured_validation_error_text = self.driver.find_elements(By.XPATH, '//input[@name="lastNameInsured"]//following-sibling::div[@class="error"]')[1].text
            assert self.__last_name_insured_validation_error_text == FieldsValidationTexts.SURNAME_OF_INSURED_NOT_SPECIFIED.value

    def check_lack_series_and_number_of_insured_error(self):
        with allure.step('Check series and number field of insured user validation error'):
            self.__series_and_number_of_passport_of_insured_validation_error_text = self.driver.find_element(By.XPATH, '//input[@name="idInsured"]//following-sibling::div[@class="error"]').text
            assert self.__series_and_number_of_passport_of_insured_validation_error_text == FieldsValidationTexts.SERIES_AND_NUMBER_OF_PASSPORT_NOT_SPECIFIED_OF_INSURED.value

    def click_on_user_is_insured(self):
        with allure.step('Click on insured checkbox'):
            self.driver.execute_script("window.scrollTo(207, 10)")
            self.__user_is_insured.click()

    def fill_element(self, element, keys):
        with allure.step(f'Fill element {element} with value {keys}'):
            element.send_keys(keys)