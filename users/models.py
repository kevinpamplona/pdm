from django.db import models

class User(models.Model):
	user = models.CharField(max_length=128, primary_key=True)
	password = models.CharField(max_length=128)
	count = models.IntegerField(default=1)

	def __unicode__(self):
		return "[un:" + self.user + ", pw:" + self.password + ", #:" + str(self.count) + "]"

class UsersModel:

	def __init__(self):
		print "UsersModel initiated"

	# error codes
	SUCCESS = 1
	ERR_BAD_CREDENTIALS = -1
	ERR_USER_EXISTS = -2
	ERR_BAD_USERNAME = -3
	ERR_BAD_PASSWORD = -4

	# max lengths
	MAX_USERNAME_LENGTH = 128
	MAX_PASSWORD_LENGTH = 128

	def add(self, username, pw):
		if len(username) > UsersModel.MAX_USERNAME_LENGTH or len(username) == 0:
			return UsersModel.ERR_BAD_USERNAME
		if len(pw) > UsersModel.MAX_PASSWORD_LENGTH or len(pw) == 0:
			return UsersModel.ERR_BAD_PASSWORD
		if (User.objects.filter(user__exact=username)):
			return UsersModel.ERR_USER_EXISTS

		new_user = User(user=username, password=pw, count=1)
		new_user.save()
		return UsersModel.SUCCESS

	def login(self, username, pw):
		if (not User.objects.filter(user__exact=username)):
			return UsersModel.ERR_BAD_CREDENTIALS

		query = User.objects.filter(user__exact=username).filter(password__exact=pw)
		if (not query):
			return UsersModel.ERR_BAD_CREDENTIALS

		existing_user = User.objects.get(user__exact=username)
		new_count = existing_user.count + 1
		existing_user.count = new_count
		existing_user.save()
		return new_count

	def TESTAPI_resetFixture(self):
		User.objects.all().delete()
		return UsersModel.SUCCESS

g_users = UsersModel()