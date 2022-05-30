from rest_framework import serializers


class TaskRequest(serializers.Serializer):
    task_id = serializers.UUIDField()


class TaskResponse(serializers.Serializer):
    task_id = serializers.UUIDField()


class TaskResultResponse(serializers.Serializer):
    total = serializers.IntegerField(help_text="总共数量")
    num = serializers.IntegerField(help_text="已完成数量")
    status = serializers.CharField(
        help_text="PROGRESS, REVOKED, FAILURE, SUCCESS")
    result = serializers.JSONField(help_text="结果")


