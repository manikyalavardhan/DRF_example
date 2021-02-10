import os
def RequestCountMiddleware(get_response):

	def middleware(request):
		try:
			count = os.environ['ReqCount']
			res = int(count)
			res += 1
			final_count= str(res)
			os.environ['ReqCount']=final_count
		except:
			os.environ['ReqCount']='0'
		response = get_response(request)

		return response 

	return middleware