from . import models
from loginSys import models as models_2
from django.db.models import Q
import random as rd

def getSchedule (request, key, admin = False, teach = False, students = True):
	listData = ''

	if admin == True :
		try:
			# if request.method == "POST" :
			# 	query = request.POST['search']
			# 	listData = models.schedule_data.objects.filter(id_admin = key,
			# 	 (Q(date_icontains = query) | 
			# 	 Q(start_icontains = query) | 
			# 	 Q(state_icontains = query)))
			listData = models.schedule_data.objects.filter(id_admin = key)
			print(listData)
		except Exception as e:
			print( str(e))
			listData = ''
	elif teach == True :
		try:
			listData = models.schedule_data.objects.filter(id_teacher = key)
			print(listData)
		except Exception as e:
			print( str(e))
			listData = ''
	else :
		print('masuk',' ',key)
		keySch = models_2.students_user.objects.filter(no_induk = key)
		
		try:
			if request.method == "POST" :
				query = request.POST['search']
				print('\nIsi search ',query,'\n')
				listData = models.schedule_data.objects.filter(id_admin = key, date_contains = query)
			listData = models.schedule_data.objects.filter(id_teacher = keySch[0].guru_id)
			print(keySch[0].guru_id)
			print(listData)
		except Exception as e:
			print( str(e))
			listData = ''
	print(len(listData))
	return listData

def viewResultTest (request, key, admin = False, teach = False, students = True):

	if admin == True :
		data = models.result_test.objects.filter(id_admin = key)
		print(data)
		return data
	elif teach == True :
		data = models.result_test.objects.filter(id_teacher = key)
		print(data)
		return data
	else :
		data = models.result_test.objects.filter(id_students = key)
		print(data)
		return data

# def getDataStdn (request):
# 	mainData = User.objects.filter(username = request.user)
# 	print(len(mainData))
# 	return True

def getQuestFile (request) :
	directory = ''
	confirm = ''
	list_quest = []
	if request.method == 'POST' :
		token = request.POST['token']
		
		try:
			schedule = models.schedule_data.objects.get(token = token)
		except Exception as e:
			print('\n',e,'\n')
			confirm = 'Error, Token tidak tersedia.'

		if confirm == '' :
			# print(schedule.state,'\n')
			if schedule.state == 'active' :
				course = schedule.id_course
				print(course)
				quest = models.quest_data.objects.filter(id_course = course)
				# print(quest.serial_quest)
				
				if len(quest) != 0 :
					for i in range(len(quest)) :
						list_quest.append(quest[i].serial_quest)
				else :
					confirm = 'Error, Mapel tidak tersedia.'

			elif schedule.state == 'deactive' :
				confirm = 'Error, Token tidak aktif.'

		if len(list_quest) != 0 :
			print(list_quest)
			directory = rd.choice(list_quest)
			directory = 'media/'+directory
		else :
			confirm += 'Error, gagal mengambil direktori soal.'
		print(confirm,' ',directory,'\n')
	else :
		confirm = 'Tidak ada request POST.'

	return directory, confirm


def getDataTch (request):
	return True

def getDataAdmin (request):
	return True