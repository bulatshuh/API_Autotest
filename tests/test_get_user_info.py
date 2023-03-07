import pytest
from my_lib.base_case import BaseCase
from my_lib.assertions import Assertions
from my_lib.my_requests import MyRequests


class TestUserAuthorize(BaseCase):

    def setup_method(self):
        self.data = {'id': '58976'}

    def test_get_non_authorized_user_info(self):
        response = MyRequests.get('/user/', data=self.data)

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_no_key(response, 'email')
        Assertions.assert_json_has_no_key(response, 'firstName')
        Assertions.assert_json_has_no_key(response, 'lastName')

    def test_get_authorized_user_info(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response1 = MyRequests.post('/user/login', data=data)

        token = self.get_header(response1, 'x-csrf-token')
        auth_sid = self.get_cookie(response1, 'auth_sid')
        user_id_from_authorization_request = self.get_json(response1, 'user_id')

        response2 = MyRequests.get(f'/user/{user_id_from_authorization_request}',
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid},
                                   )

        Assertions.assert_json_has_keys(response2, ['username', 'email', 'firstName', 'lastName'])

    @pytest.mark.new
    def test_get_authorized_another_user_info(self):
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post('/user/login', data=data)

        token = self.get_header(response_login, 'x-csrf-token')
        auth_sid = self.get_cookie(response_login, 'auth_sid')

        user_id_from_authorization_request = self.get_json(response_login, 'user_id')
        another_user_id = user_id_from_authorization_request - 1

        response = MyRequests.get(f'/user/{another_user_id}',
                                  headers={'x-csrf-token': token},
                                  cookies={'auth_sid': auth_sid},
                                  )

        Assertions.assert_json_has_key(response, 'username')
        Assertions.assert_json_has_no_key(response, 'email')
        Assertions.assert_json_has_no_key(response, 'firstName')
        Assertions.assert_json_has_no_key(response, 'lastName')
