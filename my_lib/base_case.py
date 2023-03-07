from requests import Response
import json.decoder
from datetime import datetime
from my_lib.my_requests import MyRequests


class BaseCase:
    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f'Can\'t find cookie with name {cookie_name}'
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f'Can\'t find header with name {header_name}'
        return response.headers[header_name]

    def get_json(self, response: Response, name):
        try:
            response_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in JSON format. Response is "{response.text}"'

        assert name in response_dict, f'Can\'t find {name} in JSON response'

        return response_dict[name]

    def prepare_valid_register_data(self, email=None):
        if email is None:
            base_part = 'learnqa'
            random_part = datetime.now().strftime('%m%d%Y%H%M%S')
            domain = '@example.com'
            email = f'{base_part}{random_part}{domain}'

        return {
            'password': '1234',
            'username': 'username_test',
            'firstName': 'name_test',
            'lastName': 'sec_name_test',
            'email': email
        }

    def create_new_invalid_email(self):
        base_part = 'learnqa'
        random_part = datetime.now().strftime('%m%d%Y%H%M%S')
        domain = 'example.com'
        email = f'{base_part}{random_part}{domain}'
        return email

    def prepare_invalid_register_data(self, condition):

        if condition == 'wrong_email':
            base_part = 'learnqa'
            random_part = datetime.now().strftime('%m%d%Y%H%M%S')
            domain = 'example.com'
            email = f'{base_part}{random_part}{domain}'

            return {
                'password': '1234',
                'username': 'username_test',
                'firstName': 'name_test',
                'lastName': 'sec_name_test',
                'email': email
            }

        if condition == 'short_name':
            base_part = 'learnqa'
            random_part = datetime.now().strftime('%m%d%Y%H%M%S')
            domain = 'example.com'
            email = f'{base_part}{random_part}{domain}'

            return {
                'password': '1234',
                'username': 'username_test',
                'firstName': 'n',
                'lastName': 'sec_name_test',
                'email': email
            }

        if condition == 'long_name':
            base_part = 'learnqa'
            random_part = datetime.now().strftime('%m%d%Y%H%M%S')
            domain = 'example.com'
            email = f'{base_part}{random_part}{domain}'

            return {
                'password': '1234',
                'username': 'username_test',
                'firstName': 'name_test_name_test_name_test_name_test_name_test_name_test_'
                             'name_test_name_test_name_test_name_test_name_test_name_test_'
                             'name_test_name_test_name_test_name_test_name_test_name_test_'
                             'name_test_name_test_name_test_name_test_name_test_name_test_'
                             'name_test_name_test_name_test_name_test_name_test_name_test_'
                             'name_test_name_test_name_test_name_test_name_test_name_test_'
                             'name_test_name_test_name_test_name_test_name_test_name_test_',
                'lastName': 'sec_name_test',
                'email': email
            }

        if condition == 'wrong_email':
            base_part = 'learnqa'
            random_part = datetime.now().strftime('%m%d%Y%H%M%S')
            domain = 'example.com'
            email = f'{base_part}{random_part}{domain}'

            return {
                'password': '1234',
                'username': 'username_test',
                'firstName': 'name_test',
                'lastName': 'sec_name_test',
                'email': email
            }

        if condition == 'password':
            base_part = 'learnqa'
            random_part = datetime.now().strftime('%m%d%Y%H%M%S')
            domain = 'example.com'
            email = f'{base_part}{random_part}{domain}'

            return {
                'password': None,
                'username': 'username_test',
                'firstName': 'name_test',
                'lastName': 'sec_name_test',
                'email': email
            }

        if condition == 'username':
            base_part = 'learnqa'
            random_part = datetime.now().strftime('%m%d%Y%H%M%S')
            domain = 'example.com'
            email = f'{base_part}{random_part}{domain}'

            return {
                'password': '1234',
                'username': None,
                'firstName': 'name_test',
                'lastName': 'sec_name_test',
                'email': email
            }

        if condition == 'firstName':
            base_part = 'learnqa'
            random_part = datetime.now().strftime('%m%d%Y%H%M%S')
            domain = 'example.com'
            email = f'{base_part}{random_part}{domain}'

            return {
                'password': '1234',
                'username': 'username_test',
                'firstName': None,
                'lastName': 'sec_name_test',
                'email': email
            }

        if condition == 'lastName':
            base_part = 'learnqa'
            random_part = datetime.now().strftime('%m%d%Y%H%M%S')
            domain = 'example.com'
            email = f'{base_part}{random_part}{domain}'

            return {
                'password': '1234',
                'username': 'username_test',
                'firstName': 'name_test',
                'lastName': None,
                'email': email
            }

        if condition == 'email':

            return {
                'password': '1234',
                'username': 'username_test',
                'firstName': 'name_test',
                'lastName': '',
                'email': None
            }

    def create_and_login_new_user(self):
        # REGISTRATION
        register_data = self.prepare_valid_register_data()

        response_register = MyRequests.post('/user/', data=register_data)

        user_id = self.get_json(response_register, 'id')

        # LOGIN
        login_data = {
            'email': register_data['email'],
            'password': register_data['password']
        }

        response_authorization = MyRequests.post('/user/login',
                                                 data=login_data
                                                 )

        token = self.get_header(response_authorization, 'x-csrf-token')
        auth_sid = self.get_cookie(response_authorization, 'auth_sid')

        dict_of_values = {
            'email': register_data['email'],
            'username': register_data['username'],
            'firstName': register_data['firstName'],
            'lastName': register_data['lastName'],
            'password': register_data['password'],
            'user_id': user_id,
            'token': token,
            'auth_sid': auth_sid
        }

        return dict_of_values
