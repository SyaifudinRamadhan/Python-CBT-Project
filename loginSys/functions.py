# def cetak():
# 	print("hello worl")
from . import models
from adminSide import models as models_2
from django.contrib.auth.models import User
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login as sys_login, logout, authenticate, models as userModel
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# from adminSide import models as modelsAdmin

# Fungsi ini mengembalikan text berupa nama dikumen yang dituju
def loginCheck(request, state = 'siswa'):
	userlogged = str(request.user)

	print('\n', 'test in 1','\n')

	if userlogged != 'AnonymousUser': 
		userSec = models.user_second.objects.filter(no_induk = userlogged)
		print('\n', 'test in 2','\n')
		if state != userSec[0].status:
			print('\n', 'test in 3','\n')
			if userSec[0].status == 'siswa':

				return '/stdn_auth'

			elif userSec[0].status == 'guru':
				return '/panel_sec'

			else :
				return '/panel'
		else :
			print('\n', 'test in 3 else','\n')
			return 'None'

	else :
		print('\n', 'test in 2 else','\n')
		return '/oAuth'

# Fungsi ini mengembalikan text berupa nama dikumen yang dituju
def loginCore(request, no_induk, pwd):
	authen = authenticate(request, username = no_induk, password = pwd)

	print(authen)
	print('\n\n')

	if authen != None:
		sys_login(request, authen)
		print(request.user, authen)
		print('login benar')

		userSec = models.user_second.objects.filter(no_induk = no_induk)
		print(type(userSec[0].status))
		# Untuk di redirect
		if userSec[0].status == 'siswa':
			print('\nAnda terdaftar sebagai siswa')
			return '/stdn_auth'		
		elif userSec[0].status == 'guru':
			print('\nAnda terdaftar sebagai Guru')
			return '/panel_sec'	
		else :
			print('\nAnda terdaftar sebagai admin')
			return '/panel'	

	else :
		print(request.user)
		print('login salah')
		# untuk di render
		return 'login.html'

def getState (userlogged):

	userSec = models.user_second.objects.filter(no_induk = userlogged)
	typeUser = userSec[0].status

	return typeUser

def getName (userlogged):

	userSec = models.user_second.objects.filter(no_induk = userlogged)
	name = userSec[0].username

	return name

def uploadImg (request, editSec, confirm) :
	# ------ Buat jadi function -----------
	fileState = False
	
	fileName = ''
	if len(request.FILES) != 0 :
		if editSec.profile != '' and editSec.profile != 'default.jpg':
			print(' g kosong')
			# Menghapus file lama
			dirName = 'media/'+editSec.profile
			try:
				os.remove(dirName)
			except Exception as e:
				confirm.append(e)

		file = request.FILES['photo']
		fileState = True
		print(request.method)
		print('\n', file.name)
		print('\n', len(request.FILES))

		fs = FileSystemStorage()
		file_upload = fs.save(file.name, file)

		url = fs.url(file_upload)
		fileName = url.split('/')
		print(fileName[2])
		# -----------------------------------------
		return fileState, fileName
	else :
		return fileState, fileName

def passConfirm (request, l_pass, new_pass, confirm):
	# ------------------- jadikan function ----------------------
	if l_pass != '' and new_pass != '' :
		auth = authenticate(request, username = request.user, password = l_pass)
		if auth != None :
			return True
		else :
			confirm.append('Konfirmasi password lama salah')
			print(confirm)
			return False
	elif (l_pass != '' and new_pass == '') or (l_pass == '' and new_pass != '') :
		confirm.append('Field password lama dan baru harus diisi')
		print(confirm)
		return False
	# -------------------------------------------------------------

# ------ function ini untuk mengedit profil pengguna (umum) ----------
def editStdAcc (request, pss = 'student', use = 'single'):
	# Untuk yanga admin, pss bisa diisi kong atau 'admin' 
	# sebab admin hanya menggunakan main dan user_second saja
	username = request.POST['username']
	# no induk untuk guru dan admin wajib hidden
	no_induk = request.POST['noinduk']
	email = request.POST['email']
	fname = request.POST['fname']
	lname = request.POST['lname']
	# ini khusus untuk student
	teach_id = ''
	class_id = ''
	# dua ini khusus untuk teacher
	id_admin = ''
	agency_0 = ''
	# ---------------------------
	l_pass = request.POST['pwd0']
	new_pass = request.POST['pwd']
	confirm = []
	editMain = ''
	editSec = ''
	if use == 'single':
		editMain = userModel.User.objects.get(username = request.user)
		editSec = models.user_second.objects.get(no_induk = request.user)
	elif use == 'multi':
		editMain = userModel.User.objects.get(id = request.POST.get('id'))
		editSec = models.user_second.objects.get(id = request.POST.get('id2'))
	editStdn = ''
	editTch = ''

	fileInf, nameFile = uploadImg(request, editSec, confirm)
	# Untuk upload Foto profil
	if fileInf == True :
		editSec.profile = nameFile[2]
	# Untuk ganti password
	check = passConfirm(request, l_pass, new_pass, confirm)
	if check  == True :
		editMain.set_password(new_pass)
	# Mengupdate data di db
	# Mengubah data user_main
	editMain.username = no_induk
	editMain.first_name = fname
	editMain.last_name = lname
	editMain.email = email
	# Password sudah di edit di atas
	# Mengubah data sec_user
	editSec.no_induk = no_induk
	editSec.username = username
	
	if pss == 'student':
		teach_id = request.POST['guru_id']
		if use == 'single':
			editStdn = models.students_user.objects.get(no_induk = request.user)
		elif use == 'multi':
			editStdn = models.students_user.objects.get(id = request.POST.get('id3'))
		class_id = request.POST.get('class')
		# Profile sudah diupdate di atas
		# edit stdn user
		editStdn.no_induk = no_induk
		editStdn.guru_id = teach_id
		editStdn.id_class = class_id
	elif pss == 'teacher':
		id_admin = request.POST.get('id_admin')
		agency_0 = request.POST.get('agency')
		if use == 'single':
			editTch = models.theachers_user.objects.get(no_induk = request.user)
		elif use == 'multi':
			editTch = models.theachers_user.objects.get(id = request.POST.get('id3'))
			# print('id ketiga: ',request.POST.get('id3'))
		# no induk wwajib tetap
		editTch.admin_id = id_admin
		editTch.agency = agency_0

	try:
		editMain.save()
		editSec.save()
		if pss == 'student':
			editStdn.save()
		elif pss == 'teacher':
			editTch.save()
	except Exception as e:
		print(e)
		confirm.append('Gagal menyimpan perubahan')

	if check == True :
		auth = authenticate(request, username = no_induk, password = new_pass)
		sys_login(request, auth)
	
	print(confirm)
	return confirm
	
def set_resTest (request, model_db):
	date = datetime.now().date()
	res = 0
	statuses = 'ongoing'
	course = '' #ini = id_quest
	id_teach = ''
	id_stdn = request.user
	id_admin = ''

	confirm = ''
	
	if request.method == 'POST' :
		token = request.POST['token']
		
		try:
			schedule = model_db.schedule_data.objects.get(token = token)
		except Exception as e:
			print('\n',e,'\n')
			confirm = 'Error, Token tidak tersedia.'

		if confirm == '' :
			# print(schedule.state,'\n')
			if schedule.state == 'active' :
				course = schedule.id_course
				id_teach = schedule.id_teacher
				id_admin = schedule.id_admin
				
				dataTest = model_db.result_test(date = date, result = res, state_test = statuses, token = token ,id_quest = course, id_students = id_stdn, id_admin = id_admin, id_teacher = id_teach)
				dataTest.save()
			else:
				print('\n','Jadwal tidak aktif')
		else:
			print('\n',confirm)


def change_resTest (request, model_db, value):
	confirm = True
	try:
		User_Test = model_db.result_test.objects.get(id_students = request.user, state_test = 'ongoing')
	except Exception as e:
		print(e)
		confirm = False

	if confirm == True :
		User_Test.result = value
		User_Test.state_test = 'Finished'
		User_Test.save()
		return confirm
	else :
		return confirm
	
# -------- Umum untuk tambah data (guru dan siswa) admin dan teacher page ------------------------- 
# 
def main_adding(no_induk, email, password, first_name1, last_name1, username, status, msg, agency='', admin_id='', tch_id = '', class_id='', add_for='teacher'):
	try:
		# Input daya ke database user utama
		usr = User.objects.create_user(no_induk, email, password)
		usr.first_name = first_name1
		usr.last_name = last_name1
		usr.save()
		# Extend dari user utma untuk semua user
		usr_sec = models.user_second(no_induk = no_induk, username = username, status = status, profile = 'default.jpg')
		usr_sec.save()
		# Extend user secunder setiap status
		if add_for == 'teacher':
			print('masuk input khusus 1')
			usr_sec_tch = models.theachers_user(no_induk = no_induk, agency = agency, admin_id = admin_id)
			usr_sec_tch.save()
		elif add_for == 'student':
			usr_sec_std = models.students_user(no_induk = no_induk, guru_id = tch_id, id_class = class_id)
			usr_sec_std.save()
	except Exception as e:
		msg.append('Gagal mendaftarkan '+add_for)
		print(e)

def add_acc_manual(request, add_for = 'teacher'):
	msg = []
	if request.method == "POST":
		# utama user model
		no_induk = request.POST['nrp']
		password = request.POST['pass']
		first_name1 = request.POST['fname']
		last_name1 = request.POST['lname']
		email = request.POST['email']
		# secindary user model
		username = request.POST['name']
		status = 'guru'
		# profile = 'default.jpg'
		# teachers_user model
		if add_for == 'teacher':
			agency = request.POST['agc']
			admin_id = models.user_second.objects.get(no_induk = request.user).no_induk

			# Insert ke DB
			main_adding(no_induk, email, password, first_name1, last_name1, username, status, msg, agency=agency, admin_id=admin_id)
		elif add_for == 'student':
			status = 'siswa'
			teach_id = request.POST['guru_id']
			class_id = request.POST.get('class')

			main_adding(no_induk, email, password, first_name1, last_name1, username, status, msg, tch_id=teach_id, class_id=class_id, add_for=add_for)
	return msg

def add_acc_auto(request, data_list, add_for = 'teacher', pss='admin'):
	err = ''
	msg = []
	for x in range(len(data_list)):
		tmp = []
		confirm = ''
		for y in range(1,len(data_list[x])):

			if data_list[x][y] == '':
				confirm = 'Terdeteksi inputan yang kosong'
				err += str(x+1)+' '
				break
			if y == 6:
				try:
				    validate_email(data_list[x][y])
				except ValidationError as e:
				    # print("bad email, details:", e)
				    confirm = 'Email format salah'
				    err += str(x+1)+' '
				    break
				else:
				    print("good email")
				    tmp.append(str(data_list[x][y]))
			else:
				tmp.append(str(data_list[x][y]))
				print(y)

		if confirm == '':
			if add_for == 'teacher':
				print(tmp)
				admin_id = models.user_second.objects.get(no_induk = request.user).no_induk
				status = 'guru'
				main_adding(
					tmp[0], tmp[5], tmp[2], tmp[3], 
					tmp[4], tmp[1], status, msg, agency=tmp[6], 
					admin_id=admin_id)
			elif add_for == 'student':
				# Periksa lagi. banyak kekurangan
				# admin_id = models.user_second.objects.get(no_induk = request.user).id
				status = 'siswa'
				tch_id = ''
				class_id = ''
				try:
					tch_id = models.user_second.objects.get(username = tmp[6])
					if pss == 'teacher':
						tch_id = models.user_second.objects.get(no_induk = request.user)
					class_id = models_2.class_data.objects.get(class_name = tmp[7], 
						id_admin = models.user_second.objects.get(
							no_induk = models.theachers_user.objects.get(
								no_induk = tch_id.no_induk).admin_id).id)
					print(models.theachers_user.objects.get(no_induk = tch_id.no_induk).admin_id)
					main_adding(
						tmp[0], tmp[5], tmp[2], tmp[3], 
						tmp[4], tmp[1], status, msg, tch_id=tch_id.no_induk, 
						class_id=class_id.id, add_for='student')
				except Exception as e:
					print(e)
					err+=str(x+1)+' '
	print(msg)
	return msg, err


