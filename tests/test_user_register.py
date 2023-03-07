import pytest
from my_lib.base_case import BaseCase
from my_lib.assertions import Assertions
from my_lib.my_requests import MyRequests


class TestUserRegisterPositive(BaseCase):

    def test_create_user_with_new_email(self):
        data = self.prepare_valid_register_data()

        response = MyRequests.post('/user/', data=data)

        print(response.json())

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@exmaple.com'
        data = self.prepare_valid_register_data(email)
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f'Users with email \'{email}\' already exists', \
            f'Unexpected response content {response.content}'


@pytest.mark.new
class TestUserRegisterNegative(BaseCase):
    list_of_fields = ['password', 'username', 'firstName',
                      'lastName', 'email']

    def test_create_user_without_at_symbol(self):
        data = self.prepare_invalid_register_data(condition='wrong_email')
        response = MyRequests.post('/user/', data=data)

        assert response.status_code == 400, 'Status code is not 400!!!'
        assert response.text == 'Invalid email format', 'Wrong error message in response'

    @pytest.mark.parametrize('field', list_of_fields)
    def test_create_user_without_one_field(self, field):
        data = self.prepare_invalid_register_data(condition=field)
        response = MyRequests.post('/user/', data=data)

        assert response.status_code == 400, 'Status code is not 400!!!'
        assert response.text == f'The following required params are missed: {field}'

    def test_create_user_with_short_name(self):
        data = self.prepare_invalid_register_data(condition='short_name')
        response = MyRequests.post('/user/', data=data)

        assert response.status_code == 400, 'Status code is not 400!!!'
        assert response.text == 'The value of \'firstName\' field is too short', \
            'Wrong error message in response'

    def test_create_user_with_long_name(self):
        data = self.prepare_invalid_register_data(condition='long_name')
        response = MyRequests.post('/user/', data=data)

        assert response.status_code == 400, 'Status code is not 400!!!'
        assert response.text == 'The value of \'firstName\' field is too long', \
            'Wrong error message in response'
