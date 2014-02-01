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
	photourl = models.CharField(max_length = 100);
	
class Question(models.Model):
	about_user = models.ForeignKey(Student, unique=True);
	content = models.CharField(max_length = 200);
	answer = models.CharField(max_length = 200);

