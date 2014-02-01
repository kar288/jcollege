from django.db import models

from django.contrib.auth.models import User

class Student(User):
	jid = models.CharField(max_length = 40);
	lname = models.CharField(max_length = 100);
	college = models.CharField(max_length = 100);
	room = models.CharField(max_length = 6);
	phone = models.CharField(max_length = 100);
	country = models.CharField(max_length = 100);
	majorinfo = models.CharField(max_length = 100);
