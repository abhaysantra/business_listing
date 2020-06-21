from django.shortcuts import render
from django.http import Http404, HttpResponse, HttpResponseRedirect, JsonResponse

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import TaskSerializer

from .models import Task
# Create your views here.


#--------------------------- function based view---------------------------###
@api_view(['GET'])
def apiOverview(request):
	api_urls = {
		'List':'/task-list/',
		'Detail View':'/task-detail/<str:pk>/',
		'Create':'/task-create/',
		'Update':'/task-update/<str:pk>/',
		'Delete':'/task-delete/<str:pk>/',
		}

	return Response(api_urls)

@api_view(['GET'])
def taskList(request):
	tasks = Task.objects.all().order_by('-id')
	serializer = TaskSerializer(tasks, many=True)
	# return Response(serializer.data)

	result = {'result': serializer.data,'status':'True','found':False}
	# return Response(serializer.data)
	return Response(result)

@api_view(['GET'])
def taskDetail(request, pk):
	tasks = Task.objects.get(id=pk)
	serializer = TaskSerializer(tasks, many=False)
	result = {'result': serializer.data,'status':'True'}
	# return Response(serializer.data)
	return Response(result)


@api_view(['POST'])
def taskCreate(request):
	serializer = TaskSerializer(data=request.data)

	if serializer.is_valid():
		serializer.save()

	return Response(serializer.data)

@api_view(['POST'])
def taskUpdate(request, pk):
	try:
		task = Task.objects.get(id=pk)
		serializer = TaskSerializer(instance=task, data=request.data)

		if serializer.is_valid():
			serializer.save()
		else:
			print('in exception...')
			return Response({'status':False})

		return Response(serializer.data)
	except Exception as e:
		print('Some exception comes :',e)
		return Response({'status':False})


@api_view(['DELETE'])
def taskDelete(request, pk):
	task = Task.objects.get(id=pk)
	task.delete()

	return Response('Item succsesfully delete!')

########################  end of function based view--------------- #

#----------------------class based view----#
class taskList(APIView):
	def get(self, request):
		tasks=Task.objects.all()
		serializer = TaskSerializer(tasks, many=True)
		# return JsonResponse(serializer.data, safe=False)
		# return JsonResponse(serializer.data) # error: TypeError: In order to allow non-dict objects to be serialized set the safe parameter to False.
		return Response(serializer.data)

		# result = {'result': serializer.data,'status':'True','found':False}
		# return Response(result)

	def post(self, request):
		data = request.data
		print('data:',data)
		serializer = TaskSerializer(data=data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=201)
		return Response(serializer.errors, status=400)

class taskDetail(APIView):
    def get_object(self, id):
        try:
            return Task.objects.get(id=id)
        except Task.DoesNotExist as e:
            return Response( {"error": "Given Task object not found."}, status=404)

    def get(self, request, id=None):
    	try:
    		instance = self.get_object(id)
    		# print(instance.status_code)
    		serailizer = TaskSerializer(instance)
    		return Response(serailizer.data)
    	except Exception as e:
    		print('exception :',e)
    		return Response(instance.status_code)

    def put(self, request, id=None):
        data = request.data
        instance = self.get_object(id)
        serializer = TaskSerializer(instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)

    def delete(self, request, id=None):
        instance = self.get_object(id)
        instance.delete()
        return HttpResponse(status=204)

# i am testing