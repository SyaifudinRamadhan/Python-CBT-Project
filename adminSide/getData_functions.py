from . import models
from loginSys import models as models_2
from django.db.models import Q
import random as rd
from datetime import datetime as today

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
			listData = models.schedule_data.objects.filter(id_admin = key).order_by('-date','-start')
			print(listData)
		except Exception as e:
			print( str(e))
			listData = ''
	elif teach == True :
		try:
			listData = models.schedule_data.objects.filter(id_teacher = key).order_by('-date','-start')
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
				listData = models.schedule_data.objects.filter(id_admin = key, date_contains = query).order_by('-date')
			listData = models.schedule_data.objects.filter(id_teacher = keySch[0].guru_id).order_by('-date','-start')
			print(keySch[0].guru_id)
			print(listData)
		except Exception as e:
			print( str(e))
			listData = ''
	print(len(listData))
	return listData

def viewResultTest (request, key, admin = False, teach = False, students = True):

	if admin == True :
		data = models.result_test.objects.filter(id_admin = key).order_by('-id')
		print(data)
		return data
	elif teach == True :
		data = models.result_test.objects.filter(id_teacher = key).order_by('-id')
		print(data)
		return data
	else :
		data = models.result_test.objects.filter(id_students = key).order_by('-id')
		print(data)
		return data

# def getDataStdn (request):
# 	mainData = User.objects.filter(username = request.user)
# 	print(len(mainData))
# 	return True

def getQuestFile (request) :
	directory = ''
	confirm = ''
	END_Time = ''
	list_quest = []
	if request.method == 'POST' :
		token = request.POST['token']
		
		try:
			schedule = models.schedule_data.objects.get(token = token, date = today.now().date())
		except Exception as e:
			print('\n',e,'\n')
			confirm = 'Error, Token tidak tersedia.'

		if confirm == '' :
			# print(schedule.state,'\n')
			if schedule.state == 'active' :
				course = schedule.id_course
				id_teach = schedule.id_teacher
				s_time = str(today.now().time()).split('.')

				time_now = str(today.now().time()).split('.')
				end_time = str(schedule.end)
				print(time_now)

				t_time_now = today.strptime(time_now[0], "%H:%M:%S")
				t_end_time = today.strptime(end_time, "%H:%M:%S")
				if t_time_now < t_end_time :
					tmp = str(t_end_time - t_time_now).split(':')
					print(tmp,'\n')
					END_Time = int((int(tmp[0])*3600) + (int(tmp[1])*60) + int(tmp[2]))
					print(END_Time,'\n')
				else:
					END_Time = 0.001
						

				print(course)
				quest = models.quest_data.objects.filter(id_course = course, id_teacher = id_teach)
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

	return directory, confirm, END_Time, s_time[0]


def getDataTch (request):
	return True

def getDataAdmin (request):
	return True