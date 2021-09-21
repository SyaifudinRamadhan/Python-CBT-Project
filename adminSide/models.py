from django.db import models

# Create your models here.

# Mengambil turunan dari PK dari data guru (sec user)
class class_data (models.Model):
	class_name = models.CharField(max_length = 30)
	# FK
	id_teacher = models.CharField(max_length = 20)
	id_admin = models.IntegerField()

	def _str_(self):
		return self.class_name
	
class course_data (models.Model):
	course_name = models.CharField(max_length = 40)
	# FK
	id_teacher = models.CharField(max_length = 20)
	id_admin = models.IntegerField()

	def _str_(self):
		return self.course_name

# Mengambil turunan dari PK data guru (sec user), kelas, dan mapel
class schedule_data (models.Model):
	date = models.DateField()
	start = models.TimeField()
	end = models.TimeField()
	duration = models.IntegerField()
	state = models.CharField(max_length = 10)
	# FK
	id_teacher = models.CharField(max_length = 20)
	id_class = models.IntegerField()
	id_course = models.IntegerField()
	id_admin = models.IntegerField()
	token = models.CharField(max_length = 10)

	def _str_(self):
		return self.date

# Mengambil turunan dari PK data mapel, dan guru (sec user)
class quest_data (models.Model):
	serial_quest = models.CharField(max_length = 20)
	# FK
	id_teacher = models.CharField(max_length = 20)
	id_course = models.IntegerField()
	id_admin = models.IntegerField()

	def _str_(self):
		return self.serial_quest

# Mengambil turunan dari PK soal, dan data siswa (sec_user)
class result_test (models.Model):
	date = models.DateField()
	result = models.FloatField()
	state_test = models.CharField(max_length = 10, blank = True)
	token = models.CharField(max_length = 10, blank = True)
	# FK
	id_quest = models.IntegerField()
	id_students = models.CharField(max_length = 20)
	id_admin = models.IntegerField()
	id_teacher = models.CharField(max_length = 20)

	def _str_(self):
		return self.date