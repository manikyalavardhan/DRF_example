from .models import *
from rest_framework import serializers

class UsercollectionSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = UserCollection
		fields = ['title','description','movies']
