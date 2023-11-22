from django.test import TestCase
from django.urls import resolve, reverse

from main.views import LoginUser, NewUser, sign_out
from main.views import homePage, accountPage, notificationPage
from main.views import requestsPage, searchPage, changePassword

class TestUrls(TestCase):
    
    def setUp(self):
        self.message = "{0},URL test,Passed OK..."
        
    def test_main(self):
        loginURL = reverse("main:login")
        self.assertEquals(resolve(loginURL).func.view_class, LoginUser)
        print(self.message.format("/"))
        
    def test_newUser(self):
        signupUrl = reverse("main:signup")
        self.assertEquals(resolve(signupUrl).func.view_class, NewUser)
        print(self.message.format("/create/"))
        
    def test_signout(self):
        signout = reverse("main:logout")
        self.assertEquals(resolve(signout).func, sign_out)
        print(self.message.format("/logout/"))
        
    def test_home(self):
        homeURL = reverse("main:homePage")
        self.assertEquals(resolve(homeURL).func, homePage)
        print(self.message.format("/home/"))
        
    def test_account(self):
        accountURL = reverse("main:accountPage")
        self.assertEquals(resolve(accountURL).func, accountPage)
        print(self.message.format("/account/"))
        
    def test_notification(self):
        notificationsURL = reverse("main:notifications")
        self.assertEquals(resolve(notificationsURL).func, notificationPage)
        print(self.message.format("/notifications/"))
        
    def test_requests(self):
        requestsURL = reverse("main:requestsPage")
        self.assertEquals(resolve(requestsURL).func, requestsPage)
        print(self.message.format("/requests/"))
        
    def test_search(self):
        searchURL = reverse("main:searchPage")
        self.assertEquals(resolve(searchURL).func, searchPage)
        print(self.message.format("/search/"))
    
    def test_changePassword(self):
        changePasswordURL = reverse("main:changePassword")
        self.assertEquals(resolve(changePasswordURL).func, changePassword)
        print(self.message.format("/changePassword/"))
        
    
        