import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@pytest.mark.new
class TestUserRegister(BaseCase):

    def test_create_user_with_new_email(self):
        data = self.prepare_register_data()

        response = MyRequests.post('/user/', data=data)

        print(response.json())

        Assertions.assert_status_code(response, 200)
        Assertions.assert_json_has_key(response, 'id')

    def test_create_user_with_existing_email(self):
        email = 'vinkotov@exmaple.com'
        data = self.prepare_register_data(email)
        response = MyRequests.post('/user/', data=data)

        Assertions.assert_status_code(response, 400)
        assert response.content.decode('utf-8') == f'Users with email \'{email}\' already exists', \
            f'Unexpected response content {response.content}'
