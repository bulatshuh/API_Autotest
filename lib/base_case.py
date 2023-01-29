from requests import Response
import json.decoder
from datetime import datetime


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

    def prepare_register_data(self, email=None):
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
