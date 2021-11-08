from django.db import models

# Create your models here.

# Mengambil turunan dari PK dari data guru (sec user)
class class_data (models.Model):
	class_name = models.CharField(max_length = 30)
	# FK
	id_teacher = models.CharField(max_length = 20)
	id_admin = models.IntegerField()

	# def __str__(self):
	# 	return self.class_name
	
class course_data (models.Model):
	course_name = models.CharField(max_length = 40)
	# FK
	id_teacher = models.CharField(max_length = 20)
	id_admin = models.IntegerField()

	# def __str__(self):
	# 	return self.course_name

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

	def __str__(self):
		return str(self.date)

# Mengambil turunan dari PK data mapel, dan guru (sec user)
class quest_data (models.Model):
	serial_quest = models.CharField(max_length = 255)
	# FK
	id_teacher = models.CharField(max_length = 20)
	id_course = models.IntegerField()
	id_admin = models.IntegerField()
	id_class = models.IntegerField(null=True, blank=True)

	def __str__(self):
		return self.serial_quest

# Mengambil turunan dari PK soal, dan data siswa (sec_user)
class result_test (models.Model):
	date = models.DateField()
	result = models.FloatField()
	state_test = models.CharField(max_length = 10, blank = True)
	token = models.CharField(max_length = 10, blank = True)
	survey = models.CharField(max_length = 10)
	state_eval = models.CharField(max_length = 10)
	# FK
	id_quest = models.IntegerField()
	id_students = models.CharField(max_length = 20)
	id_admin = models.IntegerField()
	id_teacher = models.CharField(max_length = 20)

	def __str__(self):
		return str(self.date)

class evaluation_tch (models.Model):
	date = models.DateField()
	cat_1 = models.IntegerField()
	cat_2 = models.IntegerField()
	cat_3 = models.IntegerField()
	cat_4 = models.IntegerField()
	cat_5 = models.IntegerField()
	cat_6 = models.IntegerField()
	cat_7 = models.IntegerField()
	cat_8 = models.IntegerField()
	cat_9 = models.IntegerField()
	cat_10 = models.IntegerField()
	cat_11 = models.IntegerField()
	cat_spec = models.FloatField(null=True, blank=True)
	score = models.FloatField(null=True, blank=True)
	# Status ada 3 macam => evaluated, non, result
	state = models.CharField(max_length = 15)
	# FK
	id_teacher = models.CharField(max_length = 20)

	def __str__(self):
		return str(self.date)

class evaluation_stdn (models.Model):
	date = models.DateField()
	quote = models.CharField(max_length = 100)
	min_score = models.FloatField()
	max_score = models.FloatField()
	# FK
	id_students = models.CharField(max_length = 20)

	def __str__(self):
		return str(self.date)