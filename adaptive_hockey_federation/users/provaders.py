import re

import phonenumbers
from core.config.base_settings import PHONENUMBER_DEFAULT_REGION
from faker.providers.phone_number.ru_RU import Provider
from users.constants import REGEX_AREA_CODE_IS_SEVEN_HUNDRED


class CustomPhoneProvider(Provider):
    """Класс провайдера для телефона."""

    def phone_number(self):
        """Получить номер телефона."""
        while True:
            phone_number = self.numerify(self.random_element(self.formats))
            parsed_number = phonenumbers.parse(
                phone_number,
                PHONENUMBER_DEFAULT_REGION,
            )
            if not re.search(
                REGEX_AREA_CODE_IS_SEVEN_HUNDRED,
                str(parsed_number.national_number),
            ):
                if phonenumbers.is_valid_number(parsed_number):
                    return phonenumbers.format_number(
                        parsed_number,
                        phonenumbers.PhoneNumberFormat.INTERNATIONAL,
                    )
