import pytest
from my_lib.base_case import BaseCase
from my_lib.my_requests import MyRequests
from my_lib.assertions import Assertions


@pytest.mark.new
class TestUserDelete(BaseCase):
    def test_user_delete_second_user(self):
        user_id = 2
        data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        response_authorization = MyRequests.post('/user/login',
                                                 data=data
                                                 )
        token = self.get_header(response_authorization, 'x-csrf-token')
        auth_sid = self.get_cookie(response_authorization, 'auth_sid')

        response = MyRequests.delete(f'/user/{user_id}',
                                     headers={'x-csrf-token': token},
                                     cookies={'auth_sid': auth_sid}
                                     )
        Assertions.assert_status_code(response, 400)
        Assertions.assert_response_text(response,
                                        'Please, do not delete test users with ID 1, 2, 3, 4 or 5.')

    def test_user_delete(self):
        response_values = self.create_and_login_new_user()

        # CHECK USER BEFORE DELETING
        response_check_before = MyRequests.get('/user/',
                                               data={'id': response_values["user_id"]}
                                               )
        Assertions.assert_status_code(response_check_before, 200)
        Assertions.assert_json_value_by_name(response_check_before,
                                             'username',
                                             response_values["username"],
                                             'Can\'t find username in response before deleting'
                                             )

        # DELETE USER
        response_delete = MyRequests.delete(f'/user/{response_values["user_id"]}',
                                            headers={'x-csrf-token': response_values["token"]},
                                            cookies={'auth_sid': response_values["auth_sid"]}
                                            )
        Assertions.assert_status_code(response_delete, 200)

        # CHECK USER AFTER DELETING
        response_check_after = MyRequests.get('/user/',
                                              data={'id': response_values["user_id"]}
                                              )
        Assertions.assert_status_code(response_check_after, 404)
        Assertions.assert_response_text(response_check_after, 'User not found')

    def test_user_delete_another_user(self):
        response_values_first = self.create_and_login_new_user()

        response_values_second = self.create_and_login_new_user()

        # CHECK FIRST USER BEFORE DELETING
        response_check_before = MyRequests.get('/user/',
                                               data={'id': response_values_first["user_id"]}
                                               )
        Assertions.assert_status_code(response_check_before, 200)
        Assertions.assert_json_value_by_name(response_check_before,
                                             'username',
                                             response_values_first["username"],
                                             'Can\'t find username in response before deleting'
                                             )

        # DELETE FIRST USER BY SECOND
        response_delete = MyRequests.delete(f'/user/{response_values_first["user_id"]}',
                                            headers={'x-csrf-token': response_values_second["token"]},
                                            cookies={'auth_sid': response_values_second["auth_sid"]}
                                            )
        Assertions.assert_status_code(response_delete, 200)

        # CHECK FIRST USER AFTER DELETING
        response_check_after = MyRequests.get('/user/',
                                              data={'id': response_values_first["user_id"]}
                                              )
        Assertions.assert_status_code(response_check_after, 200)
        Assertions.assert_json_value_by_name(response_check_after,
                                             'username',
                                             response_values_first["username"],
                                             'Can\'t find username in response before deleting'
                                             )
