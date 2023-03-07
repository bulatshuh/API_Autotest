import pytest
from my_lib.base_case import BaseCase
from my_lib.assertions import Assertions
from my_lib.my_requests import MyRequests


class TestUserAuthorize(BaseCase):
    exclude_params = [
        ('no_cookie'),
        ('no_token')
    ]

    def setup(self):
        self.correct_data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }

        response_login = MyRequests.post('/user/login', data=self.correct_data)
        self.auth_sid = self.get_cookie(response_login, 'auth_sid')
        self.token = self.get_header(response_login, 'x-csrf-token')
        self.user_id = self.get_json(response_login, 'user_id')

    def test_good_authorization(self):
        response_auth = MyRequests.get('/user/auth',
                                       headers={'x-csrf-token': self.token},
                                       cookies={'auth_sid': self.auth_sid}
                                       )

        Assertions.assert_json_value_by_name(
            response_auth,
            'user_id',
            self.user_id,
            'User id from login and from auth are not equal'
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_request_without_cookies_or_token(self, condition):
        if condition == 'no_cookie':
            response_auth = MyRequests.get('/user/auth',
                                           headers={'x-csrf-token': self.token}
                                           )
        else:
            response_auth = MyRequests.get('/user/auth',
                                           cookies={'auth_sid': self.auth_sid}
                                           )

        Assertions.assert_json_value_by_name(
            response_auth,
            'user_id',
            0,
            f'Error User authorized with {condition}'
        )


class TestAuthorizeWithWrongEmail:
    def setup(self):
        self.wrong_data = {
            'email': 'test@example.com',
            'password': '1234'
        }

    def test_authorization_wrong_email(self):

        response = MyRequests.post('/user/login', data=self.wrong_data)

        text = response.text
        assert text == 'Invalid username/password supplied', f'Wrong error message'
