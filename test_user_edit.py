import pytest
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests


@pytest.mark.new
class TestUserEdit(BaseCase):

    def test_edit_user_first_name(self):
        # REGISTRATION
        register_data = self.prepare_register_data()

        response_register = MyRequests.post('/user/', data=register_data)

        Assertions.assert_status_code(response_register, 200)
        Assertions.assert_json_has_key(response_register, 'id')

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

        # SHOW NOT EDITED DATA
        response_show_not_edited = MyRequests.get(f'/user/{user_id}',
                                                  headers={'x-csrf-token': token},
                                                  cookies={'auth_sid': auth_sid},
                                                  )

        print(response_show_not_edited.json()['firstName'])
        Assertions.assert_json_value_by_name(response_show_not_edited, 'firstName',
                                             register_data['firstName'], 'wrong first name!')

        # EDIT
        new_name = 'new_name'

        response_edit = MyRequests.put(f'/user/{user_id}',
                                       headers={'x-csrf-token': token},
                                       cookies={'auth_sid': auth_sid},
                                       data={'firstName': new_name}
                                       )
        Assertions.assert_status_code(response_edit, 200)

        # SHOW EDITED DATA

        response_show_edited = MyRequests.get(f'/user/{user_id}',
                                              headers={'x-csrf-token': token},
                                              cookies={'auth_sid': auth_sid},
                                              )
        print(response_show_edited.json()['firstName'])
        Assertions.assert_json_value_by_name(response_show_edited, 'firstName', new_name, 'wrong name after edit!')
