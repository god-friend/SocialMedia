from django.urls import reverse

from rest_framework.status import HTTP_302_FOUND, HTTP_200_OK

from api.tests.test_views_templates import CommonFuncs


class TestTemplates(CommonFuncs):
    
    def test_login(self):
        loginPage = reverse("main:login")
        self.getRequest(loginPage, None, HTTP_302_FOUND, "/",
                        anonStatus=HTTP_200_OK, anonTemp="auth/login.html")
        
        postData = {
            "username": self.user.username,
            "password": "Testuser@123"
        }
        self.postRequest(loginPage, HTTP_302_FOUND, "/", postData, None
                         , anonStatus=HTTP_302_FOUND, anonPost=postData)
        
    def test_create(self):
        signup = reverse("main:signup")
        self.getRequest(signup, None, HTTP_302_FOUND, "/create/",
                        anonStatus=HTTP_200_OK, anonTemp="auth/signup.html")
        
        postData = {
            "username": "newUser",
            "firstname": "myFirstName",
            "lastname": "myLastName",
            "password1": "testPass@123",
            "password2": "testPass@123"
        }
        self.postRequest(signup, HTTP_302_FOUND,"/create/", postData,
                         anonStatus=HTTP_302_FOUND, anonPost=postData)
    
    def test_logout(self):
        logout = reverse("main:logout")
        self.getRequest(logout, None, HTTP_302_FOUND, "logout", anonStatus=HTTP_302_FOUND)
    
    def test_home(self):
        homePage = reverse("main:homePage")
        self.getRequest(homePage, "main_app/index.html", HTTP_200_OK, "/home/",
                        anonStatus=HTTP_302_FOUND)
        
    def test_account(self):
        accountPage = reverse("main:accountPage")
        self.getRequest(accountPage, "main_app/index.html", HTTP_200_OK, "/account/",
                        anonStatus=HTTP_302_FOUND)
        
    def test_notifications(self):
        notificationsPage = reverse("main:notifications")
        self.getRequest(notificationsPage, "main_app/index.html", HTTP_200_OK, "/notifications/",
                        anonStatus=HTTP_302_FOUND)
        
    def test_requests(self):
        requestsPage = reverse("main:requestsPage")
        self.getRequest(requestsPage, "main_app/index.html", HTTP_200_OK, "/requests/",
                        anonStatus=HTTP_302_FOUND)
        
    def test_search(self):
        searchPage = reverse("main:searchPage")
        self.getRequest(searchPage, "main_app/index.html", HTTP_200_OK, "/search/",
                        anonStatus=HTTP_302_FOUND)
        
    def test_changePass(self):
        changePass = reverse("main:changePassword")
        self.getRequest(changePass, "main_app/index.html", HTTP_200_OK, "/changePassword/",
                        anonStatus=HTTP_302_FOUND)
        
        postData = {
            "nPass": "newPassword",
            "cPass": "newPassword"
        }
        self.postRequest(changePass, HTTP_302_FOUND, "/changePassword/", postData, 
                         anonStatus=HTTP_302_FOUND)