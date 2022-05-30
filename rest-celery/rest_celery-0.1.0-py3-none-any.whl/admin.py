from django.utils.safestring import mark_safe
from django.contrib import admin
from rest_celery import models, get_progress, get_result_by_id, revoke
from celery.states import SUCCESS, REVOKED, FAILURE

STATUS_COLOR_MAP = {
    SUCCESS: "green",
    REVOKED: "orange",
    FAILURE: "red"
}


class TaskResultAdmin(admin.ModelAdmin):
    @admin.display(
        description='进度',
    )
    def progress(self, obj):
        total, num, status, result = get_progress(
            str(obj.id), with_result=False)
        return mark_safe(
            f'''<p>
                    <progress value="{num}" max="{total}"></progress>
                    <span style="color:{STATUS_COLOR_MAP.get(status, "black")}">{num}/{total}&nbsp;&nbsp;{status}</span>
                </p>''')

    @admin.display(
        description='结果',
    )
    def result(self, obj):
        return get_result_by_id(str(obj.id))

    @admin.display(
        description='取消任务'
    )
    def revoke_tasks(modeladmin, request, queryset):
        for obj in queryset:
            revoke(str(obj.id))

    list_per_page = 10
    list_max_show_all = 15
    search_fields = ('id', 'name')
    list_display = ('id', 'name', 'progress', 'result', 'ctime')
    list_filter = ['name']
    actions = [revoke_tasks]


# Register your models here.
admin.site.register(models.TaskResult, TaskResultAdmin)
