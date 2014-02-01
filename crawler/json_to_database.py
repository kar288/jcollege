import json
from app.models import *
from collections import OrderedDict

def college_to_database(college_name):
	json_file = open("crawler/" + college_name + ".json")
	json_data = json.load(json_file)
	for juser in json_data:
		major = juser['major']
		exmat = major.find('exmatr')
		if exmat == -1:
			major_list = ['CS', 'EECS', 'ECE', 'ESS', 'EE', 'ACM', 'PHY', 'BCCB', 'BCE', 'IRB', 'ISCP', 'IES', 'ICS', 'ISS', 'ILME', 'CPN', 'MATH', 'GEM', 'BIOCHEM', 'CHEM', 'BIOTECH', 'BIGSSS', 'IR', 'IMS', 'IL', 'BIO/NEURO', 'GH']
			majors = ''
			for major_name in major_list:
				found = major.find(major_name)
				if found != -1:
					majors = majors + major_name + ' '
			if len(majors) != 0:
				majors = majors[:-1]
			print majors		
			username = juser['email']
			username = username.replace('@jacobs-university.de', '')
			username = username.replace('.', '')
			password = '1234'
			photourl = juser['photo']
			photourl = photourl.replace('jpeople.user.jacobs-university.de/utils/images/', 'swebtst01.public.jacobs-university.de/jPeople/image.php?id=')
			photourl = photourl.replace('.jpg', '')
			if True:
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
					major = majors,\
					year = juser['year'],\
					photourl = photourl)
				new_juser.set_password(password)
				new_juser.save()


list_of_colleges = ['mercator','nordmetall','college-III','krupp']

for college in list_of_colleges:
	college_to_database(college)