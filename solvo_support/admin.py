from django.contrib import admin
from .models import ExcelFileHandle, Status, RequestSolvo, ErrorSolvo, RevisionSolvo, BugCriticalSolvo, \
    BugSolvo, EmailSolvo, RequestBugSolvo

# Register your models here.


def file_actions(model_admin, request, queryset):
    """
    Обработка действий для файла экселя
    :param model_admin:
    :param request:
    :param queryset:
    :return:
    """
    for obj in queryset:
        obj.handle_excel_file()


file_actions.short_description = 'Обработать файл экселя'


@admin.register(ExcelFileHandle)
class ExcelFileHandleAdmin(admin.ModelAdmin):
    """
    Модель админа для обработки файлов эксель
    """
    list_display = ('file_excel', 'abs_path_name', 'is_handled', 'date_created', 'date_modified')

    actions = [file_actions, ]


@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    """
    Модель админа для статусов
    """
    list_display = ['type_id', 'status_key', 'ru_status_name']


@admin.register(RequestSolvo)
class RequestAdmin(admin.ModelAdmin):
    """
    Модель админа для заявок
    """
    list_display = ['solvo_number', 'clear_subject', 'solvo_registered_date',
                    'row_modified', 'request_type', 'is_defect_registered']
    search_fields = ['solvo_number', 'subject']


@admin.register(ErrorSolvo)
class ErrorAdmin(admin.ModelAdmin):
    """
    Модель админа для ошибок/обращений
    """
    list_display = ['solvo_number', 'subject', 'status', 'solvo_registered_date', 'row_modified']


@admin.register(RevisionSolvo)
class RevisionAdmin(admin.ModelAdmin):
    """
    Модель админа для доработок
    """
    list_display = ['solvo_number', 'solvo_revision_number', 'subject', 'status', 'solvo_registered_date', 'row_modified']


@admin.register(BugCriticalSolvo)
class BugCriticalSolvoAdmin(admin.ModelAdmin):
    """
    Модель админа для критичности дефекта
    """
    list_display = ['ru_name', 'key_name', 'days_for_fix']


@admin.register(BugSolvo)
class BugCriticalSolvoAdmin(admin.ModelAdmin):
    """
    Модель админа для критичности дефекта
    """
    # list_display = []
    pass


@admin.register(RequestBugSolvo)
class RequestBugSolvoAdmin(admin.ModelAdmin):
    """
    Модель админа для критичности дефекта
    """
    # list_display = []
    pass


@admin.register(EmailSolvo)
class EmailSolvoAdmin(admin.ModelAdmin):
    """
    Модель админа для заявок
    """
    list_display = ['request_solvo', 'date_received', 'sender']
