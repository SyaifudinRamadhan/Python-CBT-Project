import os
from django.core.files.storage import FileSystemStorage

class data_quest:
	listData = []
	params_index = 0

	# Untuk edit data soal
	def set_data_quest (self, data):
		self.listData = data

	def upload_files(self, files):
		fs = FileSystemStorage()
		try:
			file_upload = fs.save(files.name, files)

			url = fs.url(file_upload)
			fileName = url.split('/')
			return fileName[2]
		except Exception as e:
			return ''

	# Ini ke bawah untuk umum
	def get_data_request (self, request):
		# Mengumpulkan data yang di POST kan
		# field ini untuk data dengan input type radio
		type_quest = request.POST.get('type_quest')
		# Field ini berupa data form (no option)
		opti_count = request.POST.get('num_opsi')
		# field ini untuk data dengan input type radio
		category = request.POST.get('cat')
		rd_option = request.POST.get('acak')
		# Field ini berupa data form (no option)
		text_quest = request.POST.get('quest')
		img_quest = request.FILES.get('img_q')
		audio_quest = request.FILES.get('aud_q')
		video_quest = request.FILES.get('vid_q')
		opti_ans_1 = request.POST.get('op_1')
		opti_img_1 = request.FILES.get('img_ans1')
		opti_ans_2 = request.POST.get('op_2')
		opti_img_2 = request.FILES.get('img_ans2')
		opti_ans_3 = request.POST.get('op_3')
		opti_img_3 = request.FILES.get('img_ans3')
		opti_ans_4 = request.POST.get('op_4')
		opti_img_4 = request.FILES.get('img_ans4')
		opti_ans_5 = request.POST.get('op_5')
		opti_img_5 = request.FILES.get('img_ans5')
		# Data dengan type input radio
		rd_opti_ans = request.POST.get('acak_ans')
		# Data dengan type input checkbox
		ans_key = []
		ans_key_str = ''
		if request.POST.get('key1') != None:
			ans_key.append(request.POST.get('key1'))
		if request.POST.get('key2') != None:
			ans_key.append(request.POST.get('key2'))
		if request.POST.get('key3') != None:
			ans_key.append(request.POST.get('key3'))
		if request.POST.get('key4') != None:
			ans_key.append(request.POST.get('key4'))
		if request.POST.get('key5') != None:
			ans_key.append(request.POST.get('key5'))
		
		if len(ans_key) > 1:
			for x in range(len(ans_key)):
				if (x) == len(ans_key)-1:
					ans_key_str += str(ans_key[x])
				else :
					ans_key_str += str(ans_key[x]) + '-'
		elif len(ans_key) == 1 :
			ans_key_str = str(ans_key[0])


		# Penanganan upload file dan replace file
		if self.params_index < len(self.listData):
			# bandingkan filename yang baru diuplload dengan sebelumnya
			try:
				if len(self.listData[self.params_index][7]) == 0:
					opti_img_1 = self.upload_files(opti_img_1)
				elif self.listData[self.params_index][7] != opti_img_1.name :
					url = 'media/'+self.listData[self.params_index][7]
					os.remove(url)
					opti_img_1 = self.upload_files(opti_img_1)
				else:
					opti_img_1 = self.listData[self.params_index][7]
			except Exception as e:
				opti_img_1 = self.listData[self.params_index][7]

			try:
				if len(self.listData[self.params_index][9]) == 0:
					opti_img_2 = self.upload_files(opti_img_2)
				elif self.listData[self.params_index][9] != opti_img_2.name :
					url = 'media/'+self.listData[self.params_index][9]
					os.remove(url)
					opti_img_2 = self.upload_files(opti_img_2)
				else:
					opti_img_2 = self.listData[self.params_index][9]
			except Exception as e:
				opti_img_2 = self.listData[self.params_index][9]

			try:
				if len(self.listData[self.params_index][11]) == 0:
					opti_img_3 = self.upload_files(opti_img_3)
				elif self.listData[self.params_index][11] != opti_img_3.name :
					url = 'media/'+self.listData[self.params_index][11]
					os.remove(url)
					opti_img_3 = self.upload_files(opti_img_3)
				else:
					opti_img_3 = self.listData[self.params_index][11]
			except Exception as e:
				opti_img_3 = self.listData[self.params_index][11]

			try:
				if len(self.listData[self.params_index][13]) == 0:
					opti_img_4 = self.upload_files(opti_img_4)
				elif self.listData[self.params_index][13] != opti_img_4.name :
					url = 'media/'+self.listData[self.params_index][13]
					os.remove(url)
					opti_img_4 = self.upload_files(opti_img_4)
				else:
					opti_img_4 = self.listData[self.params_index][13]
			except Exception as e:
				opti_img_4 = self.listData[self.params_index][13]

			try:
				if len(self.listData[self.params_index][15]) == 0:
					opti_img_5 = self.upload_files(opti_img_5)
				elif self.listData[self.params_index][15] != opti_img_5.name :
					url = 'media/'+self.listData[self.params_index][15]
					os.remove(url)
					opti_img_5 = self.upload_files(opti_img_5)
				else:
					opti_img_5 = self.listData[self.params_index][15]
			except Exception as e:
				opti_img_5 = self.listData[self.params_index][15]

			try:
				if len(self.listData[self.params_index][16]) == 0:
					audio_quest = self.upload_files(audio_quest)
				elif self.listData[self.params_index][16] != audio_quest.name :
					url = 'media/'+self.listData[self.params_index][16]
					os.remove(url)
					audio_quest = self.upload_files(audio_quest)
				else:
					audio_quest = self.listData[self.params_index][16]
			except Exception as e:
				audio_quest = self.listData[self.params_index][16]

			try:
				if len(self.listData[self.params_index][17]) == 0:
					video_quest = self.upload_files(video_quest)
				elif self.listData[self.params_index][17] != video_quest.name :
					url = 'media/'+self.listData[self.params_index][17]
					os.remove(url)
					video_quest = self.upload_files(video_quest)
				else:
					video_quest = self.listData[self.params_index][17]
			except Exception as e:
				video_quest = self.listData[self.params_index][17]

			try:
				print(len(self.listData[self.params_index][18]),' -- ',len(img_quest.name),'\n')
				if len(self.listData[self.params_index][18]) == 0:
					img_quest = self.upload_files(img_quest)
				elif self.listData[self.params_index][18] != img_quest.name:
					url = 'media/'+self.listData[self.params_index][18]
					os.remove(url)
					img_quest = self.upload_files(img_quest)
				else:
					img_quest = self.listData[self.params_index][18]
			except Exception as e:
				img_quest = self.listData[self.params_index][18]
		else:
			opti_img_1 = self.upload_files(opti_img_1)
			opti_img_2 = self.upload_files(opti_img_2)
			opti_img_3 = self.upload_files(opti_img_3)
			opti_img_4 = self.upload_files(opti_img_4)
			opti_img_5 = self.upload_files(opti_img_5)
			audio_quest = self.upload_files(audio_quest)
			video_quest = self.upload_files(video_quest)
			img_quest = self.upload_files(img_quest)

		tmp = [
			0,type_quest,opti_count,category,rd_option,text_quest,
			opti_ans_1,opti_img_1,opti_ans_2,opti_img_2,opti_ans_3,
			opti_img_3,opti_ans_4,opti_img_4,opti_ans_5,opti_img_5,
			audio_quest,video_quest,img_quest,ans_key_str,rd_opti_ans
		]

		return tmp

	def next(self, request):

		data = self.get_data_request(request)

		if self.params_index == len(self.listData):
			self.listData.append(data)
		elif self.params_index < len(self.listData):
			self.listData[self.params_index] = data

		self.params_index += 1

		return self.params_index, len(self.listData)

	def prev(self, request):

		data = self.get_data_request(request)

		if self.params_index == len(self.listData):
			self.listData.append(data)
		elif self.params_index < len(self.listData):
			self.listData[self.params_index] = data

		if self.params_index != 0:
			self.params_index -= 1

		return self.params_index, len(self.listData)

	def get_in_page(self, index):

		type_quest = 'A'+self.listData[index][1]
		opti_count = self.listData[index][2]
		category = 'C'+self.listData[index][3]
		rd_option = 'D'+self.listData[index][4]
		text_quest = self.listData[index][5]
		img_quest = self.listData[index][18]
		audio_quest = self.listData[index][16]
		video_quest = self.listData[index][17]
		opti_ans_1 = self.listData[index][6]
		opti_img_1 = self.listData[index][7]
		opti_ans_2 = self.listData[index][8]
		opti_img_2 = self.listData[index][9]
		opti_ans_3 = self.listData[index][10]
		opti_img_3 = self.listData[index][11]
		opti_ans_4 = self.listData[index][12]
		opti_img_4 = self.listData[index][13]
		opti_ans_5 = self.listData[index][14]
		opti_img_5 = self.listData[index][15]
		ans_key_str = self.listData[index][19]
		rd_opti_ans = 'T'+self.listData[index][20]

		view = [
			index,type_quest,opti_count,category,rd_option,text_quest,
			opti_ans_1,opti_img_1,opti_ans_2,opti_img_2,opti_ans_3,
			opti_img_3,opti_ans_4,opti_img_4,opti_ans_5,opti_img_5,
			audio_quest,video_quest,img_quest,ans_key_str,rd_opti_ans
		]

		return view

	def del_data_quest(self, index):
		for x in range(len(self.listData[index])):
			if x >= 7 and x <= 15 :
				if x % 2 != 0:
					if self.listData[index][x] != '':
						url = 'media/'+self.listData[index][x]
						os.remove(url)
			elif x >= 16 and x <= 18 :
				if self.listData[index][x] != '':
					url = 'media/'+self.listData[index][x]
					os.remove(url)

		del self.listData[index]
		if index == 0 :
			self.params_index = 0
		else :
			self.params_index -= 1

	def get_all_data(self):
		return self.listData

	def get_index_params(self):
		return self.params_index

	def clear_list(self):
		self.listData.clear()

	def get_len_data(self):
		return len(self.listData)