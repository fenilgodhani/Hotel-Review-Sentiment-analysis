#!/usr/bin/env python
# coding: utf-8

# In[21]:


import pandas as pd
import nltk
from nltk.corpus import stopwords
import string
from spellchecker import SpellChecker
from langdetect import detect
from nltk.stem import WordNetLemmatizer
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import model_from_json
from difflib import get_close_matches 
from langdetect import detect
import csv
import numpy as np
import json
import os 
class DjangoRating: 


	def __init__(self,review_list):
		#nltk.download()
		self.review_list = review_list
		# load json and create model
		#json_data = os.path.join(BASE_DIR, 'static', "utils/config/model")
		#json_file = open(json_data,'r')
		self.json_file = open('Hotelreview/static/model.json', 'r')
		self.loaded_model_json = self.json_file.read()
		self.json_file.close()
		self.loaded_model = model_from_json(self.loaded_model_json)
		# load weights into new model
		self.loaded_model.load_weights("Hotelreview/static/model.h5")
		print("Loaded model from disk")
		# create the tokenizer
		self.tokenizer = Tokenizer()

	def review_clean(self):
		spell = SpellChecker()
		lemmatizer = WordNetLemmatizer()
		stop_words = stopwords.words('english')
		temp_token_list = []
		actual_review = []
		for i in range(len(self.review_list)):
			print(i)
			if self.review_list[i]!="There are no comments available for this review":
				try:
					if detect(self.review_list[i]) == "en":
            			#split review using white space....
						words = self.review_list[i].split()
            			# remove punctuation from each word....and convert word into lowercase....
						table = str.maketrans('', '', string.punctuation)
						stripped = [w.translate(table).lower() for w in words]
            			#remove stop word....
						words = [lemmatizer.lemmatize(spell.correction(w)) for w in stripped if not w in stop_words and w.isalpha() and len(w) > 1]
						if words:
							temp_token_list.append(words)
							actual_review.append(self.review_list[i])
						else:
							'''hotel_review.remove(hotel_review[i])'''
							print("No Words")
				except Exception as e:
					print(e)
			else:
				break
		return temp_token_list,actual_review

	def pedict_review(self,temp_list):
	    rating_list = []
	    max_length = 3784
	    # fit the tokenizer on the documents
	    self.tokenizer.fit_on_texts(temp_list)
	    # sequence encode
	    prediction_test = self.tokenizer.texts_to_sequences(temp_list)
	    # pad sequences
	    final_test = pad_sequences(prediction_test, maxlen=max_length, padding='post')
	    for i in range(len(final_test)):
	        temp = []
	        temp.append(final_test[i])
	        prediction = self.loaded_model.predict(np.array(temp))
	        rating_list.append(np.argmax(prediction))
	    if len(rating_list)!=0:
	    	avarage_rating = round(sum(rating_list) / len(rating_list),1)
	    else:
	    	avarage_rating = 0
	    return avarage_rating,rating_list

	# In[23]:


	#Staff location Spa/gym room cleanliness food price bathroom service

	def selection_option(self,actual_review,rating_list):
		room = []
		r_num=[]
		l_num = []
		g_num = []
		s_num=[]
		c_num=[]
		f_num=[]
		b_num=[]
		ser_num=[]
		location = []
		spa_gym = []
		staff = []
		cleanliness = []
		food = []
		bathroom = []
		service = []
		for i in range(len(actual_review)):
		    temp_list = actual_review[i].split()
		    if "room" in temp_list:
		        room.append(actual_review[i])
		        r_num.append(rating_list[i])
		    if "location" in temp_list:
		        location.append(actual_review[i])
		        l_num.append(rating_list[i])
		    if "gym" in temp_list:
		        spa_gym.append(actual_review[i])
		        g_num.append(rating_list[i])
		    if "staff" in temp_list:
		        staff.append(actual_review[i])
		        s_num.append(rating_list[i])
		    if 'cleanliness' in temp_list:
		        cleanliness.append(actual_review[i])
		        c_num.append(rating_list[i])
		    if "food" in temp_list:
		        food.append(actual_review[i])
		        f_num.append(rating_list[i])
		    if 'bathroom' in temp_list:
		        bathroom.append(actual_review[i])
		        b_num.append(rating_list[i])
		    if "service" in temp_list:
		        service.append(actual_review[i])
		        ser_num.append(rating_list[i])
		if len(r_num)!=0:
			room_avarage = round(sum(r_num) / len(r_num),1)
		else:
			room_avarage = 0
		if len(l_num)!=0:
			location_avarage = round(sum(l_num) / len(l_num),1)
		else:
			location_avarage =0
		if len(g_num)!=0:
			gym_avarage = round(sum(g_num) / len(g_num),1)
		else:
			gym_avarage = 0
		if len(s_num)!=0:
			staff_avarage = round(sum(s_num) / len(s_num),1)
		else:
			staff_avarage = 0
		if len(c_num)!=0:
			cleanliness_avarage = round(sum(c_num) / len(c_num),1)
		else:
			cleanliness_avarage = 0
		if len(f_num)!=0:
			food_avarage = round(sum(f_num) / len(f_num),1)
		else:
			food_avarage = 0
		if len(b_num)!=0:
			bathroom_avarage = round(sum(b_num) / len(b_num),1)
		else:
			bathroom_avarage= 0
		if len(ser_num)!=0:
			service_avarage = round(sum(ser_num)/len(ser_num),1)
		else:
			service_avarage = 0
		return room,r_num,location,l_num,spa_gym,g_num,staff,s_num,cleanliness,c_num,food,f_num,bathroom,b_num,service,ser_num,room_avarage,location_avarage,gym_avarage,staff_avarage,cleanliness_avarage,food_avarage,bathroom_avarage,service_avarage


	# In[ ]:




