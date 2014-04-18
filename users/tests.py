from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from users.models import UsersModel
from users.views import errors

# Create your tests here.
class LoginTestCase(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        # Build a user
        self.user = User.objects.create_user(username = "login", password = "login")
        self.user.save()

    def testLogin(self):
        # Test successful login
        response = self.client.post('/login/', {'username': 'login', 'passwd': 'login', 'login': 'Log In'})
        self.assertEqual(response.context['user'], self.user)
        self.client.logout()

        # Test unsuccessful login
        response = self.client.post('/login/', {'username': 'login', 'passwd': 'wrong', 'login': 'Log In'})
        self.assertEqual(response.context['message'], errors[UsersModel.ERR_BAD_CREDENTIALS])
        self.assertFalse(response.context['user'].is_authenticated())
        self.client.logout()

    def testLogout(self):
        self.assertTrue(self.client.login(username='login', password='login'))
        response = self.client.get('/login/')
        self.assertEqual(response.context['user'], self.user)
        response = self.client.post('/login/', {'logout': 'Log Out'})
        self.assertFalse(response.context['user'].is_authenticated())

    def testAddUser(self):
        # Test successful add
        response = self.client.post('/login/', {'username': 'add', 'passwd': '', 'adduser': 'Add User'})
        user = User.objects.get(username = 'add')
        self.assertEqual(response.context['user'], user)
        self.client.logout()

        # Test username too long
        too_long = 'x'*(UsersModel.MAX_USERNAME_LENGTH+1)
        response = self.client.post('/login/', {'username': too_long, 'passwd': '', 'adduser': 'Add User'})
        self.assertTrue('ADD USER ERROR' in response.context['message'])
        self.assertFalse(response.context['user'].is_authenticated())
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username = too_long)

        # Test blank username
        response = self.client.post('/login/', {'username': '', 'passwd': '', 'adduser': 'Add User'})
        self.assertTrue('ADD USER ERROR' in response.context['message'])
        self.assertFalse(response.context['user'].is_authenticated())
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username = '')

        # Test password too long
        too_long = 'x'*(UsersModel.MAX_PASSWORD_LENGTH+1)
        response = self.client.post('/login/', {'username': 'x', 'passwd': too_long, 'adduser': 'Add User'})
        self.assertTrue('ADD USER ERROR' in response.context['message'])
        self.assertFalse(response.context['user'].is_authenticated())
        with self.assertRaises(ObjectDoesNotExist):
            User.objects.get(username = 'x')

        # Test user conflict
        response = self.client.post('/login/', {'username': 'add', 'passwd': '', 'adduser': 'Add User'})
        self.assertEqual(response.context['message'], errors[UsersModel.ERR_USER_EXISTS])
        self.assertFalse(response.context['user'].is_authenticated())

    def tearDown(self):
        TestCase.tearDown(self)
        self.user.delete()