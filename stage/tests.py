from django.test import TestCase, Client
from django.contrib.auth.models import User
from stage.models import Stage

try: 
    import simplejson as json
except ImportError: 
    import json

# Create your tests here.
class RenderTestCase(TestCase):
    def setUp(self):
        TestCase.setUp(self)
        # Build a user
        self.user = User.objects.create_user(username = "login", password = "login")
        self.user.save()

    def testRender(self):
        dat = '  #  \nS   E\n#####'
        data = {'width': 5, 'height': 3, 'data': dat}

        # Test results when logged in
        self.client.login(username='login', password='login')
        response = self.client.post('/stage/render', data = json.dumps(data), content_type="application/json")
        stageID = json.loads(response.content)['stageid']
        stage = Stage.objects.get(pk=stageID)
        self.assertEqual(stage.data, dat)
        self.assertEqual(stage.width, 5)
        self.assertEqual(stage.height, 3)
        self.assertEqual(stage.owner, 'login')
        self.assertTrue(len(Stage.objects.filter(owner='login')) > 0)
        self.client.logout()

        # Test result when logged out
        response = self.client.post('/stage/render', data = json.dumps(data), content_type="application/json")
        stageID = json.loads(response.content)['stageid']
        stage = Stage.objects.get(pk=stageID)
        self.assertEqual(stage.data, dat)
        self.assertEqual(stage.width, 5)
        self.assertEqual(stage.height, 3)
        self.assertEqual(stage.owner, '')

    def tearDown(self):
        TestCase.tearDown(self)
        self.user.delete()