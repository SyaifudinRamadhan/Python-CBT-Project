import pandas as pd
from django.core.files.storage import FileSystemStorage
from . import models
from loginSys import models as user_sec
from django.core.files.storage import FileSystemStorage
import os
import random
import string
from datetime import datetime
# -------- general function -----------------------------
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

# ------------ Kontrol untuk menambah soal (admin) ---------------
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

# ---------- kontrol untuk menghapus soal ---------------------

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

# ----------- Kontroller untuk aktivasi dan deactivasi soal -----------
def set_active (request):
	ID = request.POST.get('id')
	set_data = models.schedule_data.objects.get(id = ID)
	set_data.state = 'active'
	set_data.save()

def set_deactive (request):
	ID = request.POST.get('id')
	set_data = models.schedule_data.objects.get(id = ID)
	set_data.state = 'deactive'
	set_data.save()

# ------ Kontroller pengolahan jadwal (tambah dan edit) -------------
def add_schedule_auto(request, data):
	err = ''
	for x in range(len(data)):
		tmp = []
		confirm = ''
		for y in range(1,8):
			if y == 1 and data[x][y] != '':
				date=''
				# print(type(data[x][y]))
				try:
					date = datetime.strptime(str(data[x][y]).split(' ')[0],'%Y-%m-%d').date()
				except Exception as e:
					confirm = e
				if confirm == '':
					tmp.append(date)
				else:
					err = str(x+1)+' '
					break
			elif (y >= 2 and y <=3) and data[x][y] != '':
				time = ''
				try:
					time = datetime.strptime(str(data[x][y]).split(' ')[0],'%H:%M:%S').time()
				except Exception as e:
					confirm =  e
				if confirm == '':
					tmp.append(time)
				else:
					err = str(x+1)+' '
					break
			elif y == 4 and data[x][y] != '':
				drt = ''
				try:
					drt = int(str(data[x][y]))
				except Exception as e:
					confirm = e
				if confirm == '':
					tmp.append(drt)
				else:
					err = str(x+1)+' '
					break
			elif y == 5 and data[x][y] != '':
				id_tch = ''
				try:
					key = user_sec.user_second.objects.get(username = str(data[x][y])).no_induk
					id_tch = user_sec.theachers_user.objects.get(no_induk = key).no_induk
				except Exception as e:
					confirm = e
				if confirm == '':
					tmp.append(id_tch)
				else:
					err = str(x+1)+' '
					break
			elif y == 6 and data[x][y] != '':
				id_course = ''
				# print(str(data[x][y]))
				try:
					id_course = models.course_data.objects.get(course_name = str(data[x][y])).id
				except Exception as e:
					confirm = e
				if confirm == '':
					tmp.append(id_course)
				else:
					err = str(x+1)+' '
					break
			elif y == 7 and data[x][y] != '':
				id_class = ''
				id_admin = ''
				token = ''
				state = 'deactive'
				for z in range(5):
					token += random.choice(string.ascii_letters)
				try:
					id_class = models.class_data.objects.get(class_name = str(data[x][y])).id
					id_admin = user_sec.user_second.objects.get(username = request.user).id
				except Exception as e:
					confirm = e

				if confirm == '':
					tmp.append(id_class)
					tmp.append(id_admin)
					tmp.append(token)
					tmp.append(state)
				else:
					err = str(x+1)+' '
					break
			if data[x][y] == '':
				confirm = 'Err, data tidak bisa di baca'

		print(confirm,' ',tmp,'\n')
		if confirm == '':
			add = models.schedule_data(
				date = tmp[0], start = tmp[1], end = tmp[2], duration = tmp[3],
				state = tmp[9], id_teacher = tmp[4], id_class = tmp[6], id_course = tmp[5],
				id_admin = tmp[7], token = tmp[8]
				)
			add.save()
		
	return err
			# print(x,'\n')
			# print(tmp,'\n')

def add_schedule_manual(request):
	token = ''
	for x in range(5):
		token += random.choice(string.ascii_letters)
	tmp = []
	tmp.append(request.POST.get('date'))
	tmp.append(request.POST.get('start'))
	tmp.append(request.POST.get('end'))
	tmp.append(request.POST.get('drt'))
	# mendapatkan ID teacher
	key = user_sec.user_second.objects.get(username = str(request.POST.get('tch'))).no_induk
	id_tch = user_sec.theachers_user.objects.get(no_induk = key).no_induk
	tmp.append(id_tch)
	# mendapatkan ID course
	id_course = models.course_data.objects.get(course_name = str(request.POST.get('course'))).id
	tmp.append(id_course)
	# mendapatkan ID class
	id_class = models.class_data.objects.get(class_name = str(request.POST.get('class'))).id
	tmp.append(id_class)
	# Mendapatkan ID admin
	id_admin = user_sec.user_second.objects.get(username = request.user).id
	tmp.append(id_admin)
	# mendapatkan token auto dan statud
	tmp.append(token)
	tmp.append('deactive')

	add = models.schedule_data(
		date = tmp[0], start = tmp[1], end = tmp[2], duration = tmp[3],
		state = tmp[9], id_teacher = tmp[4], id_class = tmp[6], id_course = tmp[5],
		id_admin = tmp[7], token = tmp[8]
		)
	add.save()

def edit_schedule_manual(request):
	ID = request.POST.get('id')
	token = ''
	for x in range(5):
		token += random.choice(string.ascii_letters)
	tmp = []
	tmp.append(request.POST.get('date'))
	tmp.append(request.POST.get('start'))
	tmp.append(request.POST.get('end'))
	tmp.append(request.POST.get('drt'))
	# mendapatkan ID teacher
	key = user_sec.user_second.objects.get(username = str(request.POST.get('tch'))).no_induk
	id_tch = user_sec.theachers_user.objects.get(no_induk = key).no_induk
	tmp.append(id_tch)
	# mendapatkan ID course
	id_course = models.course_data.objects.get(course_name = str(request.POST.get('course'))).id
	tmp.append(id_course)
	# mendapatkan ID class
	id_class = models.class_data.objects.get(class_name = str(request.POST.get('class'))).id
	tmp.append(id_class)
	# Mendapatkan ID admin
	id_admin = user_sec.user_second.objects.get(username = request.user).id
	tmp.append(id_admin)
	# mendapatkan token auto dan statud
	tmp.append(token)
	tmp.append('deactive')

	add = models.schedule_data.objects.get(id = ID)
	add.date = tmp[0] 
	add.start = tmp[1] 
	add.end = tmp[2]
	add.duration = tmp[3]
	add.state = tmp[9]
	add.id_teacher = tmp[4]
	add.id_class = tmp[6]
	add.id_course = tmp[5]
	add.id_admin = tmp[7]
	add.token = tmp[8]	
	add.save()

def del_schedule(request):
	ID = request.POST.get('id')
	delete = models.schedule_data.objects.get(id = ID)
	delete.delete()
	


				