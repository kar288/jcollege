from django.db import models

from django.contrib.auth.models import User

MERCATOR = 'M'
COLLEGEIII = 'C'
KRUPP = 'K'
NORDMETALL = 'N'
COLLEGES = (
	(MERCATOR, 'Mercator'),
	(COLLEGEIII, 'C3'),
	(KRUPP, 'Krupp'),
	(NORDMETALL, 'Nordmetall')
)

class Student(User):
	jid = models.CharField(max_length = 40);
	lname = models.CharField(max_length = 100);
	fname = models.CharField(max_length = 100);
	college = models.CharField(max_length=1,
									choices=COLLEGES,
									default=MERCATOR)
	room = models.CharField(max_length = 6);
	phone = models.CharField(max_length = 100);
	country = models.CharField(max_length = 100);
	majorinfo = models.CharField(max_length = 100);
	majorlong = models.CharField(max_length = 100);
	major = models.CharField(max_length = 50);
	year = models.CharField(max_length = 10);
	photourl = models.CharField(max_length = 100);
	points = models.IntegerField(default= 0)
	
class Question(models.Model):
	about_user = models.ForeignKey(Student, unique=True);
	content = models.CharField(max_length = 200);
	answer = models.CharField(max_length = 200);

class College(models.Model):
	name = models.CharField(max_length=1,
									choices=COLLEGES,
									default=MERCATOR)
	points = models.IntegerField(default = 0);

class Popularity(models.Model):
	stud = models.ForeignKey(Student)
	correctly_answered = models.IntegerField(default=0)
	total_questions = models.IntegerField(default=1)

	def __unicode__(self):
		return self.stud.username + " " + str(1.0 * self.correctly_answered / self.total_questions)

major_list = {
	'CS': 'Computer Science',
	'EECS': 'Electrical Engineering and Computer Science',
	'ECE': 'Electrical and Computer Engineering',
	'ESS': 'Earth and Space Sciences',
	'EE': 'Electrical Engineering',
	'ACM': 'Applied Computanional Mathematics',
	'PHY': 'Physics',
	'BCCB': 'Biochemistry and Cell biology',
	'BCE': 'Biochemical Engineering',
	'IRB': 'Intercultural Relations and Behaviour',
	'ISCP': 'Integrated Social and Cognitive Psychology',
	'IES': 'Integrated Environmental Studies',
	'ICS': 'Integrated Cultural Studies',
	'ISS': 'Integrated Social Sciences',
	'ILME': 'International Logistics Management and Engineering',
	'CPN': 'Cognitive Psychology and Neuroscience',
	'MATH': 'Mathematics',
	'GEM': 'Global Economics and Management',
	'BIOCHEM': 'Biochemistry',
	'CHEM': 'Chemistry',
	'BIOTECH': 'Biotechnology',
	'BIGSSS': 'Bremen International School of Social Sciences',
	'IR': 'International Relations',
	'IMS': 'Information Management and Systems',
	'IL': 'International Logistics',
	'BIO/NEURO': 'Biology and Neuroscience',
	'GH': 'Global Humanities'
}