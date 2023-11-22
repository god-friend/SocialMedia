from django.test import TestCase

from main.forms import ChangeUserForm, CreateUserForm, LoginForm
from main.models import Users


message = "{0},{1},{2},Passed OK..."

class TestForms(TestCase):
    
    def setUp(self):
        self.user = Users.objects.create_user(username="test", password="testuser@123")
        
    def test_ChangeUserForm(self):
        data = {
            "username": "test",
            "firstname": "test",
            "lastname": "user",
        }
        form = ChangeUserForm(data=data, instance=self.user)
        
        self.assertTrue(form.is_valid())
        
        print(message.format("ChangeUserForm()", "With User", form.is_valid()))
        
    def test_ChangeUserFormNoUser(self):
        data = {
            "firstname": "test",
            "lastname": "user",
        }
        form = ChangeUserForm(data=data)
        
        self.assertFalse(form.is_valid())
        
        print(message.format("ChangeUserForm()", "Without User", form.is_valid()))
        
    def test_CreateUserForm(self):
        data = {
            "username": "test1",
            "firstname": "test",
            "lastname": "user",
            "password1": "testuser@123",
            "password2": "testuser@123"
        }
        form = CreateUserForm(data=data)
        self.assertTrue(form.is_valid())
        print(message.format("CreateUserForm()", "New User", form.is_valid()))
    
    def test_CreateUserFormUserExists(self):
        data = {
            "username": "test",
            "firstname": "test",
            "lastname": "user",
            "password1": "testuser@123",
            "password2": "testuser@123"
        }
        form = CreateUserForm(data=data)
        self.assertFalse(form.is_valid())
        print(message.format("CreateUserForm()", "User exists", form.is_valid()))
        
    def test_LoginForm(self):
        data = {
            "username": "test",
            "password": "testuser@123"
        }
        form = LoginForm(data=data)
        self.assertTrue(form.is_valid())
        print(message.format("LoginForm()", "Authenticate User", form.is_valid()))
        
    def test_LoginFormNotExists(self):
        data = {
            "username": "testuser",
            "password": "testuser@123"
        }
        form = LoginForm(data=data)
        self.assertFalse(form.is_valid())
        print(message.format("LoginForm()", "User doesn't exists", form.is_valid()))