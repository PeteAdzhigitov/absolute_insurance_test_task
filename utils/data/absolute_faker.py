

from faker import Faker as OriginalFaker


class Faker(OriginalFaker):
    def __init__(self, locale='ru_RU'):
        super().__init__(locale)