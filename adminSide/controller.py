import pandas as pd
from django.core.files.storage import FileSystemStorage
from . import models
from loginSys import models as user_sec
from django.core.files.storage import FileSystemStorage
import os
import random
import string

def getUniquePath(folder, filename):    
    path = os.path.join(folder, filename)
    while os.path.exists(path):
         path = path.split('.')[0] + ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + '.' + path.split('.')[1]
    return path

def create_xls(request, arr_data):
	final = [[''] * 21]+arr_data
	data_frame = pd.DataFrame(final)

	filename = getUniquePath('media/',str(str(request.user)+'.xls'))
	# filename = 'media/'+filename
	# writer = pd.ExcelWriter(filename, engine='xlsxwriter')
	data_frame.to_excel(filename, sheet_name='Quest', index=False)
	return filename

def add_quest_tbl_0(request):
	id_teach = request.POST.get('tch_id')
	id_course = request.POST.get('mapel')
	id_admin = request.POST.get('id_admin')

	add = models.quest_data(
			serial_quest = '-',
			id_teacher = id_teach,
			id_course = id_course,
			id_admin = id_admin
		)
	add.save()

def add_quest_tbl_1(request, filename, pss = 'admin', serial_quest = '-'):
	obj = ''
	if pss == 'admin':
		try:
			obj = models.quest_data.objects.get(
				id_admin = user_sec.user_second.objects.get(no_induk = request.user).id,
				serial_quest = serial_quest
				)
			fileName = filename.split('/')
			obj.serial_quest = fileName[1]
			obj.save()
			return ''
		except Exception as e:
			print(e,'\n')
			os.remove(filename)
			return 'Error, data tidak ketemu'
		
	elif pss == 'teacher':
		try:
			obj = models.quest_data.objects.get(id_teacher = request.userr, serial_quest = '-')
			obj.serial_quest = filename
			obj.save()
			return ''
		except Exception as e:
			print(e)
			os.remove(filename)
			return 'Error, data tidak ketemu'

def compare_file_in_xls(request, list_data):
	all_img = request.FILES.getlist('img')
	fs = FileSystemStorage()
	for x in range(len(all_img)):
		# Simpan dulu file gambarnya dan dapatkan urlnya
		up = fs.save(all_img[x].name, all_img[x])
		url = fs.url(up)
		name = url.split('/')[2]
		match = False
		for y in range(len(list_data)):
			for z in range(len(list_data[0])):
				if list_data[y][z] == all_img[x].name:
					list_data[y][z] = name
					match = True
		if match == False:
			try:
				dr = 'media/'+name
				os.remove(dr)
			except Exception as e:
				print(e,'\n')

	return list_data

def delete_for_quest(request, data, file_name):
	# 1. Menghapus file terlasi dengan XLS file
	for x in range(len(data)):
		for y in range(len(data[0])):
			url = 'media/'+str(data[x][y])
			try:
				os.remove(url)
			except Exception as e:
				print(e,'\n------ data tidak ada ------\n')

	# 2. Menghapus data di DB
	for_del = models.quest_data.objects.get(serial_quest = file_name)
	for_del.delete()
	# 3. Menghapus XLS file
	try:
		os.remove('media/'+file_name)
	except Exception as e:
		print(e,'\n---- data tidak ada------\n')