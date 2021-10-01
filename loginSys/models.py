from django.db import models

# Class for create user (extend from User)
class user_second(models.Model):
	no_induk = models.CharField(max_length = 20)
	username = models.CharField(max_length = 50)
	status = models.CharField(max_length = 10)
	profile = models.CharField(max_length = 50, blank=True)

	def __str__(self):
		return self.username

# 2 class di bawah ini adalah turunan dari user second (extend)
class students_user(models.Model):
	no_induk = models.CharField(max_length = 20)
	guru_id = models.CharField(max_length = 20)

	def __str__(self):
		return self.no_induk

class theachers_user(models.Model):
	no_induk = models.CharField(max_length = 20)
	agency = models.CharField(max_length = 50)
	admin_id = models.CharField(max_length = 20)

	def __str__(self):
		return self.no_induk


