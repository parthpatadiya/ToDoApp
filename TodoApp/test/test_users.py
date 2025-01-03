from .utils import *
from ..routers.users import get_db,get_current_user
from starlette import status

app.dependency_overrides[get_db]=override_get_db
app.dependency_overrides[get_current_user]=override_get_current_user



def test_return_user(test_user):
    response=client.get("/user")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["username"]=="parthp"
    assert response.json()["email"]=='parthp@gmail.com'
    assert response.json()['first_name']=='parth'
    assert response.json()['last_name']=='patadiya'
    assert response.json()['role']=='admin'
    assert response.json()['phone_number']=='111-111-1111'

def test_change_password_success(test_user):
    response=client.put('/user/password',json={"current_password":"test1234",
                                               "new_password":"newpassword"})
    assert response.status_code== status.HTTP_204_NO_CONTENT

def test_change_password_invalid_current_password(test_user):
    response=client.put('/user/password',json={"current_password":"wrongpassword",
                                               "new_password":"newpassword"})
    assert response.status_code== status.HTTP_401_UNAUTHORIZED
    assert response.json()=={'detail':'Error in password change!'}

def test_change_phone_number_success(test_user):
    response=client.put('/user/phonenumber/22222222222')
    assert response.status_code== status.HTTP_204_NO_CONTENT
