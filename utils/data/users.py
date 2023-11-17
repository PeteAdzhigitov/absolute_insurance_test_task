from datetime import datetime


class User:
    def __init__(self,user_name, date_of_birth, date_of_passport_release, passport_series_and_number, phone_number, email, address='Москва'):
        self.user_name = user_name
        self.date_of_birth = date_of_birth.strftime('%d%m%Y')
        self.date_of_passport_release = date_of_passport_release.strftime('%d%m%Y')
        self.passport_series_and_number = ''.join(str(x) for x in passport_series_and_number)
        self.phone_number = ''.join(str(x) for x in phone_number)
        self.email = email
        self.address = address

class InsuredUser:
    def __init__(self, insured_user_email, insured_name, insured_user_date_of_birth, insured_date_of_passport_release, insured_passport_number):
        self.insured_user_email = insured_user_email
        self.insured_name = insured_name
        self.insured_user_date_of_birth = insured_user_date_of_birth.strftime('%d%m%Y')
        self.insured_date_of_passport_release = insured_date_of_passport_release.strftime('%d%m%Y')
        self.insured_passport_number = ''.join(str(x) for x in insured_passport_number)