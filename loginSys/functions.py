# def cetak():
# 	print("hello worl")
from . import models
import os
from django.shortcuts import render, redirect
from django.contrib.auth import login as sys_login, logout, authenticate, models as userModel
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from datetime import datetime
# from adminSide import models as modelsAdmin

# Fungsi ini mengembalikan text berupa nama dikumen yang dituju
def loginCheck(request):
	userlogged = str(request.user)

	print('\n', 'test in 1','\n')

	if userlogged != 'AnonymousUser': 
		userSec = models.user_second.objects.filter(no_induk = userlogged)
		state = userSec[0].status
		print('\n', 'test in 2','\n')
		if state != userSec[0].status:
			print('\n', 'test in 3','\n')
			if userSec[0].status == 'siswa':

				return '/stdn_auth'

			elif userSec[0].status == 'guru':
				return '/teach_auth'

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
			return '/teach_auth'	
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

def editStdAcc (request):

	username = request.POST['username']
	no_induk = request.POST['noinduk']
	email = request.POST['email']
	fname = request.POST['fname']
	lname = request.POST['lname']
	teach_id = request.POST['guru_id']
	l_pass = request.POST['pwd0']
	new_pass = request.POST['pwd']
	confirm = []
	
	editMain = userModel.User.objects.get(username = request.user)
	editSec = models.user_second.objects.get(no_induk = request.user)
	editStdn = models.students_user.objects.get(no_induk = request.user)

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
	# Profile sudah diupdate di atas
	# edit stdn user
	editStdn.no_induk = no_induk
	editStdn.guru_id = teach_id

	try:
		editMain.save()
		editSec.save()
		editStdn.save()
	except Exception as e:
		confirm.append(e)

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
			else:
				print('\n','Jadwal tidak aktif')
		else:
			print('\n',confirm)

	dataTest = model_db.result_test(date = date, result = res, state_test = statuses, token = token ,id_quest = course, id_students = id_stdn, id_admin = id_admin, id_teacher = id_teach)
	dataTest.save()

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
	
		




