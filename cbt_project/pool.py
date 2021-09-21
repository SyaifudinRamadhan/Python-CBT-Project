class quest_data :
	# Variabel data soal dari hasil pengambilan
	dic_quest = []
	keys_quest = []
	err_msg_quest = []
	inf_quest = 'Error, Token salah'

	def setter (self, dic, key, msg):
		self.dic_quest = dic
		self.keys_quest = key
		self.err_msg_quest = msg
	
	def setInfo (self, info):
		self.inf_quest = info

	def getter (self) :
		return self.dic_quest, self.err_msg_quest

	def getInfo (self) :
		return self.inf_quest

	def getKeys (self) :
		return self.keys_quest

	def getTypeQuest (self) :
		return self.dic_quest['type_quest']

	def reset (self) :
		self.dic_quest = []
		self.keys_quest = []
		self.err_msg_quest = []
		self.inf_quest = 'Error, Token salah'

class list_val():
	# constructor
	prev_pss = ''
	out_count = 0
	# ans_list = ''

	def initial (self, width, end, start):
		self.ans_list = ['']*width
		self.end_time = end
		self.start_t = start

	def set_list (self, index, val):
		self.ans_list[index-1] = val

	def set_prev_pss (self, num):
		self.prev_pss = int(num)

	def get_prev_pss (self):
		return self.prev_pss

	def get_len (self):
		return len(self.ans_list)

	def get_list (self, index):
		idx = int(index)
		return self.ans_list[idx]

	def get_all (self):
		return self.ans_list

	def add_out (self):
		self.out_count += 1

	def get_out (self):
		return self.out_count

	def get_limit_time (self):
		return self.end_time

	def get_start_time (self):
		return self.start_t

	def  reset (self):
		self.prev_pss = ''
		self.ans_list = []
		self.out_count = 0