import json
from app.models import *

def college_to_database(college_name):
	json_file = open("crawler/" + college_name + ".json")
	json_data = json.load(json_file)
	for juser in json_data:
		username = juser['email']
		username = username.replace('@jacobs-university.de', '')
		username = username.replace('.', '')
		password = '1234'
		photourl = juser['photo']
		photourl = photourl.replace('jpeople.user.jacobs-university.de/utils/images/', 'swebtst01.public.jacobs-university.de/jPeople/image.php?id=')
		photourl = photourl.replace('.jpg', '')
		new_juser = Student(jid = juser['id'],\
			fname = juser['fname'],\
			lname = juser['lname'],\
			email = juser['email'],\
			college = college_name[0].upper(),\
			room = juser['room'],\
			phone = juser['phone'],\
			country = juser['country'],\
			username = username,\
			password = password,\
			is_active = False,\
			majorinfo = juser['majorinfo'],\
			majorlong = juser['majorlong'],\
			major = juser['major'],\
			photourl = photourl)
		new_juser.set_password(password)
		new_juser.save()


list_of_colleges = ['mercator','nordmetall','college-III','krupp']

for college in list_of_colleges:
	college_to_database(college)