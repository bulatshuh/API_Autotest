from requests import Response
import json


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, message):
        try:
            response_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json format. Response is "{response.text}"'

        assert name in response_dict, f'Response json doesn\'t have key "{name}"'
        assert response_dict[name] == expected_value, message

    @staticmethod
    def assert_json_has_key(response: Response, name):
        try:
            response_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json format. Response is "{response.text}"'

        assert name in response_dict, f'Response json doesn\'t have key "{name}"'

    @staticmethod
    def assert_status_code(response: Response, code):
        assert response.status_code == code, \
            f'Unexpected status code = {response.status_code}, expected = {code}'

    @staticmethod
    def assert_json_has_no_key(response: Response, name):
        try:
            response_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json format. Response is "{response.text}"'

        assert name not in response_dict, f'Response json have key "{name}", but should not'

    @staticmethod
    def assert_json_has_keys(response: Response, names: list):
        try:
            response_dict = response.json()
        except json.JSONDecodeError:
            assert False, f'Response is not in json format. Response is "{response.text}"'

        for name in names:
            assert name in response_dict, f'Response json doesn\'t have key "{name}"'

    @staticmethod
    def assert_response_text(response: Response, text):
        assert response.text == text, 'Wrong response text'
