from django.shortcuts import render, redirect
from . import models
from . import functions
from django.contrib.auth.models import User
from django.contrib.auth import logout

# Create your views here.

def singUp (request):
	if request.method == "POST":
		username = request.POST['name']
		password = request.POST['pass']
		first_name1 = request.POST['fname']
		last_name1 = request.POST['lname']
		email = request.POST['email']
		kode_guru = request.POST['type']
		no_induk = request.POST['nrp']
		status = ''

		if kode_guru != '':
			if kode_guru == 'admin' :
				status = 'admin'
			else :
				status = 'siswa'
		else :
			status = 'guru'

		print(status)

		try:
			# Input daya ke database user utama
			usr = User.objects.create_user(no_induk, email, password)
			usr.first_name = first_name1
			usr.last_name = last_name1
			usr.save()
		except Exception as e:
			context = {
				'error_message':[
				'Registrasi GAGAL !!!', 
				e,
				'No Induk / NRP / NIS sudah terdaftar'
				],
			}
			return render(request, 'registration.html', context)
		# Extend dari user utma untuk semua user
		usr_sec = models.user_second(no_induk = no_induk, username = username, status = status, profile = 'default.jpg')
		usr_sec.save()
		# Extend user secunder setiap status
		if status == 'siswa':
			usr_sec_std = models.students_user(no_induk = no_induk, guru_id = kode_guru)
			usr_sec_std.save()
		elif status == 'guru':
			usr_sec_tch = models.theachers_user(no_induk = no_induk)
			usr_sec_tch.save()

		# doc adalah hasil return function berupa nama dokumen tujuan
		doc = functions.loginCore(request, no_induk, password)
		if doc == 'login.html' :
			context = {
				'note':'Login gagal'
			}
			return render(request, doc, context)
		else :
			return redirect(doc)

	return render(request, 'registration.html')

# Mengatur login system dan pmebagian akses
def login(request):

	if request.method == "POST":
		no_induk = request.POST['username']
		pwd = request.POST['password']
		
		# doc adalah nama dokkumen hasil return function yang akan dituju
		doc = functions.loginCore(request, no_induk, pwd)
		if doc == 'login.html' :
			context = {
				'note':'Login gagal'
			}
			return render(request, doc, context)
		else :
			return redirect(doc)

	return render(request, 'login.html') 

def log_out(request):

	if request.user != 'AnonymousUser' :
		logout(request)
		return redirect('/oAuth')
	else :
		return redirect('/oAuth')
