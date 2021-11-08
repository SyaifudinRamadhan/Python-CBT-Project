import pandas as pd
from django.core.files.storage import FileSystemStorage
from . import models
from . import getData_functions as f_get
from loginSys import models as user_sec
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
import os
import random
import string
from datetime import datetime
from . import evaluator

# del_class_on_id(obj_sec.no_induk)
# del_course_on_id(obj_sec.no_indukobj_sec.no_induk)
# del_quest_on_id(obj_sec.no_induk)
# del_schedule_on_id(obj_sec.no_induk)
# change_tch_id_stdn_on_id(obj_sec.no_induk)

# -------- general function -----------------------------
def getUniquePath(folder, filename):    
    path = os.path.join(folder, filename)
    while os.path.exists(path):
         path = path.split('.')[0] + ''.join(random.choice(string.ascii_lowercase) for i in range(10)) + '.' + path.split('.')[1]
    return path

def create_xls(request, arr_data):
	print(arr_data)
	final = [[''] * 21]+arr_data
	data_frame = pd.DataFrame(final)

	filename = getUniquePath('media/',str(str(str(request.user))+'.xls'))
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

# def cascade_del_on_id_tch(tch_no_induk_ID, data_object):
# 	count = data_object.filter(id_teacher = tch_no_induk_ID)
# 	for x in range(len(count)):
# 		obj = data_object.get(id = count[x].id)
# 		obj.delete()

# def set_dash_on_id_tch(tch_no_induk_ID, data_object):
# 	count = data_object.filter(id_teacher = tch_no_induk_ID)
# 	for x in range(len(count)):
# 		obj = data_object.get(id = count[x].id)
# 		obj.id_teacher = '-'

# def set_dash_stdn_tch_id(tch_no_induk_ID):
# 	count = models_2.students_user.objects.filter(guru_id = tch_no_induk_ID)
# 	for x in range(len(count)):
# 		obj = models_2.students_user.objects.get(id = count[x].id)
# 		obj.guru_id = '-'

# ------- FUngsi kontrol untuk mnegatasi hilangnya id teacher ---------
def change_tch_id_stdn_on_id(ID, by = 'teacher'):
	count = ''
	if by == 'teacher':
		print('Checkpoint 1')
		count = user_sec.students_user.objects.filter(guru_id = ID)
	elif by == 'class':
		count = user_sec.students_user.objects.filter(id_class = ID)
	
	for x in range(len(count)):
		obj = user_sec.students_user.objects.get(id = count[x].id)
		if by == 'teacher':
			obj.guru_id = '-'
			obj.id_class = None
		elif by == 'class':
			obj.id_class = None
		obj.save()

# ------------ Kontrol untuk menambah soal (admin) ---------------
def add_quest_tbl_0(request):
	# id_teach = request.POST.get('tch_id')
	id_course = request.POST.get('mapel')
	id_teach = models.course_data.objects.get(id = id_course).id_teacher
	id_admin = request.POST.get('id_admin')
	id_class = request.POST.get('id_class')

	add = models.quest_data(
			serial_quest = '-',
			id_teacher = id_teach,
			id_course = id_course,
			id_admin = id_admin,
			id_class = id_class
		)
	add.save()

def add_quest_tbl_1(request, filename, pss = 'admin', serial_quest = '-'):
	obj = ''
	if pss == 'admin':
		try:
			obj = models.quest_data.objects.get(
				id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id,
				serial_quest = serial_quest
				)
			fileName = filename.split('/')
			obj.serial_quest = fileName[1]
			obj.save()
			return ''
		except Exception as e:
			print(e,'\n')
			obj = models.quest_data.objects.filter(
				id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id,
				serial_quest = serial_quest
				)
			for x in range(len(obj)):
				obj[x].delete()
			os.remove(filename)
			return 'Error, data tidak ketemu'
		
	elif pss == 'teacher':
		try:
			obj = models.quest_data.objects.get(id_teacher = str(request.user), serial_quest = serial_quest)
			obj.serial_quest = filename.split('/')[1]
			obj.save()
			return ''
		except Exception as e:
			print(e)
			obj = models.quest_data.objects.filter(id_teacher = str(request.user), serial_quest = serial_quest)
			for x in range(len(obj)):
				obj[x].delete()
			os.remove(filename)
			return 'Error, data tidak ketemu'

# ---------- kontrol untuk menghapus soal ---------------------
def delete_for_quest(request, data, file_name):
	# 1. Menghapus file terlasi dengan XLS file
	# print('checkpoint 2 masuk del')
	for x in range(len(data)):
		for y in range(len(data[0])):
			url = 'media/'+str(data[x][y])
			try:
				os.remove(url)
			except Exception as e:
				print(e,'\n------ data tidak ada ------\n')

	# 2. Menghapus data di DB

	for_del = models.quest_data.objects.get(serial_quest = file_name, id = request.GET.get('del'))
	for_del = models.quest_data.objects.get(serial_quest = file_name)
	for_del.delete()
	# 3. Menghapus XLS file
	try:
		os.remove('media/'+file_name)
	except Exception as e:
		print(e,'\n---- data tidak ada------\n')

def del_quest_on_id(ID, by='teacher'):
	count = ''
	if by == 'teacher':
		count = models.quest_data.objects.filter(id_teacher = ID)
	elif by == 'class':
		# print(by,' Check kondisi')
		count = models.quest_data.objects.filter(id_class = ID)
	elif by == 'course':
		count = models.quest_data.objects.filter(id_course = ID)

	for x in range(len(count)):
		obj = models.quest_data.objects.get(id = count[x].id)
		# print('checkpoint obj get')
		# obj.delete()
		data, file_name = f_get.read_xls_storage('-', obj.id)
		delete_for_quest('-', data, file_name)

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
		for y in range(1,7):
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
					err += str(x+1)+' '
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
					err += str(x+1)+' '
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
					err += str(x+1)+' '
					break
			# elif y == 5 and data[x][y] != '':
			# 	id_tch = ''
			# 	try:
			# 		key = user_sec.user_second.objects.get(username = str(data[x][y])).no_induk
			# 		id_tch = user_sec.theachers_user.objects.get(no_induk = key).no_induk
			# 	except Exception as e:
			# 		confirm = e
				# if confirm == '':
				# 	tmp.append(id_tch)
				# else:
				# 	err = str(x+1)+' '
				# 	break
			elif y == 5 and data[x][y] != '':
				id_course = ''
				# print(str(data[x][y]))
				try:
					id_course = models.course_data.objects.get(course_name = str(data[x][y]))
				except Exception as e:
					confirm = e
				if confirm == '':
					tmp.append(id_course.id_teacher)
					tmp.append(id_course.id)
				else:
					err += str(x+1)+' '
					break
			elif y == 6 and data[x][y] != '':
				id_class = ''
				id_admin = ''
				token = ''
				state = 'deactive'
				for z in range(5):
					token += random.choice(string.ascii_letters)
				try:
					id_class = models.class_data.objects.get(class_name = str(data[x][y])).id
					id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id
				except Exception as e:
					confirm = e

				if confirm == '':
					tmp.append(id_class)
					tmp.append(id_admin)
					tmp.append(token)
					tmp.append(state)
				else:
					err += str(x+1)+' '
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

	id_course = models.course_data.objects.get(course_name = str(request.POST.get('course')))
	# mendapatkan ID teacher
	# key = user_sec.user_second.objects.get(username = str(request.POST.get('tch'))).no_induk
	# id_tch = user_sec.theachers_user.objects.get(no_induk = key).no_induk
	tmp.append(id_course.id_teacher)
	# mendapatkan ID course
	tmp.append(id_course.id)
	# mendapatkan ID class
	id_class = models.class_data.objects.get(class_name = str(request.POST.get('class'))).id
	tmp.append(id_class)
	# Mendapatkan ID admin
	id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id
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

	id_course = models.course_data.objects.get(course_name = str(request.POST.get('course')))
	# mendapatkan ID teacher
	# key = user_sec.user_second.objects.get(username = str(request.POST.get('tch'))).no_induk
	# id_tch = user_sec.theachers_user.objects.get(no_induk = key).no_induk
	tmp.append(id_course.id_teacher)
	# mendapatkan ID course
	tmp.append(id_course.id)
	# mendapatkan ID class
	id_class = models.class_data.objects.get(class_name = str(request.POST.get('class'))).id
	tmp.append(id_class)
	# Mendapatkan ID admin
	id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id
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

def del_schedule_on_id(ID, by='teacher'):
	count = ''
	if by == 'teacher':
		count = models.schedule_data.objects.filter(id_teacher = ID)
	elif by == 'class':
		count = models.schedule_data.objects.filter(id_class = ID)
	elif by == 'course':
		count = models.schedule_data.objects.filter(id_course = ID)

	for x in range(len(count)):
		obj = models.schedule_data.objects.get(id = count[x].id)
		obj.delete()

def del_schedule(request):
	ID = request.POST.get('id')
	delete = models.schedule_data.objects.get(id = ID)
	delete.delete()
	
# -------------- Kontroller halaman manage kelas (Buat, buat automatis, delete, edut) ------------
def add_class_manual(request, pss = 'admin'):
	err = ''
	name = request.POST.get('name')
	id_tch = ''
	id_admin = ''
	if pss == 'admin':
		id_admin = user_sec.user_second.objects.get(no_induk = request.POST.get('id_admin')).id
		id_tch = request.POST.get('id_tch')
		check = models.class_data.objects.filter(class_name = name, id_admin = id_admin)
		if len(check) != 0:
			err = 'Nama kelas sudah ada'
	elif pss == 'teacher':
		id_tch = str(request.user)
		try:
			id_admin = user_sec.user_second.objects.get(
				no_induk = user_sec.theachers_user.objects.get(
					no_induk = id_tch).admin_id).id

			check = models.class_data.objects.filter(class_name = name, id_admin = id_admin)
			if len(check) != 0:
				err = 'Nama kelas sudah ada'

		except Exception as e:
			print(e)
			err = 'Admin ID belum di set'
	try:
		if err == '':
			add = models.class_data(
				class_name = name,
				id_teacher = id_tch,
				id_admin = id_admin
				)
			add.save()
	except Exception as e:
		print(e)
		err = 'Data gagal ditambahkan'
	return err

def add_class_auto(request, data, pss = 'admin'):
	msg = ''
	for x in range(len(data)):
		err = ''
		class_name = data[x][1]
		id_admin = ''
		id_tch = ''
		if pss == 'admin':
			id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id
			try:
				id_tch = user_sec.user_second.objects.get(
					username = data[x][2], status='guru').no_induk
				check = models.class_data.objects.filter(class_name = class_name, id_admin = id_admin)
				if len(check) != 0:
					err = 'Nama kelas sudah ada'
			except Exception as e:
				err += str(x+1)+' '
		elif pss == 'teacher':
			id_tch = str(request.user)
			try:
				id_admin = user_sec.user_second.objects.get(
					no_induk = user_sec.theachers_user.objects.get(
						no_induk = id_tch).admin_id).id

				check = models.class_data.objects.filter(class_name = class_name, id_admin = id_admin)
				if len(check) != 0:
					err += 'Nama kelas sudah ada'

			except Exception as e:
				print(e)
				err += 'Admin ID belum di set'
			# print(err,'\n')
		if class_name != '' and err == '':
			add = models.class_data(
				class_name = class_name,
				id_teacher = id_tch,
				id_admin = id_admin
				)
			add.save()
		msg += err
	# print(msg)
	return msg	

def edit_class(request, pss='admin'):
	err = ''

	ID = request.POST.get('id')
	name = request.POST.get('name')
	id_tch = ''
	id_admin = ''
	if pss == 'admin':
		id_admin = user_sec.user_second.objects.get(no_induk = request.POST.get('id_admin')).id
		id_tch = request.POST.get('id_tch')
		check = models.class_data.objects.filter(class_name = name, id_admin = id_admin)
		if len(check) != 0:
			err = 'Nama kelas sudah ada'
	elif pss == 'teacher':
		id_tch = str(str(request.user))
		try:
			id_admin = user_sec.user_second.objects.get(
				no_induk = user_sec.theachers_user.objects.get(
					no_induk = id_tch).admin_id).id

			check = models.class_data.objects.filter(class_name = name, id_admin = id_admin)
			if len(check) != 0:
				err = 'Nama kelas sudah ada'

		except Exception as e:
			print(e)
			err = 'Admin ID belum di set'

	try:
		if err == '':
			edit = models.class_data.objects.get(id = ID)
			edit.class_name = name
			edit.id_teacher = id_tch
			edit.id_admin = id_admin
			edit.save()
	except Exception as e:
		print(e)
		err = 'Data gagal ditambahkan'

	return err

def del_class_on_id(tch_no_induk_ID):
	count = models.class_data.objects.filter(id_teacher = tch_no_induk_ID)
	for x in range(len(count)):
		obj = models.class_data.objects.get(id = count[x].id)
		del_schedule_on_id(count[x].id, by='class')
		del_quest_on_id(count[x].id, by='class')
		obj.delete()

def del_class(request):
	delete = models.class_data.objects.get(id = request.POST.get('id'))
	delete.delete()
	del_schedule_on_id(request.POST.get('id'), by='class')
	del_quest_on_id(request.POST.get('id'), by='class')
	change_tch_id_stdn_on_id(request.POST.get('id'), by='class')

# ---------- Kontroller managemen data kelas CRUD ---------------------

def add_crs_manual(request, pss='admin'):
	err = ''
	name = request.POST.get('name')
	id_tch = ''
	id_admin = ''

	if pss == 'admin':
		id_tch = request.POST.get('id_tch')
		id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id
		check = models.class_data.objects.filter(class_name = name, id_admin = id_admin)
		if len(check) != 0:
			err = 'Nama mapel sudah ada'
	elif pss == 'teacher':
		id_tch = str(request.user)
		try:
			id_admin = user_sec.user_second.objects.get(
				no_induk = user_sec.theachers_user.objects.get(
					no_induk = id_tch).admin_id
				).id
			check = models.course_data.objects.filter(course_name = name, id_admin = id_admin)
			if len(check) != 0:
				err = 'Data mapel sudah terdaftar'
		except Exception as e:
			print(e)
			err = 'Admin ID belum di set'
	
	if err == '':
		try:
			add = models.course_data(
				course_name = name,
				id_teacher = id_tch,
				id_admin = id_admin
				)
			add.save()
		except Exception as e:
			print (e)
			err = 'Data gagal ditambahkkan'

	return err

def add_crs_auto(request, data, pss = 'admin'):
	msg = ''
	for x in range(len(data)):
		err = ''
		name = data[x][1]
		id_tch = ''
		id_admin = ''

		if pss == 'admin':
			id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id
			try:
				id_tch = user_sec.user_second.objects.get(username = data[x][2]).no_induk
				check = models.class_data.objects.filter(class_name = name, id_admin = id_admin)
				if len(check) != 0:
					err = 'Nama mapel sudah ada'
			except Exception as e:
				print(e)
				err += str(x+1)+' '
		elif pss == 'teacher':
			id_tch = str(str(request.user))
			try:
				id_admin = user_sec.user_second.objects.get(
					no_induk = user_sec.theachers_user.objects.get(
						no_induk = id_tch
						).admin_id
					).id
				check = models.course_data.objects.filter(course_name = name, id_admin = id_admin)
				if len(check) != 0:
					err += 'Data mapel '+str(x+1)+' sudah terdaftar'
			except Exception as e:
				print(e)
				err = 'Admin ID belum di set'

		if err == '' and name != '':
			try:
				add = models.course_data(
					course_name = name,
					id_teacher = id_tch,
					id_admin = id_admin
					)
				add.save()
			except Exception as e:
				print(e)
				err += str(x+1)+' '

		msg += err
	return msg

def edit_crs(request, pss='admin'):
	err = ''
	ID = request.POST.get('id')
	name = request.POST.get('name')
	id_tch = ''
	id_admin = ''
	print(name)
	if pss == 'admin':
		id_tch = request.POST.get('id_tch')
		id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id
		check = models.class_data.objects.filter(class_name = name, id_admin = id_admin)
		if len(check) != 0:
			err = 'Nama mapel sudah ada'
	elif pss == 'teacher':
		id_tch = str(request.user)
		try:
			id_admin = user_sec.user_second.objects.get(
				no_induk = user_sec.theachers_user.objects.get(
					no_induk = id_tch).admin_id
				).id
			check = models.course_data.objects.filter(course_name = name, id_admin = id_admin)
			if len(check) != 0:
				err = 'Data mapel sudah terdaftar'
		except Exception as e:
			print(e)
			err = 'Admin ID belum di set'
	
	try:
		if err == '':
			edit = models.course_data.objects.get(id = ID)
			edit.course_name = name
			edit.id_teacher = id_tch
			edit.save()
	except Exception as e:
		print(e)
		err += 'Data gagal diubah'

	return err

def del_course_on_id(tch_no_induk_ID):
	count = models.course_data.objects.filter(id_teacher = tch_no_induk_ID)
	for x in range(len(count)):
		obj = models.course_data.objects.get(id = count[x].id)
		del_schedule_on_id(count[x].id, by='course')
		del_quest_on_id(count[x].id, by='course')
		obj.delete()

def del_course(request):
	obj = models.course_data.objects.get(id = request.POST.get('id'))
	obj.delete()
	del_schedule_on_id(request.POST.get('id'), by='course')
	del_quest_on_id(request.POST.get('id'), by='course')

# ------ Fungsi kontroller menghapus resut test -------------------
def del_result_test(request):
	delete = models.result_test.objects.get(id = request.POST.get('delete'))
	delete.delete()


# ------ Kontroller mengahpus data guru dan siswa -------------------
def del_tch_stdn(request, del_for = 'teacher'):
	# Catatan : JIka data guru (Main) disini di hapus, maka semua data yang terkait harus dihapus
	msg = ''
	id_main = request.POST.get('id')
	id_sec = request.POST.get('id2')
	id_spec = request.POST.get('id3')

	obj_main = User.objects.get(id = id_main)
	obj_sec = user_sec.user_second.objects.get(id = id_sec)
	obj_spec = ''
	if del_for == 'teacher':
		obj_spec = user_sec.theachers_user.objects.get(id = id_spec)
		# Proses penghapusan data terkait (FK) dari data guru
		# Meliputi data kelas, siswa (untuk siswa id guru di set null / kosong), 
		# mapel, soal, dan jadwal
		del_class_on_id(obj_sec.no_induk)
		del_course_on_id(obj_sec.no_induk)
		# del_quest_on_id(obj_sec.no_induk)
		# del_schedule_on_id(obj_sec.no_induk)
		change_tch_id_stdn_on_id(obj_sec.no_induk)
		
	elif del_for == 'student':
		obj_spec = user_sec.students_user.objects.get(id = id_spec)

	if obj_sec.profile != 'default.jpg':
		try:
			os.remove('media/'+user_sec.user_second.objects.get(id = id_sec).profile)
		except Exception as e:
			print(e, 'Foto gagal dihapus')

	try:
		obj_main.delete()
		obj_sec.delete()
		obj_spec.delete()
	except Exception as e:
		print(e)
		msg = 'Data gagal dihapus'
	return msg

def create_eval_data(request, use_for = 'admin'):
	# memastikan satus dan tanggal evaluasi
	all_eval = f_get.view_eval_data(request, view_for = use_for)
	end_eval = ''
	if len(all_eval) != 0:
		end_eval = all_eval[len(all_eval)-1][0]
	else:
		end_eval = datetime.now().date()

	m_y = end_eval
	last_date = datetime(m_y.year, m_y.month, 1)
	m_y = datetime.now().date()
	this_date = datetime(m_y.year, m_y.month, 1)

	targets = []
	res_test = ''

	if use_for == 'admin':
		all_tch = user_sec.theachers_user.objects.filter(admin_id = request.user)
		for x in range(len(all_tch)):
			targets += models.evaluation_tch.objects.filter(id_teacher = all_tch[x].no_induk, state = 'non')
		res_test = f_get.viewResultTest(request, request.user, has_eval='non' ,admin = True, students = False)
	elif use_for == 'teacher':
		targets = models.evaluation_tch.objects.filter(id_teacher = request.user, state = 'non')
		res_test = f_get.viewResultTest(request, request.user, has_eval='non' ,teach = True, students = False)

	# Ambil distance berdsarkan bulan dan uat dimensi array berdasarkan 
	# jumlah bulan
	print(len(all_eval))
	if len(all_eval) == 0:
		try:
			last_date = datetime(targets[0].date.year, targets[0].date.month, 1)
		except Exception as e:
			print(e)
		# print(last_date)
	
	if last_date != this_date and len(all_eval) != 0:
		if last_date.month + 1 > 12:
			last_date = datetime(last_date.year+1, 1, 1)
		else:
			last_date = datetime(last_date.year, last_date.month+1, 1)

	all_eval.clear()

	distance = abs(this_date - last_date).days
	distance = round(distance / 30)
	# print(distance)
	fix_arr = [[]*distance]
	for x in range(len(targets)):
		change = models.evaluation_tch.objects.get(id = targets[x].id)
		change.state = 'evaluated'
		change.save()
		for y in range(distance):
			if last_date.month + y > 12:
				month = (last_date.month+y) - 12
				if targets[x].date >= datetime(last_date.year+1, month, 1).date() and targets[x].date <= datetime(last_date.year+1, month, 31).date():
					tmp = [targets[x].id_teacher, targets[x].date, 'result', targets[x].cat_1, targets[x].cat_2, targets[x].cat_3, targets[x].cat_4, targets[x].cat_5, targets[x].cat_6, targets[x].cat_7, ctargets[x].at_8, targets[x].cat_9, targets[x].cat_10, targets[x].cat_11]
					fix_arr[y].append(tmp)
					print(fix_arr[y])
			else :
				if targets[x].date >= datetime(last_date.year, last_date.month+y, 1).date() and targets[x].date <= datetime(last_date.year, last_date.month+y, 31).date():
					tmp = [targets[x].id_teacher, targets[x].date, 'result', targets[x].cat_1, targets[x].cat_2, targets[x].cat_3, targets[x].cat_4, targets[x].cat_5, targets[x].cat_6, targets[x].cat_7, targets[x].cat_8, targets[x].cat_9, targets[x].cat_10, targets[x].cat_11]
					fix_arr[y].append(tmp)
				print("UwU",targets[x].date, datetime(last_date.year, last_date.month+y, 1).date(), datetime(last_date.year, last_date.month+y, 28).date())

	stdn_test = [[]*distance]
	
	for x in range(len(res_test)):
		for y in range(distance):
			if last_date.month + y > 12:
				month = (last_date.month+y) - 12
				if datetime.strptime(res_test[x][0], '%Y-%m-%d').date() >= datetime(last_date.year+1, month, 1).date() and datetime.strptime(res_test[x][0], '%Y-%m-%d').date() <= datetime(last_date.year+1, month, 31).date():
					tmp = [res_test[x][1], res_test[x][2], res_test[x][3], res_test[x][8]]
					stdn_test[y].append(tmp)
			else :
				if datetime.strptime(res_test[x][0], '%Y-%m-%d').date() >= datetime(last_date.year, last_date.month+y, 1).date() and datetime.strptime(res_test[x][0], '%Y-%m-%d').date() <= datetime(last_date.year, last_date.month+y, 31).date():
					tmp = [res_test[x][1], res_test[x][2], res_test[x][3], res_test[x][8]]
					stdn_test[y].append(tmp)
		
	for x in range(len(fix_arr)):
		res_eval = evaluator.teach_evaluator(fix_arr[x], stdn_test[x])
		# print("Hasil eval sistem : \n")
		# print(res_eval)
		# print(fix_arr[x])
		# print(targets)
		# Input data ke DB
		for y in range(len(res_eval)):
			add = models.evaluation_tch(
				date = res_eval[y][1],
				cat_1 = res_eval[y][3],
				cat_2 = res_eval[y][4],
				cat_3 = res_eval[y][5],
				cat_4 = res_eval[y][6],
				cat_5 = res_eval[y][7],
				cat_6 = res_eval[y][8],
				cat_7 = res_eval[y][9],
				cat_8 = res_eval[y][10],
				cat_9 = res_eval[y][11],
				cat_10 = res_eval[y][12],
				cat_11 = res_eval[y][13],
				cat_spec = res_eval[y][14],
				score = res_eval[y][15],
				state = res_eval[y][2],
				id_teacher = res_eval[y][0]
				)
			add.save()

def create_eval_stdn(request, use_for = 'admin'):
	all_eval = []
	if use_for == 'admin':
		all_tch = user_sec.theachers_user.objects.filter(admin_id = request.user)
		for x in range(len(all_tch)):
			obj = user_sec.students_user.objects.filter(guru_id = all_tch[x].no_induk)
			for y in range(len(obj)):
				try:
					all_eval.append(models.evaluation_stdn.objects.get(id_students = obj[x].no_induk))
				except Exception as e:
					print(e)
	elif use_for == 'teacher':
		all_stdn = user_sec.students_user.objects.get(guru_id = request.user)
		for x in range(len(all_stdn)):
			try:
				all_eval.append(models.evaluation_stdn.objects.get(id_students = all_stdn[x].no_induk))
			except Exception as e:
				print(e)

	end_eval = ''
	if len(all_eval) != 0:
		end_eval = all_eval[len(all_eval)-1].date
	else:
		end_eval = datetime.now().date()
	last_date = datetime(end_eval.year, end_eval.month, 1)
	end_eval = datetime.now().date()
	this_date = datetime(end_eval.year, end_eval.month, 1)

	res_test = ''

	if use_for == 'admin':
		res_test = f_get.viewResultTest(request, request.user, has_eval = 'non', admin = True, students = False)
	elif use_for == 'teacher':
		res_test = f_get.viewResultTest(request, request.user, has_eval = 'non', teach = True, students = False)

	if len(all_eval) == 0:
		try:
			dtime = datetime.strptime(res_test[0][0], '%Y-%m-%d')
			last_date = datetime(dtime.year, dtime.month, 1)
		except Exception as e:
			print(e)

	if last_date != this_date and len(all_eval) != 0:
		if last_date.month + 1 > 12:
			last_date = datetime(last_date.year+1, 1, 1)
		else:
			last_date = datetime(last_date.year, last_date.month+1, 1)

	all_eval.clear()

	distance = abs(this_date - last_date).days
	distance = round(distance / 30)

	stdn_test = [[]*distance]
	
	for x in range(len(res_test)):
		for y in range(distance):
			change = models.result_test.objects.get(id = res_test[x][9])
			change.state_eval = 'evaluated'
			change.save()
			if last_date.month + y > 12:
				month = (last_date.month+y) - 12
				if datetime.strptime(res_test[x][0], '%Y-%m-%d').date() >= datetime(last_date.year+1, month, 1).date() and datetime.strptime(res_test[x][0], '%Y-%m-%d').date() <= datetime(last_date.year+1, month, 31).date():
					tmp = [res_test[x][1], res_test[x][2], res_test[x][3], res_test[x][8], res_test[x][0]]
					stdn_test[y].append(tmp)
			else :
				if datetime.strptime(res_test[x][0], '%Y-%m-%d').date() >= datetime(last_date.year, last_date.month+y, 1).date() and datetime.strptime(res_test[x][0], '%Y-%m-%d').date() <= datetime(last_date.year, last_date.month+y, 31).date():
					tmp = [res_test[x][1], res_test[x][2], res_test[x][3], res_test[x][8], res_test[x][0]]
					stdn_test[y].append(tmp)
	# print(stdn_test[0])
	for x in range(len(stdn_test)):

		res_eval = evaluator.stdn_evaluator(stdn_test[x])

		for y in range(len(res_eval)):

			quote = ''
			if res_eval[y][1] > res_eval[y][2]:
				quote = 'Pertahankan dan tingkatkan pencapaianmu'
			else:
				quote = 'Belajarlah lebih rajin lagi'

			add = models.evaluation_stdn(
				date = res_eval[y][3],
				quote = quote,
				min_score = res_eval[y][2],
				max_score = res_eval[y][1],
				id_students = res_eval[y][0]
				)
			add.save()

def create_survey(request, ID_Result_Test):
	obj = models.result_test.objects.get(id = ID_Result_Test)
	obj.survey = 'filled'
	obj.save()

	add = models.evaluation_tch(
		date = obj.date,
		cat_1 = request.POST.get('cat1'),
		cat_2 = request.POST.get('cat2'),
		cat_3 = request.POST.get('cat3'),
		cat_4 = request.POST.get('cat4'),
		cat_5 = request.POST.get('cat5'),
		cat_6 = request.POST.get('cat6'),
		cat_7 = request.POST.get('cat7'),
		cat_8 = request.POST.get('cat8'),
		cat_9 = request.POST.get('cat9'),
		cat_10 = request.POST.get('cat10'),
		cat_11 = request.POST.get('cat11'),
		cat_spec = 0,
		score = 0,
		state = 'non',
		id_teacher = obj.id_teacher
		)

	add.save()


def control_survey(request):
	res_test = models.result_test.objects.filter(id_students = request.user, survey = 'non')

	if len(res_test) == 0:
		if request.GET.get('single') == None:
			return '/view_result_test?single=1'
		else:
			return '-'
	else:
		if request.GET.get('code') == None:
			return '/survey?code='+str(res_test[0].id)
		else:
			return '-'



