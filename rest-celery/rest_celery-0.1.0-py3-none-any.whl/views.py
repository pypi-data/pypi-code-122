from rest_framework import viewsets
from django.http.response import JsonResponse, HttpResponse
from rest_celery import swagger, serializers
from rest_celery import *
# Create your views here.


class TasksView(viewsets.ViewSet):

    @swagger.task_destroy()
    def destroy(self, request, pk):
        revoke(pk)
        return HttpResponse()

    @swagger.task_result()
    def retrieve(self, request, pk):
        total, num, status, result = get_progress(pk)
        data = {"total": total, "num": num, "status": status, "result": result}
        res = serializers.TaskResultResponse(data=data)
        res.is_valid(raise_exception=True)
        return JsonResponse(res.data)
