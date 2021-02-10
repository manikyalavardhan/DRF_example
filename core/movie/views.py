from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import *
from .serializers import UsercollectionSerializer
import requests
import os
import jwt
from requests.auth import HTTPBasicAuth

from rest_framework.permissions import AllowAny,IsAuthenticated

from rest_framework_simplejwt.tokens import Token

from django.conf import settings

class GetMoviesView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request,format=None):
		user = os.environ['Username']
		pwd = os.environ['Password']
		while True:
			res  = requests.get('https://demo.credy.in/api/v1/maya/movies/',auth=HTTPBasicAuth(user,pwd))
			if res.status_code == 200:
				break
		return Response(res.json())

class UserRegisterView(APIView):
	permission_classes = (AllowAny,)
	def post(self,request):
		username = request.data.get('username')
		password = request.data.get('password')
		try:
			User.objects.create(username=username,password=password)
			token = jwt.encode({"username":username,"password":password},settings.JWT_SECRET_KEY,algorithm='HS256')
			content={
				"access_token":token
			}
		except Exception as e:
			content = {"message":"User exists with that name"}
		return Response(content)

class CollectionView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		try:
			queryset = UserCollection.objects.filter(user_id=request.user)
			serializer  = UsercollectionSerializer(queryset,many=True)
			# val = UserCollection.objects.filter(user_id=request.user).values_list('movies')
		except Exception as e:
			data = ''
		content={"is_success":True,"data":{"collection":serializer.data,"favourite_genres":""}}
		return Response(content)

	def post(self,request):
		title = request.data.get('title')
		des = request.data.get('description')
		movies = request.data.get('movies')
		coll_inst = UserCollection.objects.create(user_id=request.user,title=title,description=des,movies=movies)
		content = {"collection_uuid":coll_inst.c_uuid}
		return Response(content)

class CrudCollectionView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request,collection_uuid):
		try:
			queryset = UserCollection.objects.filter(user_id=request.user,c_uuid=collection_uuid)
			serializer  = UsercollectionSerializer(queryset,many=True)
		except Exception as e:
			data = ''
		return Response(serializer.data)
	def put(self,request,collection_uuid):
		coll = UserCollection.objects.get(user_id=request.user,c_uuid=collection_uuid)
		if request.data.get('title'):
			coll.title = request.data.get('title')
		if request.data.get('description'):
			coll.description = request.data.get('description')
		if request.data.get('movies'):
			coll.movies =  request.data.get('movies')
		coll.save()
		return Response()
			
	def delete(self,request,collection_uuid):
		coll_inst = UserCollection.objects.get(user_id=request.user,c_uuid=collection_uuid)
		coll_inst.delete()
		return Response()

class RequestCountView(APIView):
	permission_classes = (IsAuthenticated,)
	def get(self,request):
		try:
			count = os.environ['ReqCount']
		except:
			count = 1
		return Response({"requests":count})

class ResetView(APIView):
	permission_classes = (IsAuthenticated,)
	def post(self,request):
		try:
			os.environ['ReqCount']='0'
		except Exception as e:
			print(e)
		return Response({"message":"request count reset successfully"})