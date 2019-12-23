from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from Hotelreview.utils.reviewscrapping import reviewscrapping
from Hotelreview.utils.DjangoRating import DjangoRating
from django.conf import settings
import os
import json
from django.http import JsonResponse


temp_dic1 = {}
temp_dic2 = {}
review_list = []

temp_total_review = {}
@csrf_exempt
def index(request):
	return render(request,"Reviewanalysis/search.html")


@csrf_exempt
def submit(request):
	info=request.POST.get('info')
	review_obj = reviewscrapping(info)
	review_list = review_obj.scarapping()
	print(review_list)
	clean_review_obj = DjangoRating(review_list)
	clean_review_list,actual_review = clean_review_obj.review_clean()
	print(clean_review_list)
	avarage_rating,rating_list = clean_review_obj.pedict_review(clean_review_list)
	print(type(actual_review))
	print(len(rating_list))
	total_reviews = len(actual_review)
	print("total_reviews" + str(total_reviews))
	room,r_num,location,l_num,spa_gym,g_num,staff,s_num,cleanliness,c_num,food,f_num,bathroom,b_num,service,ser_num,room_avarage,location_avarage,gym_avarage,staff_avarage,cleanliness_avarage,food_avarage,bathroom_avarage,service_avarage = clean_review_obj.selection_option(actual_review,rating_list)
	temp_dic = {}
	temp_dic1['room'] = room
	temp_dic2['room1'] = r_num
	temp_dic1['location'] = location
	temp_dic2['location1'] =l_num
	temp_dic1['spa_gym'] = spa_gym
	temp_dic2['spa_gym1'] = g_num
	temp_dic1['staff'] = staff
	temp_dic2['staff1'] = s_num
	temp_dic1['cleanliness'] = cleanliness
	temp_dic2['cleanliness1'] = c_num
	temp_dic1['food'] = food
	temp_dic2['food1'] = f_num
	temp_dic1['bathroom'] = bathroom
	temp_dic2['bathroom1'] =b_num
	temp_dic1['service']  =service
	temp_dic2['service1'] = ser_num
	temp_dic['total_reviews'] = total_reviews
	temp_dic['avarage_rating'] = avarage_rating
	temp_dic['location_avarage'] = location_avarage
	temp_dic['gym_avarage'] = gym_avarage
	temp_dic['staff_avarage'] = staff_avarage
	temp_dic['cleanliness_avarage'] = cleanliness_avarage
	temp_dic['bathroom_avarage'] = bathroom_avarage
	temp_dic['service_avarage'] = service_avarage
	temp_dic['room_avarage'] = room_avarage
	temp_dic['food_avarage'] = food_avarage
	temp_dic['all_review'] = actual_review
	temp_dic['hotel_name'] = info
	
	temp_total_review["total"] = len(actual_review)
	negative_count = 0
	positive_count = 0
	neutral_count = 0
	for i in range(len(rating_list)):
		if rating_list[i]==3:
			negative_count = negative_count + 1
			pass
		elif rating_list[i]==5:
			positive_count = positive_count + 1
			pass
		elif rating_list[i]==4:
			neutral_count = neutral_count + 1
		temp_dic['negative_count'] = negative_count / len(rating_list)
		temp_dic['positive_count'] = positive_count / len(rating_list)
		temp_dic['neutral_count'] = neutral_count / len(rating_list)
	print(temp_dic['negative_count'])

	print(positive_count)
	print(neutral_count)
	return render(request,"Reviewanalysis/display.html",{'dictionary':temp_dic})
# Create your views here.
#Novotel Ahmedabad
#OYO 10197 Hotel Apex
@csrf_exempt
def check_index(request):
	temp_dic = {}
	values = request.GET.get('opt') 
	print(temp_total_review["total"])
	result = json.loads(values)
	#print(temp_dic1)
	#print(json.loads(json.dumps(values)))
	#result = [x.strip() for x in values.split(',')]
	#print(result[0])
	#print(type(result[0]))
	#print(result)
	final_list_review = []
	final_list_rating = []
	for i in range(len(result)):
		#print(i)
		final_list_review = final_list_review + temp_dic1[result[i]]
		final_list_rating = final_list_rating + temp_dic2[result[i]+"1"]
	temp_dic['review_length']=temp_total_review["total"]
	temp_dic['review_list']=final_list_review
	temp_dic['rating_list']=list(map(str,final_list_rating))
	print(temp_dic)
	#temp_dic = {"review_length": "0", "review_list": ["The room was dirty, bins overflowing and so much dirt on the floor which was cleaned up a little in the middle of the room. The bathroom wasn't cleaned. The beds were all used when I arrived and they didn't change any of the sheets for the next guests. I also left something behind, and when I tried to organise with them to go back an get it, they said they would have to call someone to see if it was there, said they would call me back... They never did. The number they gave me for the hostel didn't work, so I never got it back.", "About 5 males landed into the room about 4.30am and proceeded to chat louded with the main light on for 3 hours despite numerous requests to shut up! They had no consideration at all for other guests and to top it all they went actually staying but had just been let use facilities by night porter!", "We booked a mixed dormitory because we are a couple, but they don't have mixed dormitory! So we had to be separated. We had to plan things together but we were not allowed to go to the dormitory of the other, even if there was no-one in the girl dormitory, so we had to stay in the dining room which is very dirty. Knowing that we didn't have what we booked, we would have like the staff to be more understandable with us. Also, the dining room and the bathroom were very dirty.", "The room was good. Although the bed could use a better mattress."], "rating_list": ["5", "4", "5", "5"]}
	#print(temp_dic)
	return JsonResponse(json.dumps(temp_dic),safe=False)


