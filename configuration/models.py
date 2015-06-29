from django.db import models


class Preset(models.Model):
	class Meta():
		db_table = "preset"
	name = models.CharField(max_length=30)
	username = models.CharField(max_length=50, default='', blank=True)
	password = models.CharField(max_length=50, default='', blank=True)
	host = models.CharField(max_length=30)
	port = models.IntegerField()

	def __unicode__(self):
		return self.name