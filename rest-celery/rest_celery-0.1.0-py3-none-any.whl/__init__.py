from collections import Counter
from celery.result import ResultBase, ResultSet, AsyncResult, GroupResult
from celery.states import SUCCESS, REVOKED, FAILURE, PENDING
from celery import Task
from celery.utils.log import get_task_logger

log = get_task_logger(__name__)


class TaskLogger:
    def __init__(self, task):
        if task.request.root_id != task.request.id:
            self.prefix = f"{task.name} [{task.request.root_id} {task.request.id}]"
        else:
            self.prefix = f"{task.name} [{task.request.root_id}]"

    def info(self, obj):
        return log.info(f"{self.prefix} {obj}")

    def error(self, obj):
        return log.error(f"{self.prefix} {obj}")

    def warn(self, obj):
        return log.warn(f"{self.prefix} {obj}")

    def warning(self, obj):
        return log.warning(f"{self.prefix} {obj}")

    def critical(self, obj):
        return log.critical(f"{self.prefix} {obj}")

    def debug(self, obj):
        return log.debug(f"{self.prefix} {obj}")


class TraceTask(Task):

    record = False

    @property
    def log(self):
        if not hasattr(self, "_log"):
            setattr(self, "_log", TaskLogger(self))
        return self._log

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.log.error(einfo)

    def before_start(self, task_id, args, kwargs):
        if self.record:
            from rest_celery import models
            models.TaskResult.objects.create(
                id=task_id,
                name=self.name
            )
        self.prefix = f"{self.name} {task_id}"
        self.log.info("Start")

    def on_success(self, retval, task_id, args, kwargs):
        self.log.info("Success")


def get_result(result):
    if isinstance(result, ResultSet):
        results = []
        for child in result.results:
            results.append(get_result(child))
        return results
    elif isinstance(result, ResultBase):
        return get_result(result.result)
    return result


def get_result_by_id(id):
    result = AsyncResult(id)
    meta = result._get_task_meta()
    result = meta.get('result', result)
    result = get_result(result)

    def dfs(result):
        real_result = get_result(result)

        if isinstance(real_result, list):
            for i, obj in enumerate(real_result):
                real_result[i] = dfs(obj)

        elif isinstance(real_result, dict):
            for k, obj in real_result.items():
                real_result[k] = dfs(obj)
        return real_result

    return dfs(result)


def get_tasks(id):
    tasks = {}

    def _get_tasks(id):
        result = AsyncResult(id)

        def dfs(result):
            if not isinstance(result, ResultSet) and not result.id in tasks:
                meta = result._get_task_meta()
                tasks[result.id] = result
                if meta.get('parent_id'):
                    _get_tasks(meta.get('parent_id'))
                if meta.get('group_id'):
                    group_result = GroupResult().restore(result.id)
                    if group_result:
                        for _res in group_result.results:
                            dfs(_res)
            for child in result.children or []:
                dfs(child)
        dfs(result)
    _get_tasks(id)
    return tasks


def get_progress(id, with_result=True):
    tasks = get_tasks(id)
    counter = Counter([task.status for task in tasks.values()])
    total = len(tasks)
    num = counter.get(SUCCESS, 0)
    status = "PROGRESS"
    if REVOKED in counter:
        status = REVOKED
    elif FAILURE in counter:
        status = FAILURE
    elif num == total:
        status = SUCCESS
    elif num == 0 and total == 1:
        status = PENDING

    result = ''
    if with_result and status == SUCCESS:
        result = get_result_by_id(id)
    return total, num, status, result


def revoke(id):
    for _, task in get_tasks(id):
        if not task.successful() and not task.failed():
            task.revoke()


def watch(id):
    total, num, status, result = get_progress(id)
    print(f"{status} {num}/{total} {result}")


# -*- coding:utf-8 -*-

def main():
    id = "53f00778-2135-4692-bfa5-7289daf65741"
    root_id = "ca514359-7b5c-44a1-a392-02f4d2f4abbb"
    root_id = "131bf645-a3df-4c2a-9d33-893ce8c7b95e"
    group_id = "3542ff09-4836-4bdf-8db9-ce5e6a99a2f4"
    watch(id)
    # result = AsyncResult(root_id)
    # print(dir(result))
    # print(result.result)


if __name__ == "__main__":
    main()
