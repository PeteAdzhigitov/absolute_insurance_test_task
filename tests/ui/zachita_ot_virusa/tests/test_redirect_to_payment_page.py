import datetime
import random
import time
from selenium.webdriver import Keys
from tests.ui.zachita_ot_virusa.pages.calculate_page import CalculatePage
from tests.ui.zachita_ot_virusa.pages.input_user_data_page import InputUserDataPage
from utils.data.gwt import GIVEN, WHEN, THEN
from utils.data.absolute_faker import Faker
from utils.data.users import User, InsuredUser

def test_calculate_500_ground_policy(driver):
    calculate_page = CalculatePage(driver)
    input_user_data_page = InputUserDataPage(driver)

    with GIVEN('User choose 500_000 policy'):
        calculate_page.choose_500_000_policy()
    with WHEN('User click on processing user data conformation and continue button'):
        calculate_page.click_on_confirm_abscence_of_contact_with_covid()
        calculate_page.agree_with_processing_personal_data()
        calculate_page.click_continue_button()
    with THEN('User redirected to Buy policy page'):
        input_user_data_page.buy_policy_page()

def test_calculate_100_ground_policy(driver):
    calculate_page = CalculatePage(driver)
    input_user_data_page = InputUserDataPage(driver)

    with GIVEN('User choose 100_000 policy'):
        calculate_page.choose_100_000_policy()
    with WHEN('User click on necessary conformations and continue button'):
        calculate_page.click_on_confirm_abscence_of_contact_with_covid()
        calculate_page.agree_with_processing_personal_data()
        calculate_page.click_continue_button()
    with THEN('User on Buy policy page'):
        input_user_data_page.buy_policy_page()

def test_continue_button_is_disabled_if_user_works_in_medicine_area_with_100_policy(driver):
    calculate_page = CalculatePage(driver)

    with GIVEN('User choose 100_000 policy'):
        calculate_page.choose_100_000_policy()

    with WHEN('User click on necessary conformations and that they work in medecine conformation'):
        calculate_page.click_on_confirm_abscence_of_contact_with_covid()
        calculate_page.agree_with_processing_personal_data()
        calculate_page.click_on_profession_in_area_of_medicine()

    with THEN('Continue button is disabled'):
        calculate_page.continue_button_not_enabled()


def test_continue_button_is_disabled_if_user_works_in_medicine_area_with_500_policy(driver):
    calculate_page = CalculatePage(driver)

    with GIVEN('User choose 500_000 policy'):
        calculate_page.choose_500_000_policy()

    with WHEN('User click on necessary conformations and that they work in medecine conformation'):
        calculate_page.click_on_confirm_abscence_of_contact_with_covid()
        calculate_page.click_on_profession_in_area_of_medicine()

    with THEN('Continue button is disabled'):
        calculate_page.continue_button_not_enabled()

def test_fill_and_successfully_send_form_with_a_valid_phone_number(driver):
    calculate_page = CalculatePage(driver)
    input_user_data_page = InputUserDataPage(driver)
    user = User(user_name=Faker(locale='ru_RU').name(),
                date_of_birth=Faker(locale='ru_RU').date_between('-30y', '-20y'),
                date_of_passport_release=Faker(locale='ru_RU').date_between('-20y', 'today'),
                passport_series_and_number=[random.randint(0, 9) for i in range(10)],
                phone_number=[9,1,6,0,9,4,2,8,6,7],
                email=Faker(locale='ru_RU').email(),
                address='Москва')

    with GIVEN('User choose 500_000 policy'):
        calculate_page.choose_500_000_policy()

    with WHEN('User click on processing user data conformation and continue button'):
        calculate_page.click_on_confirm_abscence_of_contact_with_covid()
        calculate_page.agree_with_processing_personal_data()
        calculate_page.click_continue_button()

    with THEN('User redirected to Buy policy page'):
        input_user_data_page.buy_policy_page()

    with WHEN('User filling form and sending it'):
        input_user_data_page.fill_user_data_form(user_data=user, user_is_insured=True)
        input_user_data_page.send_user_data_form()

    with THEN('There is no possibility to buy policy online note displaying'):
        input_user_data_page.user_is_on_payment_page()

def test_fill_and_successfully_send_form_with_not_valid_phone_number(driver):
    calculate_page = CalculatePage(driver)
    input_user_data_page = InputUserDataPage(driver)
    user = User(user_name=Faker(locale='ru_RU').name(),
                date_of_birth=Faker(locale='ru_RU').date_between('-30y', '-20y'),
                date_of_passport_release=Faker(locale='ru_RU').date_between('-20y', 'today'),
                passport_series_and_number=[random.randint(0, 9) for i in range(10)],
                phone_number=[0,0,0,0,9,4,2,8,6,7],
                email=Faker(locale='ru_RU').email(),
                address='Москва')

    with GIVEN('User choose 500_000 policy'):
        calculate_page.choose_500_000_policy()

    with WHEN('User click on processing user data conformation and continue button'):
        calculate_page.click_on_confirm_abscence_of_contact_with_covid()
        calculate_page.agree_with_processing_personal_data()
        calculate_page.click_continue_button()

    with THEN('User redirected to Buy policy page'):
        input_user_data_page.buy_policy_page()

    with WHEN('User filling form and sending it'):
        driver.implicitly_wait(5)
        input_user_data_page.fill_user_data_form(user_data=user, user_is_insured=True)
        input_user_data_page.send_user_data_form()

    with THEN('There is no possibility to buy policy online note displaying'):
        input_user_data_page.there_is_no_posobility_to_buy_police()

def test_fill_and_successfully_send_form_with_not_insured_user(driver):
    calculate_page = CalculatePage(driver)
    input_user_data_page = InputUserDataPage(driver)
    user = User(user_name=Faker(locale='ru_RU').name(),
                date_of_birth=Faker(locale='ru_RU').date_between('-30y', '-20y'),
                date_of_passport_release=Faker(locale='ru_RU').date_between('-20y', 'today'),
                passport_series_and_number=[random.randint(0, 9) for i in range(10)],
                phone_number=[0,0,0,0,9,4,2,8,6,7],
                email=Faker(locale='ru_RU').email(),
                address='Москва')

    insured_user = InsuredUser(insured_name=Faker(locale='ru_RU').name(),
                               insured_user_date_of_birth=Faker(locale='ru_RU').date_between('-37y', '-36y'),
                               insured_user_email=Faker(locale='ru_RU').email(),
                               insured_date_of_passport_release=Faker(locale='ru_RU').date_between('-20y', 'today'),
                               insured_passport_number=[random.randint(0, 9) for i in range(10)])

    with GIVEN('User choose 500_000 policy'):
        calculate_page.choose_500_000_policy()

    with WHEN('User click on processing user data conformation and continue button'):
        calculate_page.click_on_confirm_abscence_of_contact_with_covid()
        calculate_page.agree_with_processing_personal_data()
        calculate_page.click_continue_button()

    with THEN('User redirected to Buy policy page'):
        input_user_data_page.buy_policy_page()

    with WHEN('User filling form and sending it'):
        driver.implicitly_wait(5)
        input_user_data_page.fill_user_data_form(user_data=user, user_is_insured=False)
        input_user_data_page.fill_insured_person_info_form(user_data=insured_user)
        input_user_data_page.send_user_data_form()

    with THEN('There is no possibility to buy policy online note displaying'):
        input_user_data_page.there_is_no_posobility_to_buy_police()

def test_fields_validation_errors(driver):
    quite_recent_date = (datetime.date.today() - datetime.timedelta(days=700)).strftime('%d%m%Y')
    user = User(user_name = Faker(locale='ru_RU').name(),
                date_of_birth = Faker(locale='ru_RU').date_between('-30y','-20y'),
                date_of_passport_release = Faker(locale='ru_RU').date_between('-20y','today'),
                passport_series_and_number = [random.randint(0,9) for i in range(10)],
                phone_number = [0,0,0,0,9,4,2,8,6,7],
                email = Faker(locale='ru_RU').email(),
                address = 'Москва')

    insured_user = InsuredUser(insured_name = Faker(locale='ru_RU').name(),
                               insured_user_date_of_birth = Faker(locale='ru_RU').date_between('-37y','-36y'),
                               insured_user_email = Faker(locale='ru_RU').email(),
                               insured_date_of_passport_release = Faker(locale='ru_RU').date_between('-20y','today'),
                               insured_passport_number = [random.randint(0,9) for i in range(10)])

    calculate_page = CalculatePage(driver)
    input_user_data_page = InputUserDataPage(driver)

    with GIVEN('User choose 500_000 policy'):
        calculate_page.choose_500_000_policy()

    with WHEN('User click on processing user data conformation and continue button'):
        calculate_page.click_on_confirm_abscence_of_contact_with_covid()
        calculate_page.agree_with_processing_personal_data()
        calculate_page.click_continue_button()

    with THEN('User redirected to Buy policy page'):
        input_user_data_page.buy_policy_page()

    with WHEN('User clicks om insured user checkbox and send unfilled form'):
        input_user_data_page.click_on_user_is_insured()
        input_user_data_page.send_user_data_form()
        driver.implicitly_wait(5)

    with THEN('Validation errors show up'):
        pass

    with WHEN('User checks last name field and fill it with Users\'s Surname and send form'):
        input_user_data_page.check_lack_of_last_name_error()
        input_user_data_page.fill_element(input_user_data_page.user_name_field,
                                          user.user_name.split()[0])
        input_user_data_page.user_name_field.send_keys(Keys.ENTER)
        input_user_data_page.send_user_data_form()
        driver.implicitly_wait(5)

    with THEN('Name field validation error changed on lack of name'):
        input_user_data_page.check_lack_of_name_error()

    with WHEN('User checks other fields, checks insured_user Name, Date_of_birth fields and fill them'):
        input_user_data_page.check_lack_of_series_and_number_of_passport_error()
        input_user_data_page.check_lack_date_of_passport_release()
        input_user_data_page.check_lack_adrress_error()
        input_user_data_page.check_lack_email_error()
        input_user_data_page.check_lack_phone_error()
        input_user_data_page.check_lack_date_of_birth_error()
        input_user_data_page.empty_space.click()
        input_user_data_page.send_user_data_form()
        time.sleep(2)

        input_user_data_page.check_lack_date_of_birth_of_insured_error()
        input_user_data_page.check_lack_surname_of_insured_error()
        input_user_data_page.fill_element(input_user_data_page.fio_of_insured_field,
                                          insured_user.insured_name.split()[0])
        input_user_data_page.fill_element(input_user_data_page.date_of_birth_of_insured_field,quite_recent_date)
        input_user_data_page.send_user_data_form()
        driver.implicitly_wait(5)

    with THEN('Date of birth and Name field of insured user validates with another error'):
        input_user_data_page.check_lack_date_of_birth_of_insured_error_not_correct_day()
        input_user_data_page.check_lack_name_of_insured_error()
        driver.implicitly_wait(5)

    with WHEN('User clears date of birth and pass correct date'):
        input_user_data_page.date_of_birth_of_insured_field.clear()

        input_user_data_page.fill_element(input_user_data_page.date_of_birth_of_insured_field,
                                                                      insured_user.insured_user_date_of_birth)
        input_user_data_page.date_of_birth_of_insured_field.send_keys(Keys.ENTER)
        input_user_data_page.send_user_data_form()
        driver.implicitly_wait(1)

    with THEN('Additional fields are showed up and checked'):
        input_user_data_page.check_lack_date_of_passport_release_of_insured_error()
        input_user_data_page.check_lack_name_of_insured_error()
        input_user_data_page.check_lack_series_and_number_of_insured_error()