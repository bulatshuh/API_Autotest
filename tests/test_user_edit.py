import pytest
from my_lib.base_case import BaseCase
from my_lib.assertions import Assertions
from my_lib.my_requests import MyRequests


class TestUserEditPositive(BaseCase):
    def test_edit_user_first_name(self):
        # REGISTRATION
        register_data = self.prepare_valid_register_data()

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


@pytest.mark.new
class TestUserEditNegative(BaseCase):
    def test_edit_user_non_authorized(self):
        # REGISTRATION
        register_data = self.prepare_valid_register_data()

        response_register = MyRequests.post('/user/', data=register_data)

        Assertions.assert_status_code(response_register, 200)
        Assertions.assert_json_has_key(response_register, 'id')

        user_id = self.get_json(response_register, 'id')

        # EDIT
        new_name = 'new_name'

        response_edit = MyRequests.put(f'/user/{user_id}',
                                       data={'firstName': new_name}
                                       )
        assert response_edit.text == 'Auth token not supplied', 'Wrong error message in response'

    def test_edit_another_user(self):
        response_values_first = self.create_and_login_new_user()

        response_values_second = self.create_and_login_new_user()

        # SHOW USER DATA 1
        response_show_first_before = MyRequests.get(f'/user/{response_values_first["user_id"]}',
                                                    headers={'x-csrf-token': response_values_first["token"]},
                                                    cookies={'auth_sid': response_values_first["auth_sid"]},
                                                    )
        print(response_show_first_before.json())

        # SHOW USER DATA 2
        response_show_second_before = MyRequests.get(f'/user/{response_values_second["user_id"]}',
                                                     headers={'x-csrf-token': response_values_second["token"]},
                                                     cookies={'auth_sid': response_values_second["auth_sid"]},
                                                     )
        print(response_show_second_before.json())

        # EDIT 2nd user id but with 1st user token and auth_sid
        new_name = 'NEW_NAME'

        response_edit = MyRequests.put(f'/user/{response_values_second["user_id"]}',
                                       headers={'x-csrf-token': response_values_first["token"]},
                                       cookies={'auth_sid': response_values_first["auth_sid"]},
                                       data={'firstName': new_name}
                                       )
        Assertions.assert_status_code(response_edit, 200)

        # SHOW 1 USER DATA
        response_show_first = MyRequests.get(f'/user/{response_values_first["user_id"]}',
                                             headers={'x-csrf-token': response_values_first["token"]},
                                             cookies={'auth_sid': response_values_first["auth_sid"]},
                                             )
        Assertions.assert_json_value_by_name(response_show_first, 'firstName', 'NEW_NAME',
                                             'Wrong firstName')
        print(response_show_first.json())

        # SHOW 2 USER DATA
        response_show_second = MyRequests.get(f'/user/{response_values_second["user_id"]}',
                                              headers={'x-csrf-token': response_values_second["token"]},
                                              cookies={'auth_sid': response_values_second["auth_sid"]},
                                              )
        Assertions.assert_json_value_by_name(response_show_second, 'firstName', 'name_test',
                                             'Wrong firstName')
        print(response_show_second.json())

    def test_edit_user_to_wrong_email(self):
        response_values = self.create_and_login_new_user()

        # SHOW USER DATA
        response_show_second_before = MyRequests.get(f'/user/{response_values["user_id"]}',
                                                     headers={'x-csrf-token': response_values["token"]},
                                                     cookies={'auth_sid': response_values["auth_sid"]},
                                                     )
        print(response_show_second_before.json())

        # EDIT
        new_email = self.create_new_invalid_email()

        response_edit = MyRequests.put(f'/user/{response_values["user_id"]}',
                                       headers={'x-csrf-token': response_values["token"]},
                                       cookies={'auth_sid': response_values["auth_sid"]},
                                       data={'email': new_email}
                                       )
        Assertions.assert_status_code(response_edit, 400)
        Assertions.assert_response_text(response_edit, 'Invalid email format')

        # SHOW USER DATA
        response_show = MyRequests.get(f'/user/{response_values["user_id"]}',
                                       headers={'x-csrf-token': response_values["token"]},
                                       cookies={'auth_sid': response_values["auth_sid"]},
                                       )
        print(response_show.json())

        Assertions.assert_json_value_by_name(response_show, 'email', response_values["email"],
                                             'Email was changed to invalid!!!')

    def test_edit_user_to_short_name(self):
        response_values = self.create_and_login_new_user()

        # SHOW USER DATA
        response_show_second_before = MyRequests.get(f'/user/{response_values["user_id"]}',
                                                     headers={'x-csrf-token': response_values["token"]},
                                                     cookies={'auth_sid': response_values["auth_sid"]},
                                                     )
        print(response_show_second_before.json())

        # EDIT
        new_short_name = 'q'

        response_edit = MyRequests.put(f'/user/{response_values["user_id"]}',
                                       headers={'x-csrf-token': response_values["token"]},
                                       cookies={'auth_sid': response_values["auth_sid"]},
                                       data={'firstName': new_short_name}
                                       )
        Assertions.assert_status_code(response_edit, 400)
        Assertions.assert_json_value_by_name(response_edit, 'error',
                                             'Too short value for field firstName',
                                             'Wrong error message in json response')

        # SHOW USER DATA
        response_show = MyRequests.get(f'/user/{response_values["user_id"]}',
                                       headers={'x-csrf-token': response_values["token"]},
                                       cookies={'auth_sid': response_values["auth_sid"]},
                                       )
        print(response_show.json())

        Assertions.assert_json_value_by_name(response_show, 'firstName', response_values['firstName'],
                                             'Name was changed to invalid!!!')
