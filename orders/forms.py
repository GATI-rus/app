import re
from django import forms
# import phonenumbers


class CreateOrderForm(forms.Form):

    first_name = forms.CharField()
    last_name = forms.CharField()
    phone_number = forms.CharField()
    requires_delivery = forms.ChoiceField(
        choices=[
            ("0", False),
            ("1", True),
            ],
        )
    delivery_address = forms.CharField(required=False)
    payment_on_get = forms.ChoiceField(
        choices=[
            ("0", 'False'),
            ("1", 'True'),
            ],
        )
# Мой вариант
    # def clean_phone_number(self):
    #     data = self.cleaned_data['phone_number']
    #
    #     # Удаляем все символы, кроме цифр и плюса
    #     cleaned_data = re.sub(r'\D', '', data)
    #
    #     try:
    #         # Пытаемся разобрать номер телефона
    #         phone_number = phonenumbers.parse(cleaned_data, "RU")
    #
    #         # Проверяем, является ли номер телефона действительным
    #         if not phonenumbers.is_valid_number(phone_number):
    #             raise forms.ValidationError("Неверный формат номера")
    #
    #         # Возвращаем отформатированный номер телефона
    #         formatted_number = phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    #         return formatted_number
    #
    #     except phonenumbers.NumberParseException:
    #         raise forms.ValidationError("Неверный формат номера")

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("Номер телефона должен содержать только цифры")

        pattern = re.compile(r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Неверный формат номера")

        return data



    # first_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Введите ваше имя",
    #         }
    #     )
    # )

    # last_name = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Введите вашу фамилию",
    #         }
    #     )
    # )

    # phone_number = forms.CharField(
    #     widget=forms.TextInput(
    #         attrs={
    #             "class": "form-control",
    #             "placeholder": "Номер телефона",
    #         }
    #     )
    # )

    # requires_delivery = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", False),
    #         ("1", True),
    #     ],
    #     initial=0,
    # )

    # delivery_address = forms.CharField(
    #     widget=forms.Textarea(
    #         attrs={
    #             "class": "form-control",
    #             "id": "delivery-address",
    #             "rows": 2,
    #             "placeholder": "Введите адрес доставки",
    #         }
    #     ),
    #     required=False,
    # )

    # payment_on_get = forms.ChoiceField(
    #     widget=forms.RadioSelect(),
    #     choices=[
    #         ("0", 'False'),
    #         ("1", 'True'),
    #     ],
    #     initial="card",
    # )