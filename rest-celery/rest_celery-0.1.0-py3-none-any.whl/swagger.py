import functools
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_celery.serializers import *


task_result = functools.partial(
    swagger_auto_schema,
    operation_summary="查询任务进度和结果",
    operation_description="",
    responses={
        200: openapi.Response(
            "成功返回",
            schema=TaskResultResponse,
            examples={
                "application/json": {
                    "total": 10,
                    "num": 10,
                    "status": "SUCCESS",
                    "result": '[{"name": "bob"}, {"name": "jan"}]'
                }
            }
        )
    }
)

task_destroy = functools.partial(
    swagger_auto_schema,
    operation_summary="删除任务",
    operation_description="",
    responses={
        200: ""
    }
)
