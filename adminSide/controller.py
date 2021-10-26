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
<<<<<<< HEAD
			obj = models.quest_data.objects.filter(
				id_admin = user_sec.user_second.objects.get(no_induk = str(request.user)).id,
				serial_quest = serial_quest
				)
			for x in range(len(obj)):
				obj[x].delete()
=======
>>>>>>> c5919df8a57d32ded3055e10ae6ae6079ee65ee5
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
<<<<<<< HEAD
			obj = models.quest_data.objects.filter(id_teacher = str(request.user), serial_quest = serial_quest)
			for x in range(len(obj)):
				obj[x].delete()
=======
>>>>>>> c5919df8a57d32ded3055e10ae6ae6079ee65ee5
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
<<<<<<< HEAD
	for_del = models.quest_data.objects.get(serial_quest = file_name, id = request.GET.get('del'))
=======
	for_del = models.quest_data.objects.get(serial_quest = file_name)
>>>>>>> c5919df8a57d32ded3055e10ae6ae6079ee65ee5
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
