# -*- coding: utf-8 -*-
import re
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import User
from .handle_excel_functions import ExcelFile
from .functions_statics import get_default_id

# Create your models here.


# TODO модель обработки файла эксель
# TODO модель статусов
# TODO модель заявок
# TODO модель ошибок
# TODO модель доработок
# TODO модель модель дефектов
# TODO модель писем
# TODO модель заявок - дефектов
# TODO модель комментариев к заявке


class Status(models.Model):
    """
    Статус объектов
    """
    list_links_id = [
        (1, 'ошибка/обращение'),
        (2, 'доработка'),
        (3, 'дефект'),
    ]
    type_id = models.IntegerField(choices=list_links_id)  # тип статуса
    status_key = models.CharField(max_length=20)  # короткое обоздначение статуса
    ru_status_name = models.CharField(max_length=50)  # русское название статуса

    def __str__(self):
        return f'{self.ru_status_name}'

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class ActualStatusManager(models.Manager):
    """Менеджер актуальных статусов"""
    def get_queryset(self):
        from functools import reduce
        exclude_statuses = ['closed', 'resolved', 'done', 'canceled', 'fixed', 'not_actual']
        query = reduce(lambda q, value: q | models.Q(status__status_key=value), exclude_statuses, models.Q())
        return super().get_queryset().filter(~query)


class RequestSolvo(models.Model):
    """
    Заявка в Солво
    """

    solvo_number = models.IntegerField(unique=True)
    subject = models.CharField(max_length=255)
    description = models.TextField()
    solvo_registered_date = models.DateTimeField()
    row_created = models.DateTimeField(auto_now_add=True)
    row_modified = models.DateTimeField(auto_now=True)
    comment = models.TextField(null=True, blank=True)
    is_defect_registered = models.BooleanField(default=False)
    era_critical_prior = models.ImageField(default=50)
    request_type = None

    objects = models.Manager()
    actual_requests = ActualStatusManager()

    @property
    def clear_subject(self):
        return re.sub(r'\[#(\d+)\]', '', str(self.subject))

    def __str__(self):
        return f'[{self.solvo_number}]--{self.clear_subject}'

    def get_absolute_url(self):
        """
        веруть абсолютный url
        :return:
        """

        return reverse('solvo-support:request-details', args=[self.request_type, self.solvo_number])

    def get_last_email(self):
        """
        получить последнее письмо

        :return:
        """
        last_email = EmailSolvo.objects.filter(request_solvo=self.solvo_number).latest('date_received')
        return last_email

    def link_all_emails_by_request(self):
        """
        ссылка на все письма по заявке
        :return:
        """

        return reverse('solvo-support:list-emails', args=[self.solvo_number])

    class Meta:
        ordering = ['-solvo_registered_date']
        verbose_name = 'Заявка'
        verbose_name_plural = 'Заявки'


class ErrorSolvo(RequestSolvo):
    """
    Ошибки в Солво
    """
    status = models.ForeignKey('Status',
                               limit_choices_to={'type_id': 1},
                               on_delete=models.PROTECT,
                               default=1
                               )
    request_type = 'error'

    class Meta:
        verbose_name = 'Ошибка/обращение'
        verbose_name_plural = 'Ошибки/обращения'


class RevisionSolvo(RequestSolvo):
    """
    Доработка Солво
    """
    status = models.ForeignKey('Status',
                               limit_choices_to={'type_id': 2},
                               on_delete=models.PROTECT,
                               default=7
                               )
    solvo_revision_number = models.CharField(max_length=60, unique=True)
    hours_for_develop = models.IntegerField(null=True, blank=True)
    deadline_date = models.DateTimeField(null=True, blank=True)
    is_accelerated = models.BooleanField(default=False)
    request_type = 'revision'

    class Meta:
        verbose_name = 'Доработка'
        verbose_name_plural = 'Доработки'


class BugCriticalSolvo(models.Model):
    """
    Критичность дефектов Солво
    """
    key_name = models.CharField(max_length=1, unique=True)
    ru_name = models.CharField(max_length=40)
    days_for_fix = models.IntegerField()

    class Meta:
        unique_together = ['key_name', 'ru_name']
        verbose_name = 'Критичность дефекта'
        verbose_name_plural = 'Список уровней критичности'

    def __str__(self):
        return self.ru_name


class BugSolvo(models.Model):
    """
    Дефект Солво
    """

    default_status_id = get_default_id(3, 'registered', 13)
    solvo_number = models.IntegerField(unique=True)
    name = models.CharField(max_length=200)
    date_registered = models.DateTimeField()
    critical_state = models.ForeignKey('BugCriticalSolvo',  on_delete=models.PROTECT, to_field='key_name')
    status = models.ForeignKey('Status',
                               on_delete=models.PROTECT,
                               limit_choices_to={'type_id': 3},
                               default=default_status_id)

    objects = models.Manager()
    actual_bugs = ActualStatusManager()

    def __str__(self):
        return f'{self.solvo_number} ++ {self.name}'

    def get_absolute_url(self):
        return reverse('solvo-support:bug-details', args=[self.solvo_number])

    class Meta:
        verbose_name = 'Дефект'
        verbose_name_plural = 'Дефекты'


class RequestBugSolvo(models.Model):
    """
    Связь Заявки-Дефекты Солво

    """
    request = models.ForeignKey('RequestSolvo', on_delete=models.PROTECT, to_field='solvo_number')
    bug = models.ForeignKey('BugSolvo', on_delete=models.PROTECT, to_field='solvo_number')

    def __str__(self):
        return f'Заявка:<{self.request.solvo_number}> *** Дефект<{self.bug.solvo_number}>'

    def save(self, *args, **kwargs):
        if not self.request.is_defect_registered:
            self.request.is_defect_registered = True
            self.request.save()
        super().save()

    class Meta:
        unique_together = ['request', 'bug']
        verbose_name = 'Заявка-Дефект'
        verbose_name_plural = 'Заявки-Дефекты'


class EmailSolvo(models.Model):
    """
    Пепеписка по заявкам с Солво
    """
    request_solvo = models.ForeignKey('RequestSolvo',
                                      on_delete=models.PROTECT,
                                      to_field='solvo_number'
                                      )
    body_email = models.TextField()
    date_received = models.DateTimeField()
    sender = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.request_solvo}'

    def get_absolute_url(self):
        """
        получить url письма
        :return:
        """
        return reverse('solvo-support:email-details', args=[self.pk])

    def link_to_request_solvo(self):
        """
        ссылка на заявку Солво
        :return:
        """
        return self.request_solvo.get_absolute_url()

    class Meta:
        unique_together = ['request_solvo', 'date_received', 'sender']
        verbose_name = 'Письмо'
        verbose_name_plural = 'Письма'


class CommentRequestSolvo(models.Model):
    """
    Комментарии Солво
    """
    user_creator = models.ForeignKey(User, on_delete=models.PROTECT)
    request_solvo = models.ForeignKey('RequestSolvo', on_delete=models.PROTECT)
    comment_to_request = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)


class ExcelFileHandle(models.Model):
    """
    Обработка файлов эксель
    """
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    file_excel = models.FileField(upload_to='requests')
    is_handled = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Обработка файлов эксель'
        verbose_name_plural = verbose_name

    @property
    def abs_path_name(self):
        """
        получить путь к файлу

        :return: путь к файлу
        """
        return self.file_excel.path

    def __str__(self):
        return f'{self.abs_path_name}'

    @staticmethod
    def insert_new_requests(excel_requests_dict):
        """
        вставить новые заявки

        :param excel_requests_dict:
        :return:
        """
        db_exist_requests = RequestSolvo.objects.all()  # получаем существующие заявки из БД
        # получаем существующие номера заявок из БД
        db_exist_request_nums = {str(request.solvo_number) for request in db_exist_requests}
        # вставляем заявку по типу, если её нет в системе
        for number_request, info_request in excel_requests_dict.items():
            if number_request not in db_exist_request_nums:
                if info_request.type_request == 'revision':
                    new_revision = RevisionSolvo(
                        solvo_number=int(number_request),
                        subject=info_request.subject,
                        description=info_request.body,
                        solvo_registered_date=info_request.date_received,
                        solvo_revision_number=info_request.number_revision
                    )
                    new_revision.save()
                else:
                    new_error = ErrorSolvo(
                        solvo_number=int(number_request),
                        subject=info_request.subject,
                        description=info_request.body,
                        solvo_registered_date=info_request.date_received,
                    )
                    new_error.save()

    @staticmethod
    def insert_new_emails(excel_list_request_emails):
        """
        вставляему новые письма

        :param excel_list_request_emails: письма-заявки из экселя

        :return:
        """
        for email in excel_list_request_emails:
            try:
                request = RequestSolvo.objects.get(solvo_number=email.number_request)
                new_email = EmailSolvo(
                    request_solvo=request,
                    body_email=email.body,
                    date_received=email.date_received,
                    sender=email.sender
                )
                new_email.save()
            except ValueError as ve:
                print('Exist' + ve)
            except Exception as e:
                print(type(e), e)
                pass

    @staticmethod
    def insert_new_bugs(excel_dict_bugs):
        """
        вставить дефекты полученные из эксель

        :return:
        """
        db_bugs = BugSolvo.objects.all()
        db_bugs_nums = {bug.solvo_number for bug in db_bugs}
        for bug_num, bug_info in excel_dict_bugs.items():
            request_number = bug_info.request_number
            if int(bug_num) not in db_bugs_nums:
                try:
                    bug_info.critical_state = BugCriticalSolvo.objects.get(key_name=bug_info.critical_state)
                    del bug_info.request_number
                    new_bug = BugSolvo(**bug_info.__dict__)
                    new_bug.save()
                except Exception as e:
                    print(e)

            try:
                request = RequestSolvo.objects.get(solvo_number=request_number)
                bug = BugSolvo.objects.get(solvo_number=bug_num)
                req_bug = RequestBugSolvo(request=request, bug=bug)
                req_bug.save()
                bug.is_defect_registered = True
                bug.save()
            except Exception as e:
                print(e)

    def handle_excel_file(self):
        """
        обработать загруженный файл

        :return:
        """
        handled_excel_file = ExcelFile(self.abs_path_name)
        ExcelFileHandle.insert_new_requests(handled_excel_file.unique_dict_of_requests)
        ExcelFileHandle.insert_new_emails(handled_excel_file.list_of_requests)
        ExcelFileHandle.insert_new_bugs(handled_excel_file.dict_of_bugs)
        self.is_handled = True
        self.save()
