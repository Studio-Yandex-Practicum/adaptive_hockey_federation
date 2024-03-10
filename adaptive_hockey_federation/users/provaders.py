import phonenumbers
from core.config.base_settings import PHONENUMBER_DEFAULT_REGION
from faker.providers.phone_number.ru_RU import Provider


class CustomPhoneProvider(Provider):
    def phone_number(self):
        while True:
            phone_number = self.numerify(self.random_element(self.formats))
            parsed_number = phonenumbers.parse(
                phone_number,
                PHONENUMBER_DEFAULT_REGION
            )
            if phonenumbers.is_valid_number(parsed_number):
                return phonenumbers.format_number(
                    parsed_number,
                    phonenumbers.PhoneNumberFormat.INTERNATIONAL
                )
